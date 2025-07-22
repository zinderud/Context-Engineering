#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bağlam Mühendisliği: Geri Çağırma Destekli Üretim için RAG Tarifleri
===================================================================

Bu modül, LLM bağlamlarını harici bilgiyle geliştirmek için
Geri Çağırma Destekli Üretim (RAG) desenlerinin pratik uygulamalarını
gösterir. Karmaşık altyapı gerektirmeden anahtar kavramları
vurgulayan minimal, verimli uygulamalara odaklanıyoruz.

Ele alınan anahtar kavramlar:
1. Temel RAG boru hattı yapımı
2. Bağlam penceresi yönetimi ve parçalama stratejileri
3. Gömme ve geri çağırma teknikleri
4. Geri çağırma kalitesini ve alaka düzeyini ölçme
5. Bağlam entegrasyon desenleri
6. Gelişmiş RAG varyasyonları

Kullanım:
    # Jupyter veya Colab'da:
    %run 04_rag_recipes.py
    # veya
    from rag_recipes import SimpleRAG, ChunkedRAG, HybridRAG
"""

import os
import re
import json
import time
import numpy as np
import logging
import tiktoken
from typing import Dict, List, Tuple, Any, Optional, Union, Callable, TypeVar
from dataclasses import dataclass
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, HTML

# Günlüğe kaydetmeyi yapılandır
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Gerekli kütüphaneleri kontrol et
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI paketi bulunamadı. Yüklemek için: pip install openai")

try:
    import dotenv
    dotenv.load_dotenv()
    ENV_LOADED = True
except ImportError:
    ENV_LOADED = False
    logger.warning("python-dotenv bulunamadı. Yüklemek için: pip install python-dotenv")

try:
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn bulunamadı. Yüklemek için: pip install scikit-learn")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logger.warning("NumPy bulunamadı. Yüklemek için: pip install numpy")

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS bulunamadı. Yüklemek için: pip install faiss-cpu veya faiss-gpu")

# Sabitler
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 500
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200
DEFAULT_TOP_K = 3


# Temel Veri Yapıları
# =====================

@dataclass
class Document:
    """Meta verileriyle birlikte bir belgeyi veya metin parçasını temsil eder."""
    content: str
    metadata: Dict[str, Any] = None
    embedding: Optional[List[float]] = None
    id: Optional[str] = None
    
    def __post_init__(self):
        """Sağlanmazsa varsayılan değerleri başlatır."""
        if self.metadata is None:
            self.metadata = {}
        
        if self.id is None:
            # İçerik karmasına dayalı basit bir kimlik oluştur
            import hashlib
            self.id = hashlib.md5(self.content.encode()).hexdigest()[:8]


# Yardımcı Fonksiyonlar
# ===============

def setup_client(api_key=None, model=DEFAULT_MODEL):
    """
    LLM etkileşimleri için API istemcisini kurar.

    Args:
        api_key: API anahtarı (None ise, ortamda OPENAI_API_KEY aranır)
        model: Kullanılacak model adı

    Returns:
        tuple: (istemci, model_adı)
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key is None and not ENV_LOADED:
            logger.warning("API anahtarı bulunamadı. OPENAI_API_KEY ortam değişkenini ayarlayın veya api_key parametresini geçin.")
    
    if OPENAI_AVAILABLE:
        client = OpenAI(api_key=api_key)
        return client, model
    else:
        logger.error("OpenAI paketi gerekli. Yüklemek için: pip install openai")
        return None, model


