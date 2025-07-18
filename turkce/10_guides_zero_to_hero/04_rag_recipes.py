#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG Tarifleri: Bilgi Tabanlı Üretim için Pratik Şablonlar
========================================================

Bu modül, Harici Bilgi Kullanarak Üretim (Retrieval-Augmented Generation, RAG)
örneklerini minimal ve verimli biçimde uygulamayı gösterir. Amacımız, karmaşık
altyapılara gerek kalmadan temel kavramları öne çıkaran şablonlar sunmaktır.

Ele alınan ana kavramlar:
1. Temel RAG hattı kurulumları
2. Bağlam penceresi yönetimi ve metin parçalama stratejileri
3. Gömü ve alma (embedding & retrieval) yöntemleri
4. Alım kalitesi ve alaka düzeyi ölçümleri
5. Bağlam entegrasyon desenleri
6. İleri düzey RAG varyasyonları

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
# tiktoken için: pip install tiktoken
try:
    import tiktoken
except ImportError:
    tiktoken = None

from typing import Dict, List, Tuple, Any, Optional, Union, Callable, TypeVar
from dataclasses import dataclass
import matplotlib.pyplot as plt
try:
    from IPython.display import display, Markdown, HTML
except ImportError:
    display = print
    Markdown = str
    HTML = str

# Günlüğe kaydetme ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Kütüphane kontrolü
# openai istemcisi için: pip install openai
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI paketi bulunamadı. Yüklemek için: pip install openai")

# ortam değişkenleri için: pip install python-dotenv
try:
    import dotenv
    dotenv.load_dotenv()
    ENV_LOADED = True
except ImportError:
    ENV_LOADED = False
    logger.warning("python-dotenv paketi bulunamadı. Yüklemek için: pip install python-dotenv")

# scikit-learn için: pip install scikit-learn
try:
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn paketi bulunamadı. Yüklemek için: pip install scikit-learn")

# FAISS için: pip install faiss-cpu veya faiss-gpu
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS paketi bulunamadı. Yüklemek için: pip install faiss-cpu")

# Sabitler
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 500
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200
DEFAULT_TOP_K = 3

# Temel Veri Yapıları
@dataclass
class Document:
    """Metin parçalarını ve meta verisini tutan veri sınıfı."""
    content: str
    metadata: Dict[str, Any] = None
    embedding: Optional[List[float]] = None
    id: Optional[str] = None

    def __post_init__(self):
        # metadata veya id yoksa varsayılan değerler oluştur
        if self.metadata is None:
            self.metadata = {}
        if self.id is None:
            import hashlib
            self.id = hashlib.md5(self.content.encode()).hexdigest()[:8]

# Yardımcı Fonksiyonlar
# ==============

def setup_client(api_key: Optional[str] = None, model: str = DEFAULT_MODEL) -> Tuple[Any, str]:
    """
    LLM API istemcisini ayarlar.

    Args:
        api_key: API anahtarı (None ise ortam değişkeninden alır)
        model: Model adı

    Returns:
        client, model
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    if OPENAI_AVAILABLE:
        client = OpenAI(api_key=api_key)
        return client, model
    else:
        logger.error("OpenAI istemcisi bulunamadı, öncelikle yükleyin.")
        return None, model

# ...fonksiyonların Türkçelendirilmiş halleri ile devam edilecek...
