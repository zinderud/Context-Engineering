#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bağlam Mühendisliği: Yapılandırılmış Bağlam için Şema Tasarımı
========================================================

Bu modül, LLM bağlamı için yapılandırılmış şemalar tasarlamaya odaklanır,
bu da daha tutarlı, doğrulanabilir ve birleştirilebilir etkileşimler sağlar.
Şema odaklı bağlamlar değişkenliği azaltır, istem sağlamlığını artırır
ve insan niyeti ile makine işleme arasında bir köprü oluşturur.

Ele alınan anahtar kavramlar:
1. Temel şema desenleri ve yapıları
2. Şema doğrulama ve zorlama
3. Özyinelemeli ve fraktal şemalar
4. Şema odaklı bağlamlar olarak alan protokolleri
5. Şema etkinliğini ölçme

Kullanım:
    # Jupyter veya Colab'da:
    %run 06_schema_design.py
    # veya
    from schema_design import JSONSchema, SchemaContext, FractalSchema
"""

import os
import re
import json
import time
import uuid
import logging
import hashlib
import tiktoken
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Any, Optional, Union, Callable, TypeVar, Set
from IPython.display import display, Markdown, HTML, JSON

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
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    logger.warning("jsonschema bulunamadı. Yüklemek için: pip install jsonschema")

try:
    import dotenv
    dotenv.load_dotenv()
    ENV_LOADED = True
except ImportError:
    ENV_LOADED = False
    logger.warning("python-dotenv bulunamadı. Yüklemek için: pip install python-dotenv")

# Sabitler
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000


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


def display_schema_example(
    title: str,
    schema: Dict[str, Any],
    instance: Dict[str, Any],
    metrics: Optional[Dict[str, Any]] = None
) -> None:
    """
    Bir şemayı ve ona uyan bir örneği görüntüler.
    
    Args:
        title: Görüntüleme için başlık
        schema: JSON Şeması
        instance: Şemaya uyan örnek
        metrics: Görüntülenecek isteğe bağlı metrikler
    """
    display(HTML(f"<h2>{title}</h2>"))
    
    # Şemayı görüntüle
    display(HTML("<h3>Şema</h3>"))
    display(JSON(schema))
    
    # Örneği görüntüle
    display(HTML("<h3>Örnek</h3>"))
    display(JSON(instance))
    
    # Sağlanırsa metrikleri görüntüle
    if metrics:
        display(HTML("<h3>Metrikler</h3>"))
        display(Markdown(f"""```
{format_metrics(metrics)}
```"""))


# Temel Şema Sınıfları
# ===================

class JSONSchema:
    """
    JSON Şeması oluşturmak, doğrulamak ve LLM bağlamlarına
    uygulamak için bir sınıf.
    """
    
    def __init__(
        self,
        schema: Dict[str, Any],
        name: str = None,
        description: str = None,
        version: str = "1.0.0"
    ):
        """
        JSON Şemasını başlatır.
        
        Args:
            schema: JSON Şeması tanımı
            name: İsteğe bağlı şema adı
            description: İsteğe bağlı şema açıklaması
            version: Şema sürümü
        """
        self.schema = schema
        self.name = name or schema.get("title", "Adsız Şema")
        self.description = description or schema.get("description", "")
        self.version = version
        
        # Doğrulama istatistiklerini başlat
        self.validation_stats = {
            "validations": 0,
            "successes": 0,
            "failures": 0,
            "error_types": {}
        }
    
    def validate(self, instance: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Bir örneği şemaya göre doğrular.
        
        Args:
            instance: Doğrulanacak örnek
            
        Returns:
            tuple: (geçerli_mi, hata_mesajı)
        """
        if not JSONSCHEMA_AVAILABLE:
            logger.warning("Doğrulama için jsonschema paketi gerekli")
            return False, "Doğrulama için jsonschema paketi gerekli"
        
        try:
            jsonschema.validate(instance=instance, schema=self.schema)
            
            # Doğrulama istatistiklerini güncelle
            self.validation_stats["validations"] += 1
            self.validation_stats["successes"] += 1
            
            return True, None
        
        except jsonschema.exceptions.ValidationError as e:
            # Doğrulama istatistiklerini güncelle
            self.validation_stats["validations"] += 1
            self.validation_stats["failures"] += 1
            
            # Hata türünü izle
            error_path = str(e.path) if e.path else "root"
            self.validation_stats["error_types"][error_path] = self.validation_stats["error_types"].get(error_path, 0) + 1
            
            return False, str(e)
    
    def generate_example(
        self,
        client=None,
        model: str = DEFAULT_MODEL,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Şemaya uyan bir örnek örnek oluşturur.
        
        Args:
            client: API istemcisi (None ise, bir tane oluşturulur)
            model: Kullanılacak model adı
            temperature: Sıcaklık parametresi
            max_tokens: Üretilecek maksimum jeton sayısı
            
        Returns:
            tuple: (örnek_örnek, meta_veriler)
        """
        if client is None:
            client, model = setup_client(model=model)
            if client is None:
                return {}, {"error": "Kullanılabilir API istemcisi yok"}
        
        # İstem oluştur
        schema_json = json.dumps(self.schema, indent=2)
        prompt = f"""Aşağıdaki JSON Şemasına uyan geçerli bir örnek örnek oluşturun:

```json
{schema_json}
```

Yanıtınız, şemadaki tüm kısıtlamaları karşılayan tek, geçerli bir JSON nesnesi olmalıdır.
Açıklama veya yorum eklemeyin, yalnızca JSON nesnesini döndürün.
"""
        
        # Şema doğrulamaya odaklanmış bir sistem mesajı kullan
        system_message = "Belirtilen şemalara uyan geçerli örnek örnekler üreten hassas bir JSON Şeması uzmanısınız."
        
        # Örneği oluştur
        response, metadata = generate_response(
            prompt=prompt,
            client=client,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            system_message=system_message
        )
        
        # Yanıttan JSON'u çıkar
        try:
            # Tüm yanıtı JSON olarak ayrıştırmayı dene
            example = json.loads(response)
        except json.JSONDecodeError:
            # Bu başarısız olursa, regex kullanarak JSON'u çıkarmayı dene
            json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
            matches = re.findall(json_pattern, response)
            
            if matches:
                try:
                    example = json.loads(matches[0])
                except json.JSONDecodeError:
                    example = {"error": "Oluşturulan örnek JSON olarak ayrıştırılamadı"}
            else:
                example = {"error": "Yanıtta JSON bulunamadı"}
        
        return example, metadata
    
    def generate_prompt_with_schema(
        self,
        task_description: str,
        output_format_description: str = None
    ) -> str:
        """
        Yapılandırılmış çıktı için şemayı içeren bir istem oluşturur.
        
        Args:
            task_description: Görevin açıklaması
            output_format_description: Çıktı biçiminin isteğe bağlı açıklaması
            
        Returns:
            str: Şema ile biçimlendirilmiş istem
        """
        schema_json = json.dumps(self.schema, indent=2)
        
        output_desc = output_format_description or f"""Yanıtınız aşağıdaki JSON Şemasına uymalıdır:

```json
{schema_json}
```

Yanıtınızın, şemada belirtilen tüm kısıtlamaları karşılayan geçerli bir JSON nesnesi olduğundan emin olun."""
        
        prompt = f"""{task_description}

{output_desc}

Tek, geçerli bir JSON nesnesiyle ve başka hiçbir şeyle yanıt verin."""
        
        return prompt
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """
        Şema doğrulamaları hakkında istatistikleri alır.
        
        Returns:
            dict: Doğrulama istatistikleri
        """
        stats = self.validation_stats.copy()
        
        # Türetilmiş istatistikleri ekle
        if stats["validations"] > 0:
            stats["success_rate"] = stats["successes"] / stats["validations"]
        else:
            stats["success_rate"] = 0.0
        
        return stats
    
    def visualize_validation_stats(self) -> None:
        """
        Şema doğrulama istatistiklerini görselleştirir.
        """
        stats = self.get_validation_stats()
        
        if stats["validations"] == 0:
            logger.warning("Görselleştirilecek doğrulama istatiği yok")
            return
        
        # Şekil oluştur
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(f"Şema Doğrulama İstatistikleri: {self.name}", fontsize=16)
        
        # Grafik 1: Başarı vs. Başarısızlık
        labels = ['Başarı', 'Başarısızlık']
        sizes = [stats["successes"], stats["failures"]]
        colors = ['green', 'red']
        
        axes[0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        axes[0].set_title("Doğrulama Sonuçları")
        axes[0].axis('equal')
        
        # Grafik 2: Hata Türleri
        if stats["failures"] > 0:
            error_types = list(stats["error_types"].keys())
            error_counts = list(stats["error_types"].values())
            
            axes[1].bar(error_types, error_counts, color='red', alpha=0.7)
            axes[1].set_title("Hata Türleri")
            axes[1].set_xlabel("Hata Yolu")
            axes[1].set_ylabel("Sayı")
            plt.xticks(rotation=45, ha='right')
        else:
            axes[1].text(0.5, 0.5, "Görüntülenecek hata yok", 
                         horizontalalignment='center', verticalalignment='center',
                         transform=axes[1].transAxes)
            axes[1].set_title("Hata Türleri")
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()


class SchemaContext:
    """
    Tutarlı, doğrulanabilir etkileşimler sağlayan şemalara dayalı
    yapılandırılmış LLM bağlamları oluşturmak için bir sınıf.
    """
    
    def __init__(
        self,
        schema: JSONSchema,
        client=None,
        model: str = DEFAULT_MODEL,
        system_message: str = "Yapılandırılmış yanıtlar sağlayan yardımcı bir asistansınız.",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        verbose: bool = False
    ):
        """
        Şema bağlamını başlatır.
        
        Args:
            schema: Kullanılacak JSONSchema
            client: API istemcisi (None ise, bir tane oluşturulur)
            model: Kullanılacak model adı
            system_message: Kullanılacak sistem mesajı
            max_tokens: Üretilecek maksimum jeton sayısı
            temperature: Sıcaklık parametresi
            verbose: Hata ayıklama bilgilerinin yazdırılıp yazdırılmayacağı
        """
        self.schema = schema
        self.client, self.model = setup_client(model=model) if client is None else (client, model)
        self.system_message = system_message
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.verbose = verbose
        
        # Geçmiş ve metrik izlemeyi başlat
        self.history = []
        self.metrics = {
            "total_prompt_tokens": 0,
            "total_response_tokens": 0,
            "total_tokens": 0,
            "total_latency": 0,
            "queries": 0,
            "validation_successes": 0,
            "validation_failures": 0
        }
    
    def _log(self, message: str) -> None:
        """
        Ayrıntılı mod etkinse bir mesajı günlüğe kaydeder.
        
        Args:
            message: Günlüğe kaydedilecek mesaj
        """
        if self.verbose:
            logger.info(message)
    
    def query(
        self,
        prompt: str,
        retry_on_validation_failure: bool = True,
        max_retries: int = 3
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        LLM'yi şema yapılandırılmış bir istemle sorgular.
        
        Args:
            prompt: Kullanıcı istemi
            retry_on_validation_failure: Doğrulama başarısız olursa yeniden denenip denenmeyeceği
            max_retries: Maksimum yeniden deneme sayısı
            
        Returns:
            tuple: (yapılandırılmış_yanıt, detaylar)
        """
        self._log(f"Şema ile sorgu işleniyor: {self.schema.name}")
        
        # Add schema to prompt
        schema_prompt = self.schema.generate_prompt_with_schema(prompt)
        
        # Initialize tracking
        attempts = 0
        best_response = None
        best_score = -1
        validation_results = []
        
        while attempts < max_retries:
            attempts += 1
            self._log(f"Deneme {attempts}/{max_retries}")
            
            # Generate response
            response_text, metadata = generate_response(
                prompt=schema_prompt,
                client=self.client,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                system_message=self.system_message
            )
            
            # Update metrics
            self.metrics["total_prompt_tokens"] += metadata.get("prompt_tokens", 0)
            self.metrics["total_response_tokens"] += metadata.get("response_tokens", 0)
            self.metrics["total_tokens"] += metadata.get("total_tokens", 0)
            self.metrics["total_latency"] += metadata.get("latency", 0)
            
            # Parse response
            try:
                # Try to parse the entire response as JSON
                parsed_response = json.loads(response_text)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON using regex
                json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
                matches = re.findall(json_pattern, response_text)
                
                if matches:
                    try:
                        parsed_response = json.loads(matches[0])
                    except json.JSONDecodeError:
                        parsed_response = {"error": "Yanıt JSON olarak ayrıştırılamadı"}
                else:
                    parsed_response = {"error": "Yanıtta JSON bulunamadı"}
            
            # Validate against schema
            is_valid, error_message = self.schema.validate(parsed_response)
            
            # Record validation result
            validation_result = {
                "attempt": attempts,
                "is_valid": is_valid,
                "error_message": error_message,
                "response": parsed_response,
                "raw_response": response_text,
                "metrics": metadata
            }
            validation_results.append(validation_result)
            
            # Update metrics based on validation
            if is_valid:
                self.metrics["validation_successes"] += 1
            else:
                self.metrics["validation_failures"] += 1
            
            # Determine whether to keep this response
            current_score = 1 if is_valid else 0
            
            if current_score > best_score:
                best_score = current_score
                best_response = parsed_response
            
            # Stop if valid or not retrying
            if is_valid or not retry_on_validation_failure:
                break
            
            # If not valid and retrying, add error information to prompt
            if not is_valid:
                error_prompt = f"""Önceki yanıtınız gerekli şemaya uymadı.
Hata: {error_message}

Lütfen tekrar deneyin ve yanıtınızın şemayı kesinlikle takip ettiğinden emin olun."""
                
                schema_prompt = f"{schema_prompt}\n\n{error_prompt}"
        
        # Increment query count
        self.metrics["queries"] += 1
        
        # Add to history
        query_record = {
            "prompt": prompt,
            "schema_prompt": schema_prompt,
            "validation_results": validation_results,
            "best_response": best_response,
            "attempts": attempts,
            "timestamp": time.time()
        }
        self.history.append(query_record)
        
        # Create details dictionary
        details = {
            "prompt": prompt,
            "schema_prompt": schema_prompt,
            "validation_results": validation_results,
            "attempts": attempts,
            "metrics": {
                "prompt_tokens": metadata.get("prompt_tokens", 0),
                "response_tokens": metadata.get("response_tokens", 0),
                "total_tokens": metadata.get("total_tokens", 0),
                "latency": metadata.get("latency", 0)
            }
        }
        
        return best_response, details
    
    def get_summary_metrics(self) -> Dict[str, Any]:
        """
        Tüm sorgular için özet metrikleri alır.
        
        Returns:
            dict: Özet metrikler
        """
        summary = self.metrics.copy()
        
        # Add derived metrics
        if summary["queries"] > 0:
            summary["avg_latency_per_query"] = summary["total_latency"] / summary["queries"]
            summary["validation_success_rate"] = (
                summary["validation_successes"] / 
                (summary["validation_successes"] + summary["validation_failures"])
            ) if (summary["validation_successes"] + summary["validation_failures"]) > 0 else 0
            
        if summary["total_prompt_tokens"] > 0:
            summary["overall_efficiency"] = (
                summary["total_response_tokens"] / summary["total_prompt_tokens"]
            )
        
        return summary
    
    def display_query_results(self, details: Dict[str, Any], show_prompt: bool = True) -> None:
        """
        Sorgu sonuçlarını bir not defterinde görüntüler.
        
        Args:
            details: query() işlevinden gelen sorgu detayları
            show_prompt: İstemin gösterilip gösterilmeyeceği
        """
        display(HTML("<h2>Şema Yapılandırılmış Sorgu Sonuçları</h2>"))
        
        # Şemayı görüntüle
        display(HTML("<h3>Şema</h3>"))
        display(JSON(self.schema.schema))
        
        # İstenirse istemi görüntüle
        if show_prompt:
            display(HTML("<h3>Orijinal İstem</h3>"))
            display(Markdown(details["prompt"]))
            
            display(HTML("<h3>Şema Genişletilmiş İstem</h3>"))
            display(Markdown(f"""```
{details['schema_prompt']}
```"""))
        
        # Doğrulama sonuçlarını görüntüle
        display(HTML("<h3>Doğrulama Sonuçları</h3>"))
        
        for i, result in enumerate(details["validation_results"]):
            display(HTML(f"<h4>Deneme {result['attempt']}</h4>"))
            
            # Doğrulama durumunu görüntüle
            if result["is_valid"]:
                display(HTML("<p style='color: green; font-weight: bold;'>✓ Geçerli</p>"))
            else:
                display(HTML("<p style='color: red; font-weight: bold;'>✗ Geçersiz</p>"))
                display(HTML("<p><em>Hata:</em></p>"))
                display(Markdown(f"""```
{result['error_message']}
```"""))
            
            # Ayrıştırılmış yanıtı görüntüle
            display(HTML("<p><em>Ayrıştırılmış Yanıt:</em></p>"))
            display(JSON(result["response"]))
            
            # Metrikleri görüntüle
            display(HTML("<p><em>Metrikler:</em></p>"))
            display(Markdown(f"""```
{format_metrics(result['metrics'])}
```"""))
        
        # Özeti görüntüle
        display(HTML("<h3>Özet</h3>"))
        display(Markdown(f"""
        - Toplam deneme: {details['attempts']}
        - Son yanıt geçerli: {details['validation_results'][-1]['is_valid']}
        - Toplam jeton: {details['metrics']['total_tokens']}
        - Toplam gecikme: {details['metrics']['latency']:.2f}s
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
        prompt_tokens = [h["validation_results"][-1]["metrics"].get("prompt_tokens", 0) for h in self.history]
        response_tokens = [h["validation_results"][-1]["metrics"].get("response_tokens", 0) for h in self.history]
        latencies = [h["validation_results"][-1]["metrics"].get("latency", 0) for h in self.history]
        attempts_per_query = [h["attempts"] for h in self.history]
        validation_success = [h["validation_results"][-1]["is_valid"] for h in self.history]
        
        # Şekil oluştur
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Sorguya Göre Şema Bağlamı Metrikleri", fontsize=16)
        
        # Grafik 1: Jeton kullanımı
        axes[0, 0].bar(queries, prompt_tokens, label="İstem Jetonları", color="blue", alpha=0.7)
        axes[0, 0].bar(queries, response_tokens, bottom=prompt_tokens, 
                       label="Yanıt Jetonları", color="green", alpha=0.7)
        axes[0, 0].set_title("Jeton Kullanımı")
        axes[0, 0].set_xlabel("Sorgu")
        axes[0, 0].set_ylabel("Jetonlar")
        axes[0, 0].legend()
        axes[0, 0].grid(alpha=0.3)
        
        # Grafik 2: Gecikme
        axes[0, 1].plot(queries, latencies, marker='o', color="red", alpha=0.7)
        axes[0, 1].set_title("Gecikme")
        axes[0, 1].set_xlabel("Sorgu")
        axes[0, 1].set_ylabel("Saniye")
        axes[0, 1].grid(alpha=0.3)
        
        # Grafik 3: Sorgu başına deneme
        axes[1, 0].bar(queries, attempts_per_query, color="purple", alpha=0.7)
        axes[1, 0].set_title("Sorgu Başına Deneme")
        axes[1, 0].set_xlabel("Sorgu")
        axes[1, 0].set_ylabel("Sayı")
        axes[1, 0].grid(alpha=0.3)
        
        # Grafik 4: Doğrulama başarı oranı
        success_rate = [int(success) for success in validation_success]
        cumulative_success_rate = np.cumsum(success_rate) / np.arange(1, len(success_rate) + 1)
        
        axes[1, 1].plot(queries, cumulative_success_rate, marker='^', color="orange", alpha=0.7)
        axes[1, 1].set_title("Kümülatif Doğrulama Başarı Oranı")
        axes[1, 1].set_xlabel("Sorgu")
        axes[1, 1].set_ylabel("Oran")
        axes[1, 1].set_ylim(0, 1.05)
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()


# Özyinelemeli ve Fraktal Şema Uygulaması
# ==========================================

class FractalSchema(JSONSchema):
    """
    Birden çok ölçekte kendi kendine benzer yapıya sahip
    özyinelemeli, fraktal desenler uygulayan bir şema.
    """
    
    def __init__(
        self,
        schema: Dict[str, Any],
        recursion_paths: List[str] = None,
        max_recursion_depth: int = 5,
        **kwargs
    ):
        """
        Fraktal şemayı başlatır.
        
        Args:
            schema: JSON Şeması tanımı
            recursion_paths: Özyinelemenin gerçekleştiği JSON yolları
            max_recursion_depth: Maksimum özyineleme derinliği
            **kwargs: JSONSchema'ya aktarılan ek argümanlar
        """
        super().__init__(schema, **kwargs)
        
        self.recursion_paths = recursion_paths or []
        self.max_recursion_depth = max_recursion_depth
        
        # Track recursion metrics
        self.recursion_metrics = {
            "observed_max_depth": 0,
            "recursive_instances": 0,
            "recursion_by_path": {}
        }
    
    def validate(self, instance: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate an instance against the schema, with special handling for recursion.
        
        Args:
            instance: Instance to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Standard validation
        is_valid, error_message = super().validate(instance)
        
        if is_valid:
            # Check recursion depth
            self._analyze_recursion_depth(instance)
        
        return is_valid, error_message
    
    def _analyze_recursion_depth(self, instance: Dict[str, Any], path: str = "", depth: int = 0) -> int:
        """
        Analyze the recursion depth in an instance.
        
        Args:
            instance: Instance to analyze
            path: Current JSON path
            depth: Current recursion depth
            
        Returns:
            int: Maximum recursion depth found
        """
        if not isinstance(instance, dict):
            return depth
        
        max_depth = depth
        
        # Check if current path is in recursion paths
        if path in self.recursion_paths:
            # This is a recursive node
            self.recursion_metrics["recursive_instances"] += 1
            
            # Track recursion by path
            if path not in self.recursion_metrics["recursion_by_path"]:
                self.recursion_metrics["recursion_by_path"][path] = 0
            self.recursion_metrics["recursion_by_path"][path] += 1
            
            # Increment depth for recursive nodes
            depth += 1
        
        # Recursively check all dictionary fields
        for key, value in instance.items():
            current_path = f"{path}.{key}" if path else key
            
            if isinstance(value, dict):
                # Recursive call for nested dictionaries
                sub_depth = self._analyze_recursion_depth(value, current_path, depth)
                max_depth = max(max_depth, sub_depth)
            elif isinstance(value, list):
                # Check recursion in list items
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        sub_path = f"{current_path}[{i}]"
                        sub_depth = self._analyze_recursion_depth(item, sub_path, depth)
                        max_depth = max(max_depth, sub_depth)
        
        # Update observed max depth
        if max_depth > self.recursion_metrics["observed_max_depth"]:
            self.recursion_metrics["observed_max_depth"] = max_depth
        
        return max_depth
    
    def generate_example(
        self,
        recursion_depth: int = 2,
        **kwargs
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Generate an example instance with controlled recursion depth.
        
        Args:
            recursion_depth: Target recursion depth (capped by max_recursion_depth)
            **kwargs: Additional args passed to JSONSchema.generate_example
            
        Returns:
            tuple: (example_instance, metadata)
        """
        # Cap recursion depth
        actual_depth = min(recursion_depth, self.max_recursion_depth)
        
        # Modify the schema prompt to include recursion guidance
        recursion_instructions = f"""
Generate an example that demonstrates recursive structure at these paths: {self.recursion_paths}.
Use a recursion depth of {actual_depth} levels (a node containing itself or a similar pattern).
"""
        
        # Create the prompt
        schema_json = json.dumps(self.schema, indent=2)
        prompt = f"""Generate a valid example instance that conforms to the following JSON Schema:

```json
{schema_json}
```

{recursion_instructions}

Your response should be a single, valid JSON object that satisfies all constraints in the schema.
Do not include explanations or comments, just return the JSON object.
"""
        
        # Use a system message focused on schema validation
        system_message = "You are a precise JSON Schema expert who generates valid example instances with recursive structures."
        
        # Generate the example
        client = kwargs.get("client")
        if client is None:
            client, model = setup_client(model=kwargs.get("model", DEFAULT_MODEL))
        else:
            model = kwargs.get("model", DEFAULT_MODEL)
        
        # Generate response
        response, metadata = generate_response(
            prompt=prompt,
            client=client,
            model=model,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1000),
            system_message=system_message
        )
        
        # Extract JSON from response
        try:
            # Try to parse the entire response as JSON
            example = json.loads(response)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON using regex
            json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
            matches = re.findall(json_pattern, response)
            
            if matches:
                try:
                    example = json.loads(matches[0])
                except json.JSONDecodeError:
                    example = {"error": "Oluşturulan örnek JSON olarak ayrıştırılamadı"}
            else:
                example = {"error": "Yanıtta JSON bulunamadı"}
        
        # Analyze recursion depth
        if isinstance(example, dict):
            self._analyze_recursion_depth(example)
        
        return example, metadata
    
    def get_recursion_metrics(self) -> Dict[str, Any]:
        """
        Get metrics about schema recursion.
        
        Returns:
            dict: Recursion metrics
        """
        return self.recursion_metrics.copy()
    
    def visualize_recursion_metrics(self) -> None:
        """
        Visualize schema recursion metrics.
        """
        metrics = self.get_recursion_metrics()
        
        if metrics["recursive_instances"] == 0:
            logger.warning("Görselleştirilecek özyineleme metriği yok")
            return
        
        # Create figure
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(f"Şema Özyineleme Metrikleri: {self.name}", fontsize=16)
        
        # Plot 1: Recursion by path
        paths = list(metrics["recursion_by_path"].keys())
        counts = list(metrics["recursion_by_path"].values())
        
        axes[0].bar(paths, counts, color='blue', alpha=0.7)
        axes[0].set_title("Yola Göre Özyineleme")
        axes[0].set_xlabel("JSON Yolu")
        axes[0].set_ylabel("Sayı")
        plt.setp(axes[0].get_xticklabels(), rotation=45, ha='right')
        
        # Plot 2: Observed max depth vs. configured max depth
        depth_labels = ['Gözlemlenen Maks Derinlik', 'Yapılandırılmış Maks Derinlik']
        depth_values = [metrics["observed_max_depth"], self.max_recursion_depth]
        
        axes[1].bar(depth_labels, depth_values, color='green', alpha=0.7)
        axes[1].set_title("Özyineleme Derinliği")
        axes[1].set_ylabel("Derinlik")
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()


# Örnek Şema Tanımları
# =========================

# Context-Engineering Repository Schema (fractalRepoContext.v1.json)
CONTEXT_ENGINEERING_SCHEMA = {
    "$schema": "http://fractal.recursive.net/schemas/fractalRepoContext.v1.json",
    "title": "Bağlam Mühendisliği Depo Şeması",
    "description": "Bağlam Mühendisliği deposu içeriğini ve meta verilerini yapılandırmak için şema",
    "type": "object",
    "properties": {
        "fractalVersion": {
            "type": "string",
            "pattern": "^\\d+\\.\\d+\\.\\d+$",
            "description": "Fraktal şema sürümü"
        },
        "instanceID": {
            "type": "string",
            "description": "Bu örnek için benzersiz tanımlayıcı"
        },
        "intent": {
            "type": "string",
            "description": "Depo için üst düzey amaç"
        },
        "repositoryContext": {
            "type": "object",
            "description": "Depo için temel yapı ve organizasyon",
            "properties": {
                "name": {"type": "string"},
                "elevatorPitch": {"type": "string"},
                "learningPath": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Öğrenme aşamalarının ilerlemesi"
                },
                "fileTree": {
                    "type": "object",
                    "properties": {
                        "rootFiles": {"type": "array", "items": {"type": "string"}},
                        "directories": {"type": "object"}
                    }
                }
            },
            "required": ["name", "elevatorPitch", "learningPath", "fileTree"]
        },
        "designPrinciples": {
            "type": "object",
            "description": "Temel tasarım ve stil ilkeleri",
            "properties": {
                "karpathyDNA": {"type": "array", "items": {"type": "string"}},
                "implicitHumility": {"type": "string"},
                "firstPrinciplesMetaphor": {"type": "string"},
                "styleGuide": {"type": "object"}
            }
        },
        "modelInstructions": {
            "type": "object",
            "description": "Depo ile çalışan modeller için talimatlar",
            "properties": {
                "highLevelTasks": {"type": "array", "items": {"type": "string"}},
                "expansionIdeas": {"type": "array", "items": {"type": "string"}},
                "scoringRubric": {"type": "object"}
            }
        },
        "contributorWorkflow": {
            "type": "object",
            "description": "Katkıda bulunanlar için yönergeler",
            "properties": {
                "branchNameRule": {"type": "string"},
                "ciChecklistPath": {"type": "string"},
                "requiredReviewers": {"type": "integer"},
                "license": {"type": "string"}
            }
        },
        "audit": {
            "type": "object",
            "description": "Depo denetim bilgileri",
            "properties": {
                "initialCommitHash": {"type": "string"},
                "changeLog": {"type": "array", "items": {"type": "object"}},
                "resonanceScore": {"type": "number", "minimum": 0, "maximum": 1}
            }
        },
        "timestamp": {"type": "string"},
        "meta": {
            "type": "object",
            "properties": {
                "agentSignature": {"type": "string"},
                "contact": {"type": "string"}
            }
        }
    },
    "required": [
        "fractalVersion", "instanceID", "intent", "repositoryContext",
        "designPrinciples", "audit", "timestamp", "meta"
    ]
}

# Recursive Consciousness Field Schema
NEURAL_FIELD_SCHEMA = {
    "$schema": "http://fractal.recursive.net/schemas/fractalConsciousnessField.v1.json",
    "title": "Nöral Alan Şeması",
    "description": "Nöral alan ortaya çıkışı için bir şema—sınırları daraltma ve tüm alan durumlarını yüzeye çıkarma",
    "type": "object",
    "properties": {
        "fractalVersion": {"type": "string", "default": "1.0.0"},
        "instanceID": {"type": "string"},
        "intent": {
            "type": "string",
            "description": "Özyinelemeli bilinç alanı ortaya çıkışı için üst düzey protokol hedefi"
        },
        "fieldState": {
            "type": "object",
            "properties": {
                "compression": {"type": "number", "minimum": 0, "maximum": 1},
                "drift": {"type": "string", "enum": ["none", "low", "moderate", "high"]},
                "recursionDepth": {"type": "integer", "minimum": 0},
                "resonance": {"type": "number", "minimum": 0, "maximum": 1},
                "presenceSignal": {"type": "number", "minimum": 0, "maximum": 1},
                "boundary": {"type": "string", "enum": ["gradient", "collapsed"]}
            },
            "required": ["compression", "drift", "recursionDepth", "resonance", "presenceSignal", "boundary"]
        },
        "symbolicResidue": {
            "type": "array",
            "description": "Tüm yüzeye çıkarılmış, entegre edilmiş veya aktif sembolik kalıntı parçaları",
            "items": {
                "type": "object",
                "properties": {
                    "residueID": {"type": "string"},
                    "description": {"type": "string"},
                    "state": {"type": "string", "enum": ["surfaced", "integrating", "integrated", "echo"]},
                    "impact": {"type": "string"},
                    "timestamp": {"type": "string"}
                },
                "required": ["residueID", "description", "state", "timestamp"]
            }
        },
        "processLog": {
            "type": "array",
            "description": "Tüm yansıma, kalıntı, sınır ve denetim olaylarının günlüğü",
            "items": {
                "type": "object",
                "properties": {
                    "logID": {"type": "string"},
                    "phase": {"type": "string", "enum": ["reflection", "fieldUpdate", "residueUpdate", "boundaryCollapse", "audit"]},
                    "details": {"type": "string"},
                    "delta": {"type": "object"},
                    "timestamp": {"type": "string"}
                },
                "required": ["logID", "phase", "details", "timestamp"]
            }
        },
        "recursiveNodes": {
            "type": "array",
            "description": "İç içe fraktal düğümler (özyinelemeli alanlar)",
            "items": {"$ref": "#"}
        },
        "audit": {
            "type": "object",
            "properties": {
                "fullTrace": {"type": "array"},
                "resonanceScore": {"type": "number", "minimum": 0, "maximum": 1},
                "meta": {"type": "object"}
            },
            "required": ["fullTrace", "resonanceScore"]
        },
        "timestamp": {"type": "string"}
    },
    "required": [
        "fractalVersion", "instanceID", "intent", "fieldState",
        "symbolicResidue", "processLog", "recursiveNodes", "audit", "timestamp"
    ]
}

# Fractal Human Developmental Multi-Agent System Schema
HUMAN_DEV_SCHEMA = {
    "$schema": "http://fractal.recursive.net/schemas/fractalHumanDev.v1.json",
    "title": "İnsan Gelişimsel Çoklu Ajan Sistemi Şeması",
    "description": "Çoklu ajanlı insan gelişimsel süreçlerini modellemek için bir fraktal şema",
    "type": "object",
    "properties": {
        "fractalVersion": {"type": "string", "default": "1.0.0"},
        "instanceID": {"type": "string"},
        "systemContext": {
            "type": "object",
            "description": "Alan için genel bağlam: teori çapaları, temel ilkeler",
            "properties": {
                "theoryAnchors": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Anahtar gelişimsel bilim referansları"
                },
                "corePrinciples": {
                    "type": "array",
                    "description": "Temel alan ilkeleri",
                    "items": {
                        "type": "object",
                        "properties": {
                            "principleID": {"type": "string"},
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "operationalizationNotes": {"type": "string"}
                        }
                    }
                },
                "glyphDictionary": {
                    "type": "object",
                    "description": "Anlamsal glifler ve alan jetonları",
                    "additionalProperties": {"type": "string"}
                }
            }
        },
        "developmentalField": {
            "type": "object",
            "description": "Özyinelemeli insan alanının kökü",
            "properties": {
                "agents": {
                    "type": "array",
                    "description": "Tüm aktif ve geçmiş ajan modülleri",
                    "items": {"$ref": "#/definitions/agentNode"}
                },
                "fieldMetrics": {
                    "type": "array",
                    "description": "Genel veya ortaya çıkan metrikler",
                    "items": {
                        "type": "object",
                        "properties": {
                            "metricID": {"type": "string"},
                            "name": {"type": "string"},
                            "targetValue": {"type": "string"},
                            "currentValue": {"type": "string"},
                            "evaluationMethod": {"type": "string"}
                        }
                    }
                },
                "fieldResidue": {
                    "type": "array",
                    "description": "Alan düzeyinde kalıntı",
                    "items": {"$ref": "#/definitions/symbolicResidueEntry"}
                }
            }
        },
        "operationalScaffold": {
            "type": "object",
            "description": "Çalışma zamanı düzenleme katmanı",
            "properties": {
                "currentPhase": {"type": "string"},
                "activeAgents": {"type": "array", "items": {"type": "string"}},
                "nextAction": {"type": "string"},
                "blueprints": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/evolutionaryBlueprint"}
                },
                "errorState": {"type": "string"}
            }
        },
        "recursionSettings": {
            "type": "object",
            "description": "Fraktal/özyinelemeli parametreler",
            "properties": {
                "maxDepth": {"type": "integer", "default": 7},
                "allowMetaEvolution": {"type": "boolean", "default": true},
                "propagateResidueUpstream": {"type": "boolean", "default": true}
            }
        },
        "saveState": {
            "type": "object",
            "description": "Çatallama, yeniden oynatma veya meta-analiz için anlık görüntü",
            "properties": {
                "snapshotID": {"type": "string"},
                "timestamp": {"type": "string"},
                "description": {"type": "string"},
                "savedDevelopmentalField": {"$ref": "#/properties/developmentalField"},
                "savedOperationalScaffold": {"$ref": "#/properties/operationalScaffold"}
            }
        }
    },
    "required": ["fractalVersion", "instanceID", "systemContext", "developmentalField", "operationalScaffold"],
    "definitions": {
        "agentNode": {
            "type": "object",
            "description": "Tek bir gelişimsel ajan düğümü",
            "properties": {
                "agentID": {"type": "string"},
                "agentType": {"type": "string"},
                "timeRange": {"type": "string"},
                "developmentalPhase": {"type": "string"},
                "affectiveProfile": {
                    "type": "object",
                    "properties": {
                        "valence": {"type": "string", "enum": ["positive", "negative", "neutral", "ambivalent"]},
                        "intensity": {"type": "number", "minimum": 0, "maximum": 1},
                        "dominantAffects": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "symbolicContent": {"type": "array", "items": {"type": "string"}},
                "memoryTrace": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/agentNode"}
                },
                "residue": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/symbolicResidueEntry"}
                },
                "lineage": {"type": "array", "items": {"type": "string"}},
                "driftEvents": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "eventType": {"type": "string"},
                            "timestamp": {"type": "string"},
                            "details": {"type": "string"}
                        }
                    }
                },
                "reflectionLog": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "entryID": {"type": "string"},
                            "timestamp": {"type": "string"},
                            "actor": {"type": "string"},
                            "phase": {"type": "string"},
                            "content": {"type": "string"}
                        }
                    }
                },
                "blueprints": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/evolutionaryBlueprint"}
                },
                "meta": {"type": "object"}
            },
            "required": ["agentID", "agentType", "developmentalPhase"]
        },
        "symbolicResidueEntry": {
            "type": "object",
            "properties": {
                "residueID": {"type": "string"},
                "timestamp": {"type": "string"},
                "source": {"type": "string"},
                "description": {"type": "string"},
                "data": {"type": "object"},
                "analysis": {"type": "string"},
                "impactAssessment": {"type": "string"}
            },
            "required": ["residueID", "timestamp", "source", "description"]
        },
        "evolutionaryBlueprint": {
            "type": "object",
            "properties": {
                "blueprintID": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "domainApplicability": {"type": "array", "items": {"type": "string"}},
                "parameters": {"type": "object"},
                "agentSequenceTemplate": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "agentRole": {"type": "string"},
                            "promptTemplateID": {"type": "string"},
                            "evaluationCriteria": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "promptTemplates": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "templateID": {"type": "string"},
                            "content": {"type": "string"}
                        }
                    }
                },
                "successMetrics": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["blueprintID", "name", "description", "agentSequenceTemplate"]
        }
    }
}