def count_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
    """
    Metin dizesindeki jetonları uygun jetonlayıcıyı kullanarak sayar.

    Args:
        text: Jetonlanacak metin
        model: Jetonlama için kullanılacak model adı

    Returns:
        int: Jeton sayısı
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception as e:
        # Tiktoken modeli desteklemediğinde geri düşüş
        logger.warning(f"{model} için tiktoken kullanılamadı: {e}")
        # Kaba bir tahmin: 1 jeton ≈ İngilizce'de 4 karakter
        return len(text) // 4


def generate_embedding(
    text: str,
    client=None,
    model: str = DEFAULT_EMBEDDING_MODEL
) -> List[float]:
    """
    Verilen metin için bir gömme vektörü oluşturur.

    Args:
        text: Gömülecek metin
        client: API istemcisi (None ise, bir tane oluşturulur)
        model: Gömme modeli adı

    Returns:
        list: Gömme vektörü
    """
    if client is None:
        client, _ = setup_client()
        if client is None:
            # İstemci yoksa sahte gömme döndür
            return [0.0] * 1536  # Birçok gömme modeli için varsayılan boyut
    
    try:
        response = client.embeddings.create(
            model=model,
            input=[text]
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Gömme oluşturulurken hata oluştu: {e}")
        # Hata durumunda sahte gömme döndür
        return [0.0] * 1536


def generate_response(
    prompt: str,
    client=None,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    system_message: str = "Yardımcı bir asistansınız."
) -> Tuple[str, Dict[str, Any]]:
    """
    LLM'den bir yanıt üretir ve meta verilerle birlikte döndürür.

    Args:
        prompt: Gönderilecek istem
        client: API istemcisi (None ise, bir tane oluşturulur)
        model: Model adı
        temperature: Sıcaklık parametresi
        max_tokens: Üretilecek maksimum jeton sayısı
        system_message: Kullanılacak sistem mesajı

    Returns:
        tuple: (yanıt_metni, meta_veriler)
    """
    if client is None:
        client, model = setup_client(model=model)
        if client is None:
            return "HATA: Kullanılabilir API istemcisi yok", {"error": "API istemcisi yok"}
    
    prompt_tokens = count_tokens(prompt, model)
    system_tokens = count_tokens(system_message, model)
    
    metadata = {
        "prompt_tokens": prompt_tokens,
        "system_tokens": system_tokens,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "timestamp": time.time()
    }
    
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        latency = time.time() - start_time
        
        response_text = response.choices[0].message.content
        response_tokens = count_tokens(response_text, model)
        
        metadata.update({
            "latency": latency,
            "response_tokens": response_tokens,
            "total_tokens": prompt_tokens + system_tokens + response_tokens,
            "token_efficiency": response_tokens / (prompt_tokens + system_tokens) if (prompt_tokens + system_tokens) > 0 else 0,
            "tokens_per_second": response_tokens / latency if latency > 0 else 0
        })
        
        return response_text, metadata
    
    except Exception as e:
        logger.error(f"Yanıt üretilirken hata oluştu: {e}")
        metadata["error"] = str(e)
        return f"HATA: {str(e)}", metadata


def format_metrics(metrics: Dict[str, Any]) -> str:
    """
    Metrikler sözlüğünü okunabilir bir dizeye biçimlendirir.
    
    Args:
        metrics: Metrikler sözlüğü
        
    Returns:
        str: Biçimlendirilmiş metrikler dizesi
    """
    # Gösterilecek en önemli metrikleri seç
    key_metrics = {
        "prompt_tokens": metrics.get("prompt_tokens", 0),
        "response_tokens": metrics.get("response_tokens", 0),
        "total_tokens": metrics.get("total_tokens", 0),
        "latency": f"{metrics.get('latency', 0):.2f}s",
        "token_efficiency": f"{metrics.get('token_efficiency', 0):.2f}"
    }
    
    return " | ".join([f"{k}: {v}" for k, v in key_metrics.items()])


def display_response(
    prompt: str,
    response: str,
    retrieved_context: Optional[str] = None,
    metrics: Dict[str, Any] = None,
    show_prompt: bool = True,
    show_context: bool = True
) -> None:
    """
    Bir istem-yanıt çiftini bir not defterinde metriklerle birlikte görüntüler.
    
    Args:
        prompt: İstem metni
        response: Yanıt metni
        retrieved_context: Geri çağrılan bağlam (isteğe bağlı)
        metrics: Metrikler sözlüğü (isteğe bağlı)
        show_prompt: İstem metninin gösterilip gösterilmeyeceği
        show_context: Geri çağrılan bağlamın gösterilip gösterilmeyeceği
    """
    if show_prompt:
        display(HTML("<h4>Sorgu:</h4>"))
        display(Markdown(f"```
{prompt}
```"))
    
    if retrieved_context and show_context:
        display(HTML("<h4>Geri Çağrılan Bağlam:</h4>"))
        display(Markdown(f"```
{retrieved_context}
```"))
    
    display(HTML("<h4>Yanıt:</h4>"))
    display(Markdown(response))
    
    if metrics:
        display(HTML("<h4>Metrikler:</h4>"))
        display(Markdown(f"```
{format_metrics(metrics)}
```"))


# Belge İşleme Fonksiyonları
# ============================

def text_to_chunks(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    model: str = DEFAULT_MODEL
) -> List[Document]:
    """
    Metni belirtilen jeton boyutunda örtüşen parçalara böler.
    
    Args:
        text: Bölünecek metin
        chunk_size: Parça başına maksimum jeton
        chunk_overlap: Parçalar arasında örtüşecek jeton sayısı
        model: Jetonlama için kullanılacak model
        
    Returns:
        list: Belge nesneleri listesi
    """
    if not text:
        return []
    
    # Jetonlayıcıyı al
    try:
        encoding = tiktoken.encoding_for_model(model)
    except:
        logger.warning(f"{model} için jetonlayıcı alınamadı. Yaklaşık parçalama kullanılıyor.")
        return _approximate_text_to_chunks(text, chunk_size, chunk_overlap)
    
    # Metni jetonla
    tokens = encoding.encode(text)
    
    # Parçaları oluştur
    chunks = []
    i = 0
    while i < len(tokens):
        # Parça jetonlarını çıkar
        chunk_end = min(i + chunk_size, len(tokens))
        chunk_tokens = tokens[i:chunk_end]
        
        # Metne geri çöz
        chunk_text = encoding.decode(chunk_tokens)
        
        # Belge oluştur
        chunks.append(Document(
            content=chunk_text,
            metadata={
                "start_idx": i,
                "end_idx": chunk_end,
                "chunk_size": len(chunk_tokens)
            }
        ))
        
        # Örtüşmeyi dikkate alarak bir sonraki parçaya geç
        i += max(1, chunk_size - chunk_overlap)
    
    return chunks


def _approximate_text_to_chunks(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
) -> List[Document]:
    """
    Basit bir karakter tabanlı yaklaşımla metni parçalara böler.
    
    Args:
        text: Bölünecek metin
        chunk_size: Parça başına yaklaşık karakter (~4 karakter/jeton varsayar)
        chunk_overlap: Örtüşecek yaklaşık karakter
        
    Returns:
        list: Belge nesneleri listesi
    """
    # Jeton boyutlarını karakter boyutlarına dönüştür (yaklaşık)
    char_size = chunk_size * 4
    char_overlap = chunk_overlap * 4
    
    # Önce paragraflara göre böl (mümkünse paragrafların ortasında kesmekten kaçınmak için)
    paragraphs = text.split('

')
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for paragraph in paragraphs:
        paragraph_size = len(paragraph)
        
        # Bu paragrafı eklemek parça boyutunu aşarsa
        if current_size + paragraph_size > char_size and current_chunk:
            # Mevcut metinden bir parça oluştur
            chunk_text = '

'.join(current_chunk)
            chunks.append(Document(
                content=chunk_text,
                metadata={"approx_size": current_size}
            ))
            
            # Örtüşme ile yeni bir parça başlat
            # Örtüşmeye dahil edilmesi gereken paragrafları bul
            overlap_size = 0
            overlap_paragraphs = []
            
            for p in reversed(current_chunk):
                p_size = len(p)
                if overlap_size + p_size <= char_overlap:
                    overlap_paragraphs.insert(0, p)
                    overlap_size += p_size
                else:
                    break
            
            current_chunk = overlap_paragraphs
            current_size = overlap_size
        
        # Mevcut paragrafı ekle
        current_chunk.append(paragraph)
        current_size += paragraph_size
    
    # Kalan bir şey varsa son parçayı ekle
    if current_chunk:
        chunk_text = '

'.join(current_chunk)
        chunks.append(Document(
            content=chunk_text,
            metadata={"approx_size": current_size}
        ))
    
    return chunks


def extract_document_batch_embeddings(
    documents: List[Document],
    client=None,
    model: str = DEFAULT_EMBEDDING_MODEL,
    batch_size: int = 10
) -> List[Document]:
    """
    Bir belge topluluğu için verimli bir şekilde gömmeler oluşturur.
    
    Args:
        documents: Gömülecek Belge nesneleri listesi
        client: API istemcisi (None ise, bir tane oluşturulur)
        model: Kullanılacak gömme modeli
        batch_size: Her API çağrısında gömülecek belge sayısı
        
    Returns:
        list: Gömme içeren güncellenmiş Belge nesneleri
    """
    if not documents:
        return []
    
    if client is None:
        client, _ = setup_client()
        if client is None:
            logger.error("Gömme için kullanılabilir API istemcisi yok")
            return documents
    
    # Toplu olarak işle
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        batch_texts = [doc.content for doc in batch]
        
        try:
            # Topluluk için gömmeler oluştur
            response = client.embeddings.create(
                model=model,
                input=batch_texts
            )
            
            # Belgeleri gömmelerle güncelle
            for j, doc in enumerate(batch):
                if j < len(response.data):
                    doc.embedding = response.data[j].embedding
                else:
                    logger.warning(f"Belge {i+j} için eksik gömme")
        except Exception as e:
            logger.error(f"Toplu gömme oluşturulurken hata oluştu: {e}")
    
    return documents


def similarity_search(
    query_embedding: List[float],
    documents: List[Document],
    top_k: int = DEFAULT_TOP_K
) -> List[Tuple[Document, float]]:
    """
    Bir sorgu gömmesine en benzer belgeleri bulur.
    
    Args:
        query_embedding: Sorgu gömme vektörü
        documents: Gömme içeren Belge nesneleri listesi
        top_k: Döndürülecek sonuç sayısı
        
    Returns:
        list: (belge, benzerlik_puanı) demetleri listesi
    """
    if not NUMPY_AVAILABLE:
        logger.error("Benzerlik araması için NumPy gerekli")
        return []
    
    # Gömme içermeyen belgeleri filtrele
    docs_with_embeddings = [doc for doc in documents if doc.embedding is not None]
    
    if not docs_with_embeddings:
        logger.warning("Gömme içeren belge bulunamadı")
        return []
    
    # Gömmeleri numpy dizilerine dönüştür
    query_embedding_np = np.array(query_embedding).reshape(1, -1)
    doc_embeddings = np.array([doc.embedding for doc in docs_with_embeddings])
    
    # Kosinüs benzerliklerini hesapla
    if SKLEARN_AVAILABLE:
        similarities = cosine_similarity(query_embedding_np, doc_embeddings)[0]
    else:
        # Manuel kosinüs benzerliği hesaplamasına geri dön
        norm_query = np.linalg.norm(query_embedding_np)
        norm_docs = np.linalg.norm(doc_embeddings, axis=1)
        dot_products = np.dot(query_embedding_np, doc_embeddings.T)[0]
        similarities = dot_products / (norm_query * norm_docs)
    
    # (belge, benzerlik) çiftleri oluştur
    doc_sim_pairs = list(zip(docs_with_embeddings, similarities))
    
    # Benzerliğe göre sırala (azalan) ve top_k al
    sorted_pairs = sorted(doc_sim_pairs, key=lambda x: x[1], reverse=True)
    return sorted_pairs[:top_k]


def create_faiss_index(documents: List[Document]) -> Any:
    """
    Verimli benzerlik araması için belge gömmelerinden bir FAISS dizini oluşturur.
    
    Args:
        documents: Gömme içeren Belge nesneleri listesi
        
    Returns:
        object: FAISS dizini veya FAISS mevcut değilse None
    """
    if not FAISS_AVAILABLE:
        logger.error("Dizinleme için FAISS gerekli")
        return None
    
    # Gömme içermeyen belgeleri filtrele
    docs_with_embeddings = [doc for doc in documents if doc.embedding is not None]
    
    if not docs_with_embeddings:
        logger.warning("Gömme içeren belge bulunamadı")
        return None
    
    # İlk belgeden gömme boyutunu al
    embedding_dim = len(docs_with_embeddings[0].embedding)
    
    # FAISS dizini oluştur
    index = faiss.IndexFlatL2(embedding_dim)
    
    # Dizine gömmeleri ekle
    embeddings = np.array([doc.embedding for doc in docs_with_embeddings], dtype=np.float32)
    index.add(embeddings)
    
    return index, docs_with_embeddings


def faiss_similarity_search(
    query_embedding: List[float],
    faiss_index: Any,
    documents: List[Document],
    top_k: int = DEFAULT_TOP_K
) -> List[Tuple[Document, float]]:
    """
    Bir FAISS dizini kullanarak en benzer belgeleri bulur.
    
    Args:
        query_embedding: Sorgu gömme vektörü
        faiss_index: FAISS dizini (create_faiss_index'ten)
        documents: Dizine karşılık gelen Belge nesneleri listesi
        top_k: Döndürülecek sonuç sayısı
        
    Returns:
        list: (belge, benzerlik_puanı) demetleri listesi
    """
    if not FAISS_AVAILABLE:
        logger.error("Benzerlik araması için FAISS gerekli")
        return []
    
    if faiss_index is None:
        logger.error("FAISS dizini None")
        return []
    
    # create_faiss_index'ten döndürülürse dizini ve belgeleri aç
    if isinstance(faiss_index, tuple):
        index, docs_with_embeddings = faiss_index
    else:
        index = faiss_index
        docs_with_embeddings = documents
    
    # Sorguyu numpy dizisine dönüştür
    query_np = np.array([query_embedding], dtype=np.float32)
    
    # Dizini ara
    distances, indices = index.search(query_np, top_k)
    
    # (belge, benzerlik) çiftleri oluştur
    # L2 mesafesini benzerlik puanına dönüştür (daha yüksek daha iyi)
    results = []
    for i in range(len(indices[0])):
        idx = indices[0][i]
        if idx < len(docs_with_embeddings):
            # L2 mesafesini benzerliğe dönüştür (1 / (1 + mesafe))
            similarity = 1.0 / (1.0 + distances[0][i])
            results.append((docs_with_embeddings[idx], similarity))
    
    return results


# RAG Sistemi Temel Sınıfı
# =====================

class RAGSystem:
    """
    Geri Çağırma Destekli Üretim sistemleri için temel sınıf.
    Ortak işlevsellik ve arayüzler sağlar.
    """
    
    def __init__(
        self,
        client=None,
        model: str = DEFAULT_MODEL,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
        system_message: str = "Geri çağrılan bağlama göre yanıt veren yardımcı bir asistansınız.",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        verbose: bool = False
    ):
        """
        RAG sistemini başlatır.
        
        Args:
            client: API istemcisi (None ise, bir tane oluşturulur)
            model: Üretim için kullanılacak model adı
            embedding_model: Gömmeler için kullanılacak model adı
            system_message: Kullanılacak sistem mesajı
            max_tokens: Üretilecek maksimum jeton sayısı
            temperature: Sıcaklık parametresi
            verbose: Hata ayıklama bilgilerinin yazdırılıp yazdırılmayacağı
        """
        self.client, self.model = setup_client(model=model) if client is None else (client, model)
        self.embedding_model = embedding_model
        self.system_message = system_message
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.verbose = verbose
        
        # Belge deposunu başlat
        self.documents = []
        
        # Geçmiş ve metrik izlemeyi başlat
        self.history = []
        self.metrics = {
            "total_prompt_tokens": 0,
            "total_response_tokens": 0,
            "total_tokens": 0,
            "total_latency": 0,
            "retrieval_latency": 0,
            "queries": 0
        }
    
    def _log(self, message: str) -> None:
        """
        Ayrıntılı mod etkinse bir mesajı günlüğe kaydeder.
        
        Args:
            message: Günlüğe kaydedilecek mesaj
        """
        if self.verbose:
            logger.info(message)
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Belge deposuna belgeler ekler.
        
        Args:
            documents: Eklenecek Belge nesneleri listesi
        """
        self.documents.extend(documents)
    
    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Belge deposuna isteğe bağlı meta verilerle metinler ekler.
        
        Args:
            texts: Eklenecek metin dizeleri listesi
            metadatas: Meta veri sözlükleri listesi (isteğe bağlı)
        """
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        # Belge nesneleri oluştur
        documents = [
            Document(content=text, metadata=metadata)
            for text, metadata in zip(texts, metadatas)
        ]
        
        self.add_documents(documents)
    
    def _retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K
    ) -> List[Tuple[Document, float]]:
        """
        Bir sorgu için ilgili belgeleri geri çağırır.
        
        Args:
            query: Sorgu dizesi
            top_k: Döndürülecek sonuç sayısı
            
        Returns:
            list: (belge, benzerlik_puanı) demetleri listesi
        """
        # Bu bir yer tutucudur - alt sınıflar bunu uygulamalıdır
        raise NotImplementedError("Alt sınıflar _retrieve uygulamalıdır")
    
    def _format_context(
        self,
        retrieved_documents: List[Tuple[Document, float]]
    ) -> str:
        """
        Geri çağrılan belgeleri bir bağlam dizesine biçimlendirir.
        
        Args:
            retrieved_documents: (belge, benzerlik_puanı) demetleri listesi
            
        Returns:
            str: Biçimlendirilmiş bağlam dizesi
        """
        context_parts = []
        
        for i, (doc, score) in enumerate(retrieved_documents):
            # Belgeyi meta verilerle biçimlendir
            source_info = ""
            if doc.metadata:
                # Varsa kaynak bilgisini çıkar
                source = doc.metadata.get("source", "")
                if source:
                    source_info = f" (Kaynak: {source})"
            
            context_parts.append(f"[Belge {i+1}{source_info}]
{doc.content}
")
        
        return "
".join(context_parts)
    
    def _create_prompt(
        self,
        query: str,
        context: str
    ) -> str:
        """
        Sorguyu ve geri çağrılan bağlamı birleştiren bir istem oluşturur.
        
        Args:
            query: Kullanıcı sorgusu
            context: Geri çağrılan bağlam
            
        Returns:
            str: Biçimlendirilmiş istem
        """
        return f"""Aşağıdaki soruyu geri çağrılan bağlama göre yanıtlayın. Bağlam ilgili bilgiyi içermiyorsa, uydurma bir yanıt vermek yerine bunu belirtin.

Geri Çağrılan Bağlam:
{context}

Soru: {query}

Yanıt:"""
    
    def query(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Bir sorguyu RAG boru hattı üzerinden işler.
        
        Args:
            query: Sorgu dizesi
            top_k: Döndürülecek sonuç sayısı
            
        Returns:
            tuple: (yanıt, detaylar)
        """
        self._log(f"Sorgu işleniyor: {query}")
        
        # İlgili belgeleri geri çağır
        start_time = time.time()
        retrieved_docs = self._retrieve(query, top_k)
        retrieval_latency = time.time() - start_time
        
        # Geri çağrılan belgelerden bağlamı biçimlendir
        context = self._format_context(retrieved_docs)
        
        # İstem oluştur
        prompt = self._create_prompt(query, context)
        
        # Yanıt oluştur
        response, metadata = generate_response(
            prompt=prompt,
            client=self.client,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            system_message=self.system_message
        )
        
        # Metrikleri güncelle
        self.metrics["total_prompt_tokens"] += metadata.get("prompt_tokens", 0)
        self.metrics["total_response_tokens"] += metadata.get("response_tokens", 0)
        self.metrics["total_tokens"] += metadata.get("total_tokens", 0)
        self.metrics["total_latency"] += metadata.get("latency", 0)
        self.metrics["retrieval_latency"] += retrieval_latency
        self.metrics["queries"] += 1
        
        # Geçmişe ekle
        query_record = {
            "query": query,
            "retrieved_docs": [(doc.content, score) for doc, score in retrieved_docs],
            "context": context,
            "prompt": prompt,
            "response": response,
            "metrics": {
                **metadata,
                "retrieval_latency": retrieval_latency
            },
            "timestamp": time.time()
        }
        self.history.append(query_record)
        
        # Detaylar sözlüğü oluştur
        details = {
            "query": query,
            "retrieved_docs": retrieved_docs,
            "context": context,
            "response": response,
            "metrics": {
                **metadata,
                "retrieval_latency": retrieval_latency
            }
        }
        
        return response, details
    
    def get_summary_metrics(self) -> Dict[str, Any]:
        """
        Tüm sorgular için özet metrikleri alır.
        
        Returns:
            dict: Özet metrikler
        """
        summary = self.metrics.copy()
        
        # Türetilmiş metrikleri ekle
        if summary["queries"] > 0:
            summary["avg_latency_per_query"] = summary["total_latency"] / summary["queries"]
            summary["avg_retrieval_latency"] = summary["retrieval_latency"] / summary["queries"]
            
        if summary["total_prompt_tokens"] > 0:
            summary["overall_efficiency"] = (
                summary["total_response_tokens"] / summary["total_prompt_tokens"]
            )
        
        return summary
    
    def display_query_results(self, details: Dict[str, Any], show_context: bool = True) -> None:
        """
        Sorgu sonuçlarını bir not defterinde görüntüler.
        
        Args:
            details: query() işlevinden gelen sorgu detayları
            show_context: Geri çağrılan bağlamın gösterilip gösterilmeyeceği
        """
        display(HTML("<h2>RAG Sorgu Sonuçları</h2>"))
        
        # Sorguyu görüntüle
        display(HTML("<h3>Sorgu</h3>"))
        display(Markdown(details["query"]))
        
        # Geri çağrılan belgeleri görüntüle
        if show_context and "retrieved_docs" in details:
            display(HTML("<h3>Geri Çağrılan Belgeler</h3>"))
            
            for i, (doc, score) in enumerate(details["retrieved_docs"]):
                display(HTML(f"<h4>Belge {i+1} (Puan: {score:.4f})</h4>"))
                
                # Varsa meta verileri görüntüle
                if doc.metadata:
                    display(HTML("<p><em>Meta Veriler:</em></p>"))
                    display(Markdown(f"```json
{json.dumps(doc.metadata, indent=2)}
```"))
                
                # İçeriği görüntüle
                display(Markdown(f"```
{doc.content}
```"))
        
        # Yanıtı görüntüle
        display(HTML("<h3>Yanıt</h3>"))
        display(Markdown(details["response"]))
        
        # Metrikleri görüntüle
        if "metrics" in details:
            display(HTML("<h3>Metrikler</h3>"))
            metrics = details["metrics"]
            
            # Metrikleri biçimlendir
            display(Markdown(f"""
            - İstem jetonları: {metrics.get('prompt_tokens', 0)}
            - Yanıt jetonları: {metrics.get('response_tokens', 0)}
            - Toplam jeton: {metrics.get('total_tokens', 0)}
            - Üretim gecikmesi: {metrics.get('latency', 0):.2f}s
            - Geri çağırma gecikmesi: {metrics.get('retrieval_latency', 0):.2f}s
            - Toplam gecikme: {metrics.get('latency', 0) + metrics.get('retrieval_latency', 0):.2f}s
            """))
    
    def visualize_metrics(self) -> None:
        """
        Sorgular arasında metriklerin görselleştirilmesini oluşturur.
        """
        if not self.history:
            logger.warning("Görselleştirilecek geçmiş yok")
            return
        
        # Çizim için verileri çıkar
        queries = list(range(1, len(self.history) + 1))
        prompt_tokens = [h["metrics"].get("prompt_tokens", 0) for h in self.history]
        response_tokens = [h["metrics"].get("response_tokens", 0) for h in self.history]
        generation_latencies = [h["metrics"].get("latency", 0) for h in self.history]
        retrieval_latencies = [h["metrics"].get("retrieval_latency", 0) for h in self.history]
        total_latencies = [g + r for g, r in zip(generation_latencies, retrieval_latencies)]
        
        # Şekil oluştur
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Sorguya Göre RAG Sistemi Metrikleri", fontsize=16)
        
        # Grafik 1: Jeton kullanımı
        axes[0, 0].bar(queries, prompt_tokens, label="İstem Jetonları", color="blue", alpha=0.7)
        axes[0, 0].bar(queries, response_tokens, bottom=prompt_tokens, 
                       label="Yanıt Jetonları", color="green", alpha=0.7)
        axes[0, 0].set_title("Jeton Kullanımı")
        axes[0, 0].set_xlabel("Sorgu")
        axes[0, 0].set_ylabel("Jetonlar")
        axes[0, 0].legend()
        axes[0, 0].grid(alpha=0.3)
        
        # Grafik 2: Gecikme dökümü
        axes[0, 1].bar(queries, retrieval_latencies, label="Geri Çağırma", color="orange", alpha=0.7)
        axes[0, 1].bar(queries, generation_latencies, bottom=retrieval_latencies, 
                      label="Üretim", color="red", alpha=0.7)
        axes[0, 1].set_title("Gecikme Dökümü")
        axes[0, 1].set_xlabel("Sorgu")
        axes[0, 1].set_ylabel("Saniye")
        axes[0, 1].legend()
        axes[0, 1].grid(alpha=0.3)
        
        # Grafik 3: Geri çağırma sayısı
        if any("retrieved_docs" in h for h in self.history):
            doc_counts = [len(h.get("retrieved_docs", [])) for h in self.history]
            axes[1, 0].plot(queries, doc_counts, marker='o', color="purple", alpha=0.7)
            axes[1, 0].set_title("Geri Çağrılan Belge Sayısı")
            axes[1, 0].set_xlabel("Sorgu")
            axes[1, 0].set_ylabel("Sayı")
            axes[1, 0].grid(alpha=0.3)
        
        # Grafik 4: Kümülatif jetonlar
        cumulative_tokens = np.cumsum([h["metrics"].get("total_tokens", 0) for h in self.history])
        axes[1, 1].plot(queries, cumulative_tokens, marker='^', color="brown", alpha=0.7)
        axes[1, 1].set_title("Kümülatif Jeton Kullanımı")
        axes[1, 1].set_xlabel("Sorgu")
        axes[1, 1].set_ylabel("Toplam Jeton")
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()


# RAG Sistemi Uygulamaları
# =========================

class SimpleRAG(RAGSystem):
    """
    Gömme benzerlik araması kullanan basit bir RAG sistemi.
    """
    
    def __init__(self, **kwargs):
        """Basit RAG sistemini başlatır."""
        super().__init__(**kwargs)
        
        # Belgelerin gömülüp gömülmediği
        self.documents_embedded = False
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Belge deposuna belgeler ekler ve gömme bayrağını sıfırlar.
        
        Args:
            documents: Eklenecek Belge nesneleri listesi
        """
        super().add_documents(documents)
        self.documents_embedded = False
    
    def _ensure_documents_embedded(self) -> None:
        """Tüm belgelerin gömmelere sahip olduğundan emin olur."""
        if self.documents_embedded:
            return
        
        docs_to_embed = [doc for doc in self.documents if doc.embedding is None]
        
        if docs_to_embed:
            self._log(f"{len(docs_to_embed)} belge için gömme oluşturuluyor")
            extract_document_batch_embeddings(
                docs_to_embed, 
                client=self.client,
                model=self.embedding_model
            )
        
        self.documents_embedded = True
    
    def _retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K
    ) -> List[Tuple[Document, float]]:
        """
        Gömme benzerliği kullanarak bir sorgu için ilgili belgeleri geri çağırır.
        
        Args:
            query: Sorgu dizesi
            top_k: Döndürülecek sonuç sayısı
            
        Returns:
            list: (belge, benzerlik_puanı) demetleri listesi
        """
        # Belgelerin gömülü olduğundan emin ol
        self._ensure_documents_embedded()
        
        if not self.documents:
            self._log("Belge deposunda belge yok")
            return []
        
        # Sorgu gömmesi oluştur
        query_embedding = generate_embedding(
            query,
            client=self.client,
            model=self.embedding_model
        )
        
        # Benzerlik araması yap
        results = similarity_search(
            query_embedding,
            self.documents,
            top_k
        )
        
        return results


class ChunkedRAG(SimpleRAG):
    """
    Dizinlemeden önce belgeleri parçalayan bir RAG sistemi.
    """
    
    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
        **kwargs
    ):
        """
        Parçalanmış RAG sistemini başlatır.
        
        Args:
            chunk_size: Parça başına maksimum jeton
            chunk_overlap: Parçalar arasında örtüşecek jeton sayısı
            **kwargs: RAGSystem'e aktarılan ek argümanlar
        """
        super().__init__(**kwargs)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Parçalamadan önceki orijinal belgeler
        self.original_documents = []
        
        # Geri çağırma için FAISS kullanılıp kullanılmayacağı (varsa)
        self.use_faiss = FAISS_AVAILABLE
        self.faiss_index = None
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Belgeleri depoya ekler, parçalar ve gömme bayrağını sıfırlar.
        
        Args:
            documents: Eklenecek Belge nesneleri listesi
        """
        # Orijinal belgeleri sakla
        self.original_documents.extend(documents)
        
        # Her belgeyi parçala
        chunked_docs = []
        for doc in documents:
            chunks = text_to_chunks(
                doc.content,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                model=self.model
            )
            
            # Meta verileri parçalara kopyala ve üst referans ekle
            for i, chunk in enumerate(chunks):
                chunk.metadata.update(doc.metadata)
                chunk.metadata["parent_id"] = doc.id
                chunk.metadata["chunk_index"] = i
                chunk.metadata["parent_content"] = doc.content[:100] + "..." if len(doc.content) > 100 else doc.content
            
            chunked_docs.extend(chunks)
        
        # Parçalanmış belgeleri depoya ekle
        super().add_documents(chunked_docs)
        
        # FAISS kullanılıyorsa FAISS dizinini sıfırla
        if self.use_faiss:
            self.faiss_index = None
    
    def _ensure_documents_embedded(self) -> None:
        """Tüm belgelerin gömmelere sahip olduğundan ve gerekirse FAISS dizini oluşturduğundan emin olur."""
        super()._ensure_documents_embedded()
        
        # FAISS kullanılıyorsa ve FAISS dizini yoksa ve belgeler varsa FAISS dizini oluştur
        if self.use_faiss and self.faiss_index is None and self.documents:
            self._log("FAISS dizini oluşturuluyor")
            self.faiss_index = create_faiss_index(self.documents)
    
    def _retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K
    ) -> List[Tuple[Document, float]]:
        """
        Gömme benzerliği veya FAISS kullanarak ilgili belge parçalarını geri çağırır.
        
        Args:
            query: Sorgu dizesi
            top_k: Döndürülecek sonuç sayısı
            
        Returns:
            list: (belge, benzerlik_puanı) demetleri listesi
        """
        # Belgelerin gömülü olduğundan ve gerekirse FAISS dizininin oluşturulduğundan emin ol
        self._ensure_documents_embedded()
        
        if not self.documents:
            self._log("Belge deposunda belge yok")
            return []
        
        # Sorgu gömmesi oluştur
        query_embedding = generate_embedding(
            query,
            client=self.client,
            model=self.embedding_model
        )
        
        # Varsa geri çağırma için FAISS kullan
        if self.use_faiss and self.faiss_index is not None:
            results = faiss_similarity_search(
                query_embedding,
                self.faiss_index,
                self.documents,
                top_k
            )
        else:
            # Temel benzerlik aramasına geri dön
            results = similarity_search(
                query_embedding,
                self.documents,
                top_k
            )
        
        return results


class HybridRAG(ChunkedRAG):
    """
    Gömme benzerliğini anahtar kelime aramasıyla birleştiren bir RAG sistemi.
    """
    
    def __init__(
        self,
        keyword_weight: float = 0.3,
        **kwargs
    ):
        """
        Hibrit RAG sistemini başlatır.
        
        Args:
            keyword_weight: Anahtar kelime araması için ağırlık (0.0 ile 1.0 arası)
            **kwargs: ChunkedRAG'a aktarılan ek argümanlar
        """
        super().__init__(**kwargs)
        self.keyword_weight = max(0.0, min(1.0, keyword_weight))
        self.embedding_weight = 1.0 - self.keyword_weight
    
    def _keyword_search(
        self,
        query: str,
        documents: List[Document],
        top_k: int = DEFAULT_TOP_K
    ) -> List[Tuple[Document, float]]:
        """
        Belgelerde anahtar kelime araması yapar.
        
        Args:
            query: Sorgu dizesi
            documents: Belge nesneleri listesi
            top_k: Döndürülecek sonuç sayısı
            
        Returns:
            list: (belge, benzerlik_puanı) demetleri listesi
        """
        # Basit anahtar kelime eşleştirme
        query_terms = set(query.lower().split())
        
        results = []
        for doc in documents:
            content = doc.content.lower()
            
            # Eşleşen terimleri say ve puanı hesapla
            matches = sum(1 for term in query_terms if term in content)
            score = matches / len(query_terms) if query_terms else 0.0
            
            results.append((doc, score))
        
        # Puana göre sırala (azalan) ve top_k al
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        return sorted_results[:top_k]
    
    def _retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K
    ) -> List[Tuple[Document, float]]:
        """
        Hibrit arama kullanarak ilgili belge parçalarını geri çağırır.
        
        Args:
            query: Sorgu dizesi
            top_k: Döndürülecek sonuç sayısı
            
        Returns:
            list: (belge, benzerlik_puanı) demetleri listesi
        """
        # Belgelerin gömülü olduğundan emin ol
        self._ensure_documents_embedded()
        
        if not self.documents:
            self._log("Belge deposunda belge yok")
            return []
        
        # Sorgu gömmesi oluştur
        query_embedding = generate_embedding(
            query,
            client=self.client,
            model=self.embedding_model
        )
        
        # Anlamsal arama sonuçlarını al
        if self.use_faiss and self.faiss_index is not None:
            semantic_results = faiss_similarity_search(
                query_embedding,
                self.faiss_index,
                self.documents,
                top_k
            )
        else:
            semantic_results = similarity_search(
                query_embedding,
                self.documents,
                top_k
            )
        
        # Anahtar kelime arama sonuçlarını al
        keyword_results = self._keyword_search(
            query,
            self.documents,
            top_k
        )
        
        # Sonuçları birleştir ve yeniden sırala
        combined_results = {}
        
        # Anlamsal sonuçları ekle
        for doc, score in semantic_results:
            combined_results[doc.id] = {
                "doc": doc,
                "semantic_score": score,
                "keyword_score": 0.0
            }
        
        # Anahtar kelime sonuçlarını ekle
        for doc, score in keyword_results:
            if doc.id in combined_results:
                combined_results[doc.id]["keyword_score"] = score
            else:
                combined_results[doc.id] = {
                    "doc": doc,
                    "semantic_score": 0.0,
                    "keyword_score": score
                }
        
        # Hibrit puanı hesapla
        final_results = []
        for doc_id, data in combined_results.items():
            hybrid_score = (
                self.embedding_weight * data["semantic_score"] + 
                self.keyword_weight * data["keyword_score"]
            )
            final_results.append((data["doc"], hybrid_score))
        
        # Hibrit puana göre sırala ve top_k al
        sorted_final = sorted(final_results, key=lambda x: x[1], reverse=True)
        return sorted_final[:top_k]