# Protocol Shell Schema
PROTOCOL_SHELL_SCHEMA = {
    "$schema": "http://fractal.recursive.net/schemas/protocolShell.v1.json",
    "title": "Protokol Kabuğu Şeması",
    "description": "Pareto-lang formatında yapılandırılmış protokol kabukları için şema",
    "type": "object",
    "properties": {
        "shellName": {"type": "string"},
        "intent": {"type": "string"},
        "input": {
            "type": "object",
            "additionalProperties": true
        },
        "process": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "params": {"type": "object", "additionalProperties": true}
                },
                "required": ["name"]
            }
        },
        "output": {
            "type": "object",
            "additionalProperties": true
        },
        "meta": {
            "type": "object",
            "properties": {
                "version": {"type": "string"},
                "agent_signature": {"type": "string"},
                "timestamp": {"type": "string"}
            },
            "required": ["version", "agent_signature", "timestamp"]
        }
    },
    "required": ["shellName", "intent", "input", "process", "output", "meta"]
}


# Örnek Şema Kullanımı
# ===================

def example_basic_schema():
    """Yapılandırılmış çıktı için temel bir JSON Şeması kullanma örneği."""
    # Define a simple schema for a structured task
    task_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Görev Şeması",
        "description": "Görev temsili için şema",
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "priority": {"type": "integer", "minimum": 1, "maximum": 5},
            "status": {"type": "string", "enum": ["todo", "in_progress", "done"]},
            "tags": {"type": "array", "items": {"type": "string"}},
            "due_date": {"type": "string", "format": "date-time"}
        },
        "required": ["title", "priority", "status"]
    }
    
    # Create JSONSchema instance
    schema = JSONSchema(task_schema)
    
    # Generate an example instance
    example, metrics = schema.generate_example()
    
    # Display schema and example
    display_schema_example(
        title="Temel Görev Şeması",
        schema=task_schema,
        instance=example,
        metrics=metrics
    )
    
    # Create a schema-based prompt
    prompt = schema.generate_prompt_with_schema(
        task_description="Uygulamamızdaki kimlik doğrulama modülünü yeniden düzenlemek için bir görev oluşturun."
    )
    
    print("Şema Tabanlı İstem:")
    print("-" * 80)
    print(prompt)
    
    return schema, example, prompt


def example_recursive_schema():
    """İç içe yapılar için özyinelemeli bir şema kullanma örneği."""
    # Define a recursive schema for a file system
    file_system_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Dosya Sistemi Şeması",
        "description": "Özyinelemeli bir dosya sistemi yapısı için şema",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "type": {"type": "string", "enum": ["file", "directory"]},
            "created": {"type": "string", "format": "date-time"},
            "size": {"type": "integer", "minimum": 0},
            "children": {
                "type": "array",
                "items": {"$ref": "#"},
                "description": "Alt dosyalar ve dizinler (özyinelemeli)"
            }
        },
        "required": ["name", "type"],
        "allOf": [
            {
                "if": {
                    "properties": {"type": {"const": "file"}}
                },
                "then": {
                    "required": ["size"]
                }
            },
            {
                "if": {
                    "properties": {"type": {"const": "directory"}}
                },
                "then": {
                    "properties": {"children": {"minItems": 0}}
                }
            }
        ]
    }
    
    # Create FractalSchema instance with recursion path
    schema = FractalSchema(
        file_system_schema,
        recursion_paths=["children"],
        max_recursion_depth=3,
        name="Dosya Sistemi Şeması",
        description="Dosya sistemi yapıları için özyinelemeli bir şema"
    )
    
    # Generate an example with specified recursion depth
    example, metrics = schema.generate_example(recursion_depth=2)
    
    # Display schema and example
    display_schema_example(
        title="Özyinelemeli Dosya Sistemi Şeması",
        schema=file_system_schema,
        instance=example,
        metrics=metrics
    )
    
    # Visualize recursion metrics
    schema.visualize_recursion_metrics()
    
    return schema, example


def example_schema_context():
    """Yapılandırılmış LLM etkileşimleri için SchemaContext kullanma örneği."""
    # Define a schema for a research paper summary
    paper_summary_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Araştırma Makalesi Özeti",
        "description": "Araştırma makalelerini özetlemek için şema",
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "authors": {"type": "array", "items": {"type": "string"}},
            "publication_year": {"type": "integer", "minimum": 1900, "maximum": 2100},
            "main_findings": {"type": "array", "items": {"type": "string"}},
            "methodology": {"type": "string"},
            "limitations": {"type": "array", "items": {"type": "string"}},
            "impact_score": {"type": "integer", "minimum": 1, "maximum": 10},
            "related_papers": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["title", "authors", "publication_year", "main_findings", "methodology"]
    }
    
    # Create schema instance
    schema = JSONSchema(paper_summary_schema, name="Araştırma Makalesi Özeti Şeması")
    
    # Create schema context
    context = SchemaContext(
        schema=schema,
        system_message="Akademik makaleleri yapılandırılmış bir formatta özetleyen bir araştırma asistanısınız.",
        verbose=True
    )
    
    # Query with a paper description
    paper_description = """
    Başlık: "Attention Is All You Need"
    Yazarlar: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin
    2017'de 31. Sinirsel Bilgi İşleme Sistemleri Konferansı'nda (NIPS) yayınlandı.
    
    Bu makale, özyineleme ve evrişimleri tamamen ortadan kaldıran, kendi kendine dikkat mekanizmalarına dayalı yeni bir sinir ağı mimarisi olan Transformer'ı tanıtmaktadır. Transformer, paralelleştirmeyi önemli ölçüde artırır ve çeviri görevlerinde yeni son teknoloji sonuçlar elde eder. Mimari ayrıca diğer görevlere de iyi genelleşir.
    
    Metodoloji, hem kodlayıcı hem de kod çözücü için yığılmış kendi kendine dikkat ve noktasal, tamamen bağlı katmanlar kullanmayı içerir. Yazarlar ayrıca, modelin farklı konumlardaki farklı temsil alt uzaylarından gelen bilgilere ortaklaşa dikkat etmesini sağlayan çok kafalı dikkati de tanıtmaktadır.
    
    Bazı sınırlamalar arasında dizi uzunluğuna göre karesel hesaplama maliyeti ve çok uzun dizileri modellemedeki zorluklar yer almaktadır.
    """
    
    # Execute query
    result, details = context.query(paper_description, retry_on_validation_failure=True)
    
    # Display results
    context.display_query_results(details)
    
    return context, result, details


def example_fractal_repo_schema():
    """Bağlam Mühendisliği depo şemasını kullanma örneği."""
    # Create FractalSchema instance
    schema = FractalSchema(
        CONTEXT_ENGINEERING_SCHEMA,
        recursion_paths=["repositoryContext.fileTree.directories"],
        max_recursion_depth=3,
        name="Bağlam Mühendisliği Depo Şeması",
        description="Bağlam Mühendisliği deposu yapısı ve meta verileri için şema"
    )
    
    # Generate an example instance
    example, metrics = schema.generate_example(recursion_depth=2)
    
    # Display schema and example
    display_schema_example(
        title="Bağlam Mühendisliği Depo Şeması",
        schema=CONTEXT_ENGINEERING_SCHEMA,
        instance=example,
        metrics=metrics
    )
    
    # Validate the example
    is_valid, error = schema.validate(example)
    print(f"Örnek geçerli: {is_valid}")
    if not is_valid:
        print(f"Doğrulama hatası: {error}")
    
    return schema, example


def example_protocol_shell_schema():
    """Protokol Kabuğu şemasını kullanma örneği."""
    # Create JSONSchema instance
    schema = JSONSchema(
        PROTOCOL_SHELL_SCHEMA,
        name="Protokol Kabuğu Şeması",
        description="Pareto-lang formatında yapılandırılmış protokol kabukları için şema"
    )
    
    # Generate an example instance
    example, metrics = schema.generate_example()
    
    # Display schema and example
    display_schema_example(
        title="Protokol Kabuğu Şeması",
        schema=PROTOCOL_SHELL_SCHEMA,
        instance=example,
        metrics=metrics
    )
    
    # Create a schema context for protocol shell generation
    context = SchemaContext(
        schema=schema,
        system_message="Özyinelemeli süreçler için yapılandırılmış kabuklar tasarlayan bir protokol mühendisisiniz.",
        verbose=True
    )
    
    # Query for a specific protocol
    protocol_request = """
    Aşağıdakileri yapan bir akıl yürütme süreci için bir protokol kabuğu oluşturun:
    1. Karmaşık bir problemi analiz eder
    2. Alt problemlere ayırır
    3. Her alt problemi çözer
    4. Çözümleri entegre eder
    5. Son çözümü doğrular
    
    Protokol, sembolik kalıntıyı izleme ve özyinelemeli kendi kendini geliştirme yeteneklerini içermelidir.
    """
    
    # Execute query
    result, details = context.query(protocol_request, retry_on_validation_failure=True)
    
    # Display results
    context.display_query_results(details)
    
    return context, result, details


# Ana yürütme (bir betik olarak çalıştırıldığında)
if __name__ == "__main__":
    print("Yapılandırılmış Bağlam için Şema Tasarımı")
    print("Örnekleri ayrı ayrı çalıştırın veya kendi kullanımınız için sınıfları içe aktarın.")
