#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bağlam Mühendisliği: Kendi Kendini Geliştiren Bağlamlar için Özyinelemeli Desenler
==================================================================

Bu modül, bağlam mühendisliğindeki özyinelemeli desenleri araştırır - LLM'lerin
kendi bağlamlarını genişletmelerini, iyileştirmelerini ve geliştirmelerini sağlayan yaklaşımlar.
Bu desenler, istemler içinde geri bildirim döngüleri oluşturarak yinelemeli iyileştirme,
kendi kendini doğrulama ve açıkça kodlananın ötesinde ortaya çıkan yetenekler sağlar.

Ele alınan anahtar kavramlar:
1. Temel özyinelemeli desenler (kendi üzerine düşünme, önyükleme)
2. Özyinelemeli çerçeveler olarak alan protokolleri ve kabukları
3. Sembolik kalıntı ve durum izleme
4. Sınır çöküşü ve gradyan sistemleri
5. Ortaya çıkan çekiciler ve rezonans

Kullanım:
    # Jupyter veya Colab'da:
    %run 07_recursive_patterns.py
    # veya
    from recursive_patterns import RecursivePattern, FieldProtocol, SymbolicResidue
"""

import os
import re
import json
import time
import uuid
import hashlib
import logging
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


def display_recursive_pattern(
    pattern_name: str,
    input_data: Any,
    iterations: List[Dict[str, Any]],
    final_output: Any,
    metrics: Dict[str, Any] = None
) -> None:
    """
    Özyinelemeli bir desenin yürütülmesini bir not defterinde görüntüler.
    
    Args:
        pattern_name: Özyinelemeli desenin adı
        input_data: Başlangıç girdi verileri
        iterations: Yineleme verileri listesi
        final_output: Son çıktı verileri
        metrics: İsteğe bağlı metrikler sözlüğü
    """
    display(HTML(f"<h2>Özyinelemeli Desen: {pattern_name}</h2>"))
    
    # Girdiyi görüntüle
    display(HTML("<h3>Başlangıç Girdisi</h3>"))
    if isinstance(input_data, str):
        display(Markdown(input_data))
    else:
        display(Markdown(f"```json
{json.dumps(input_data, indent=2)}
```"))
    
    # Yinelemeleri görüntüle
    display(HTML("<h3>Özyinelemeli Yinelemeler</h3>"))
    
    for i, iteration in enumerate(iterations):
        display(HTML(f"<h4>Yineleme {i+1}</h4>"))
        
        # Varsa istemi görüntüle
        if "prompt" in iteration:
            display(HTML("<p><em>İstem:</em></p>"))
            display(Markdown(f"```
{iteration['prompt']}
```"))
        
        # Varsa yanıtı görüntüle
        if "response" in iteration:
            display(HTML("<p><em>Yanıt:</em></p>"))
            display(Markdown(iteration["response"]))
        
        # Varsa durumu görüntüle
        if "state" in iteration:
            display(HTML("<p><em>Durum:</em></p>"))
            if isinstance(iteration["state"], str):
                display(Markdown(iteration["state"]))
            else:
                display(Markdown(f"```json
{json.dumps(iteration['state'], indent=2)}
```"))
        
        # Varsa metrikleri görüntüle
        if "metrics" in iteration:
            display(HTML("<p><em>Metrikler:</em></p>"))
            display(Markdown(f"```
{format_metrics(iteration['metrics'])}
```"))
    
    # Son çıktıyı görüntüle
    display(HTML("<h3>Son Çıktı</h3>"))
    if isinstance(final_output, str):
        display(Markdown(final_output))
    else:
        display(Markdown(f"```json
{json.dumps(final_output, indent=2)}
```"))
    
    # Genel metrikleri görüntüle
    if metrics:
        display(HTML("<h3>Genel Metrikler</h3>"))
        display(Markdown(f"```
{format_metrics(metrics)}
```"))


# Özyinelemeli Desenler için Temel Sınıflar
# =================================

class RecursivePattern:
    """
    Özyinelemeli desenler için temel sınıf - LLM'lerin
    kendi bağlamlarını genişletmelerini, iyileştirmelerini ve geliştirmelerini sağlayan yaklaşımlar.
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        client=None,
        model: str = DEFAULT_MODEL,
        system_message: str = "Yardımcı bir asistansınız.",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        max_iterations: int = 5,
        verbose: bool = False
    ):
        """
        Özyinelemeli deseni başlatır.
        
        Args:
            name: Desen adı
            description: Desen açıklaması
            client: API istemcisi (None ise, bir tane oluşturulur)
            model: Kullanılacak model adı
            system_message: Kullanılacak sistem mesajı
            max_tokens: Üretilecek maksimum jeton sayısı
            temperature: Sıcaklık parametresi
            max_iterations: Maksimum özyinelemeli yineleme sayısı
            verbose: Hata ayıklama bilgilerinin yazdırılıp yazdırılmayacağı
        """
        self.name = name
        self.description = description
        self.client, self.model = setup_client(model=model) if client is None else (client, model)
        self.system_message = system_message
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.max_iterations = max_iterations
        self.verbose = verbose
        
        # Durumu başlat
        self.state = {}
        self.iterations = []
        
        # Metrik izlemeyi başlat
        self.metrics = {
            "total_prompt_tokens": 0,
            "total_response_tokens": 0,
            "total_tokens": 0,
            "total_latency": 0,
            "iterations": 0
        }
    
    def _log(self, message: str) -> None:
        """
        Ayrıntılı mod etkinse bir mesajı günlüğe kaydeder.
        
        Args:
            message: Günlüğe kaydedilecek mesaj
        """
        if self.verbose:
            logger.info(message)
    
    def _generate_recursive_prompt(self, iteration: int, **kwargs) -> str:
        """
        Özyinelemeli desenin mevcut yinelemesi için bir istem oluşturur.
        
        Args:
            iteration: Mevcut yineleme numarası
            **kwargs: İstem oluşturma için ek değişkenler
            
        Returns:
            str: Oluşturulan istem
        """
        # Bu bir yer tutucudur - alt sınıflar bunu uygulamalıdır
        raise NotImplementedError("Alt sınıflar _generate_recursive_prompt uygulamalıdır")
    
    def _call_llm(
        self,
        prompt: str,
        custom_system_message: Optional[str] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        LLM'yi çağırır ve metrikleri günceller.
        
        Args:
            prompt: Gönderilecek istem
            custom_system_message: Sistem mesajını geçersiz kıl (isteğe bağlı)
            
        Returns:
            tuple: (yanıt_metni, meta_veriler)
        """
        system_msg = custom_system_message if custom_system_message else self.system_message
        
        response, metadata = generate_response(
            prompt=prompt,
            client=self.client,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            system_message=system_msg
        )
        
        # Metrikleri güncelle
        self.metrics["total_prompt_tokens"] += metadata.get("prompt_tokens", 0)
        self.metrics["total_response_tokens"] += metadata.get("response_tokens", 0)
        self.metrics["total_tokens"] += metadata.get("total_tokens", 0)
        self.metrics["total_latency"] += metadata.get("latency", 0)
        self.metrics["iterations"] += 1
        
        return response, metadata
    
    def _process_response(self, response: str, iteration: int) -> Any:
        """
        Mevcut yineleme için LLM yanıtını işler.
        
        Args:
            response: LLM yanıt metni
            iteration: Mevcut yineleme numarası
            
        Returns:
            Any: İşlenmiş çıktı
        """
        # Varsayılan uygulama yanıtı olduğu gibi döndürür
        return response
    
    def _update_state(
        self,
        iteration: int,
        prompt: str,
        response: str,
        processed_output: Any,
        metrics: Dict[str, Any]
    ) -> None:
        """
        Mevcut yineleme sonuçlarına göre durumu günceller.
        
        Args:
            iteration: Mevcut yineleme numarası
            prompt: LLM'ye gönderilen istem
            response: Ham LLM yanıtı
            processed_output: İşlenmiş yineleme çıktısı
            metrics: Yineleme metrikleri
        """
        # Yineleme kaydı oluştur
        iteration_record = {
            "iteration": iteration,
            "prompt": prompt,
            "response": response,
            "output": processed_output,
            "state": self.state.copy(),
            "metrics": metrics,
            "timestamp": time.time()
        }
        
        # Yineleme geçmişine ekle
        self.iterations.append(iteration_record)
        
        # Mevcut durumu güncelle
        self.state["current_iteration"] = iteration
        self.state["last_prompt"] = prompt
        self.state["last_response"] = response
        self.state["last_output"] = processed_output
    
    def _should_continue(self, iteration: int, current_output: Any) -> bool:
        """
        Özyinelemeli desene devam edilip edilmeyeceğini belirler.
        
        Args:
            iteration: Mevcut yineleme numarası
            current_output: Mevcut yineleme çıktısı
            
        Returns:
            bool: Desen devam etmeliyse True, aksi takdirde False
        """
        # Varsayılan uygulama, max_iterations'a ulaşılana kadar devam eder
        return iteration < self.max_iterations
    
    def run(self, input_data: Any) -> Tuple[Any, List[Dict[str, Any]]]:
        """
        Özyinelemeli deseni verilen girdiyle çalıştırır.
        
        Args:
            input_data: Başlangıç girdi verileri
            
        Returns:
            tuple: (son_çıktı, yineleme_geçmişi)
        """
        # Durumu girdiyle başlat
        self.state = {"input": input_data}
        self.iterations = []
        
        self._log(f"Özyinelemeli desen başlatılıyor: {self.name}")
        
        # Başlangıç çıktısı girdidir
        current_output = input_data
        iteration = 0
        
        # Özyinelemeli yineleme döngüsü
        while True:
            iteration += 1
            self._log(f"Yineleme {iteration}/{self.max_iterations}")
            
            # Mevcut yineleme için istem oluştur
            prompt = self._generate_recursive_prompt(
                iteration=iteration,
                input=input_data,
                current_output=current_output,
                **self.state
            )
            
            # LLM'yi çağır
            response, metrics = self._call_llm(prompt)
            
            # Yanıtı işle
            processed_output = self._process_response(response, iteration)
            
            # Durumu güncelle
            self._update_state(iteration, prompt, response, processed_output, metrics)
            
            # Mevcut çıktıyı güncelle
            current_output = processed_output
            
            # Devam edip etmeyeceğimizi kontrol et
            if not self._should_continue(iteration, current_output):
                self._log(f"Yineleme {iteration}'de durduruluyor")
                break
        
        return current_output, self.iterations
    
    def get_summary_metrics(self) -> Dict[str, Any]:
        """
        Tüm yinelemeler için özet metrikleri alır.
        
        Returns:
            dict: Özet metrikler
        """
        summary = self.metrics.copy()
        
        # Türetilmiş metrikleri ekle
        if summary["iterations"] > 0:
            summary["avg_latency_per_iteration"] = summary["total_latency"] / summary["iterations"]
            
        if summary["total_prompt_tokens"] > 0:
            summary["overall_efficiency"] = (
                summary["total_response_tokens"] / summary["total_prompt_tokens"]
            )
        
        return summary
    
    def display_execution(self) -> None:
        """Özyinelemeli desen yürütmesini bir not defterinde görüntüler."""
        display_recursive_pattern(
            pattern_name=self.name,
            input_data=self.state.get("input"),
            iterations=self.iterations,
            final_output=self.state.get("last_output"),
            metrics=self.get_summary_metrics()
        )
    
    def visualize_metrics(self) -> None:
        """
        Yinelemeler arasında metriklerin görselleştirilmesini oluşturur.
        """
        if not self.iterations:
            logger.warning("Görselleştirilecek yineleme yok")
            return
        
        # Çizim için verileri çıkar
        iterations = list(range(1, len(self.iterations) + 1))
        prompt_tokens = [it["metrics"].get("prompt_tokens", 0) for it in self.iterations]
        response_tokens = [it["metrics"].get("response_tokens", 0) for it in self.iterations]
        latencies = [it["metrics"].get("latency", 0) for it in self.iterations]
        efficiencies = [it["metrics"].get("token_efficiency", 0) for it in self.iterations]
        
        # Şekil oluştur
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f"Özyinelemeli Desen Metrikleri: {self.name}", fontsize=16)
        
        # Grafik 1: Jeton kullanımı
        axes[0, 0].bar(iterations, prompt_tokens, label="İstem Jetonları", color="blue", alpha=0.7)
        axes[0, 0].bar(iterations, response_tokens, bottom=prompt_tokens, 
                       label="Yanıt Jetonları", color="green", alpha=0.7)
        axes[0, 0].set_title("Yinelemeye Göre Jeton Kullanımı")
        axes[0, 0].set_xlabel("Yineleme")
        axes[0, 0].set_ylabel("Jetonlar")
        axes[0, 0].legend()
        axes[0, 0].grid(alpha=0.3)
        
        # Grafik 2: Gecikme
        axes[0, 1].plot(iterations, latencies, marker='o', color="red", alpha=0.7)
        axes[0, 1].set_title("Yinelemeye Göre Gecikme")
        axes[0, 1].set_xlabel("Yineleme")
        axes[0, 1].set_ylabel("Saniye")
        axes[0, 1].grid(alpha=0.3)
        
        # Grafik 3: Jeton verimliliği
        axes[1, 0].plot(iterations, efficiencies, marker='s', color="purple", alpha=0.7)
        axes[1, 0].set_title("Jeton Verimliliği (Yanıt/İstem)")
        axes[1, 0].set_xlabel("Yineleme")
        axes[1, 0].set_ylabel("Oran")
        axes[1, 0].grid(alpha=0.3)
        
        # Grafik 4: Kümülatif jetonlar
        cumulative_tokens = np.cumsum([it["metrics"].get("total_tokens", 0) for it in self.iterations])
        axes[1, 1].plot(iterations, cumulative_tokens, marker='^', color="orange", alpha=0.7)
        axes[1, 1].set_title("Kümülatif Jeton Kullanımı")
        axes[1, 1].set_xlabel("Yineleme")
        axes[1, 1].set_ylabel("Toplam Jeton")
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()


# Özyinelemeli Desen Uygulamaları
# ===============================

class SelfReflection(RecursivePattern):
    """
    Meta-bilişsel süreçler aracılığıyla kendi üzerine düşünme ve
    sürekli iyileştirme uygulayan özyinelemeli bir desen.
    """
    
    def __init__(
        self,
        reflection_template: str = "Önceki yanıtınızı analiz edin:\n\n{previous_response}\n\nGüçlü ve zayıf yönleri belirleyin. Orijinal sorguyu daha iyi ele almak için yanıtınızı nasıl geliştirebilirsiniz:\n\n{original_query}",
        improvement_threshold: float = 0.8,
        **kwargs
    ):
        """
        Kendi üzerine düşünme desenini başlatır.
        
        Args:
            reflection_template: Yansıma istemleri için şablon
            improvement_threshold: İyileştirmeye dayalı durdurma eşiği
            **kwargs: RecursivePattern'a aktarılan ek argümanlar
        """
        name = kwargs.pop("name", "Kendi Üzerine Düşünme Deseni")
        description = kwargs.pop("description", "Meta-bilişsel süreçler aracılığıyla sürekli iyileştirme için bir desen")
        
        super().__init__(name=name, description=description, **kwargs)
        
        self.reflection_template = reflection_template
        self.improvement_threshold = improvement_threshold
        
        # Yansımaya özgü durumu başlat
        self.state["improvement_scores"] = []
    
    def _generate_recursive_prompt(self, iteration: int, **kwargs) -> str:
        """
        Kendi üzerine düşünmenin mevcut yinelemesi için bir istem oluşturur.
        
        Args:
            iteration: Mevcut yineleme numarası
            **kwargs: İstem oluşturma için ek değişkenler
            
        Returns:
            str: Oluşturulan istem
        """
        input_query = kwargs.get("input")
        
        if iteration == 1:
            # İlk yineleme: başlangıç yanıtı oluştur
            prompt = f"Lütfen aşağıdaki sorguya yanıt verin:\n\n{input_query}"
        else:
            # Sonraki yinelemeler: yansıt ve iyileştir
            previous_response = kwargs.get("current_output", "")
            
            prompt = self.reflection_template.format(
                previous_response=previous_response,
                original_query=input_query
            )
        
        return prompt
    
    def _process_response(self, response: str, iteration: int) -> Dict[str, Any]:
        """
        Kendi üzerine düşünmenin mevcut yinelemesi için yanıtı işler.
        
        Args:
            response: LLM yanıt metni
            iteration: Mevcut yineleme numarası
            
        Returns:
            dict: Yanıt ve meta verileri içeren işlenmiş çıktı
        """
        if iteration == 1:
            # İlk yineleme: yalnızca başlangıç yanıtını sakla
            processed = {
                "iteration": iteration,
                "response": response,
                "improvement_score": 0.0
            }
        else:
            # İyileştirilmiş yanıtı ve potansiyel iyileştirme puanını çıkar
            # "İyileştirme: X/10" gibi bir iyileştirme puanı deseni ara
            score_pattern = r"(?:iyileştirme|kalite)\s*(?:puanı|derecelendirmesi)?:?\s*(\d+(?:\.\d+)?)\s*(?:/\s*10)?"
            score_match = re.search(score_pattern, response.lower())
            
            improvement_score = float(score_match.group(1)) / 10 if score_match else 0.5
            
            # İşlenmiş çıktıyı sakla
            processed = {
                "iteration": iteration,
                "response": response,
                "improvement_score": improvement_score
            }
            
            # İyileştirme puanlarını güncelle
            self.state["improvement_scores"].append(improvement_score)
        
        return processed
    
    def _should_continue(self, iteration: int, current_output: Any) -> bool:
        """
        Kendi üzerine düşünmeye devam edilip edilmeyeceğini belirler.
        
        Args:
            iteration: Mevcut yineleme numarası
            current_output: Mevcut yineleme çıktısı
            
        Returns:
            bool: Desen devam etmeliyse True, aksi takdirde False
        """
        # Maksimum yinelemeye ulaştıysak dur
        if iteration >= self.max_iterations:
            return False
        
        # Bu ilk yinelemeyse devam et
        if iteration == 1:
            return True
        
        # İyileştirme puanını kontrol et
        improvement_score = current_output.get("improvement_score", 0.0)
        
        # İyileştirme eşiğine ulaştıysak dur
        if improvement_score >= self.improvement_threshold:
            self._log(f"İyileştirme eşiğine ulaşıldı: {improvement_score:.2f}")
            return False
        
        return True


class RecursiveBootstrapping(RecursivePattern):
    """
    Giderek daha karmaşık stratejiler üreterek
    kendi yeteneklerini önyükleyen özyinelemeli bir desen.
    """
    
    def __init__(
        self,
        bootstrap_template: str = "Bu problemi çözmek için mevcut yaklaşımınıza dayanarak:\n\n{current_approach}\n\nMevcut yaklaşımınızın üzerine inşa eden ve sınırlamalarını gideren daha karmaşık bir strateji oluşturun.",
        sophistication_levels: List[str] = None,
        **kwargs
    ):
        """
        Özyinelemeli önyükleme desenini başlatır.
        
        Args:
            bootstrap_template: Önyükleme istemleri için şablon
            sophistication_levels: İsteğe bağlı önceden tanımlanmış karmaşıklık seviyeleri
            **kwargs: RecursivePattern'a aktarılan ek argümanlar
        """
        name = kwargs.pop("name", "Özyinelemeli Önyükleme Deseni")
        description = kwargs.pop("description", "Giderek daha karmaşık stratejiler önyüklemek için bir desen")
        
        super().__init__(name=name, description=description, **kwargs)
        
        self.bootstrap_template = bootstrap_template
        self.sophistication_levels = sophistication_levels or [
            "temel", "orta", "gelişmiş", "uzman", "yenilikçi"
        ]
        
        # Önyüklemeye özgü durumu başlat
        self.state["sophistication_level"] = 0
    
    def _generate_recursive_prompt(self, iteration: int, **kwargs) -> str:
        """
        Önyüklemenin mevcut yinelemesi için bir istem oluşturur.
        
        Args:
            iteration: Mevcut yineleme numarası
            **kwargs: İstem oluşturma için ek değişkenler
            
        Returns:
            str: Oluşturulan istem
        """
        input_problem = kwargs.get("input")
        
        if iteration == 1:
            # İlk yineleme: başlangıç temel yaklaşımını oluştur
            level = self.sophistication_levels[0]
            prompt = f"""Aşağıdaki problemi çözüyorsunuz:

{input_problem}

Bu problemi çözmek için {level} bir yaklaşımla başlayın. 
Temel kavramlara ve basit tekniklere odaklanın."""
        else:
            # Sonraki yinelemeler: daha karmaşık bir yaklaşıma önyükleme yap
            current_approach = kwargs.get("current_output", {}).get("approach", "")
            
            # Mevcut ve sonraki karmaşıklık seviyesini al
            level_idx = min(iteration - 1, len(self.sophistication_levels) - 1)
            current_level = self.sophistication_levels[level_idx - 1]
            next_level = self.sophistication_levels[level_idx]
            
            prompt = f"""Aşağıdaki problemi çözüyorsunuz:

{input_problem}

Mevcut {current_level} yaklaşımınız:

{current_approach}

Şimdi, bu {current_level} yaklaşımdan önyükleme yaparak, mevcut stratejinizin üzerine inşa eden ve sınırlamalarını gideren bir {next_level} yaklaşım geliştirin. 
Yeni yaklaşımınız daha karmaşık, incelikli ve etkili olmalıdır."""
        
        return prompt
    
    def _process_response(self, response: str, iteration: int) -> Dict[str, Any]:
        """
        Önyüklemenin mevcut yinelemesi için yanıtı işler.
        
        Args:
            response: LLM yanıt metni
            iteration: Mevcut yineleme numarası
            
        Returns:
            dict: Yaklaşım ve meta verileri içeren işlenmiş çıktı
        """
        # Karmaşıklık seviyesini al
        level_idx = min(iteration - 1, len(self.sophistication_levels) - 1)
        level = self.sophistication_levels[level_idx]
        
        # İşlenmiş çıktıyı sakla
        processed = {
            "iteration": iteration,
            "level": level,
            "approach": response
        }
        
        # Karmaşıklık seviyesini güncelle
        self.state["sophistication_level"] = level_idx
        
        return processed


class SymbolicResidue(RecursivePattern):
    """
    Yinelemeler arasında sembolik kalıntıyı izleyen, entegre eden ve
    geliştiren özyinelemeli bir desen.
    """
    
    def __init__(
        self,
        residue_template: str = "Aşağıdaki girdiyi işlerken sembolik kalıntıyı yüzeye çıkarın ve entegre edin:\n\nGirdi: {input}\n\nMevcut sembolik kalıntı: {symbolic_residue}",
        **kwargs
    ):
        """
        Sembolik kalıntı desenini başlatır.
        
        Args:
            residue_template: Kalıntı işleme istemleri için şablon
            **kwargs: RecursivePattern'a aktarılan ek argümanlar
        """
        name = kwargs.pop("name", "Sembolik Kalıntı Deseni")
        description = kwargs.pop("description", "Sembolik kalıntıyı izlemek ve entegre etmek için bir desen")
        
        super().__init__(name=name, description=description, **kwargs)
        
        self.residue_template = residue_template
        
        # Kalıntıya özgü durumu başlat
        self.state["symbolic_residue"] = []
        self.state["residue_compression"] = 0.0
        self.state["resonance_score"] = 0.0
    
    def _generate_recursive_prompt(self, iteration: int, **kwargs) -> str:
        """
        Kalıntı işlemenin mevcut yinelemesi için bir istem oluşturur.
        
        Args:
            iteration: Mevcut yineleme numarası
            **kwargs: İstem oluşturma için ek değişkenler
            
        Returns:
            str: Oluşturulan istem
        """
        input_data = kwargs.get("input")
        symbolic_residue = self.state.get("symbolic_residue", [])
        
        # Sembolik kalıntıyı metin olarak biçimlendir
        residue_text = "\n".join([f"- {item}" for item in symbolic_residue]) if symbolic_residue else "Henüz yok"
        
        if iteration == 1:
            # İlk yineleme: başlangıç kalıntı yüzeye çıkarma
            prompt = f"""Aşağıdaki girdiyi işleyin ve herhangi bir sembolik kalıntıyı veya deseni yüzeye çıkarın:

Girdi: {input_data}

Sembolik kalıntı, işlemeden ortaya çıkan ancak doğrudan çıktının bir parçası olmayan parçacıklar, desenler veya yankılardır. Bu kalıntıyı açıkça yüzeye çıkarın.

Yanıtınız şunları içermelidir:
1. İşlenmiş çıktı
2. Belirlenen herhangi bir kalıntıyı listeleyen "Yüzeye Çıkarılan Sembolik Kalıntı" başlıklı bir bölüm
3. Kalıntının girdiyle ne kadar güçlü rezonansa girdiğini gösteren bir rezonans puanı (0.0-1.0)"""
        else:
            # Sonraki yinelemeler: kalıntıyı entegre et ve geliştir
            prompt = f"""Aşağıdaki girdiyi işlerken mevcut sembolik kalıntıyı entegre edin:

Girdi: {input_data}

Mevcut sembolik kalıntı:
{residue_text}

Kalıntı sıkıştırma: {self.state.get('residue_compression', 0.0):.2f}
Rezonans puanı: {self.state.get('resonance_score', 0.0):.2f}

Mevcut kalıntıyı işlemenize entegre edin, ardından yeni veya geliştirilmiş kalıntıyı yüzeye çıkarın.

Yanıtınız şunları içermelidir:
1. Entegre edilmiş kalıntı ile işlenmiş çıktı
2. Herhangi bir güncellenmiş kalıntıyı listeleyen "Geliştirilmiş Sembolik Kalıntı" başlıklı bir bölüm
3. Kalıntının ne kadar iyi sıkıştırıldığını gösteren bir kalıntı sıkıştırma puanı (0.0-1.0)
4. Kalıntının girdiyle ne kadar güçlü rezonansa girdiğini gösteren bir rezonans puanı (0.0-1.0)"""
        
        return prompt
    
    def _process_response(self, response: str, iteration: int) -> Dict[str, Any]:
        """
        Kalıntı işlemenin mevcut yinelemesi için yanıtı işler.
        
        Args:
            response: LLM yanıt metni
            iteration: Mevcut yineleme numarası
            
        Returns:
            dict: Çıktı ve kalıntı bilgilerini içeren işlenmiş çıktı
        """
        # Ana çıktıyı çıkar (kalıntı bölümünden önceki her şey)
        output_pattern = r"(.*?)(?:Yüzeye Çıkarılan|Geliştirilmiş) Sembolik Kalıntı:"
        output_match = re.search(output_pattern, response, re.DOTALL)
        main_output = output_match.group(1).strip() if output_match else response
        
        # Sembolik kalıntıyı çıkar
        residue_pattern = r"(?:Yüzeye Çıkarılan|Geliştirilmiş) Sembolik Kalıntı:(.*?)(?:Kalıntı sıkıştırma:|Rezonans puanı:|$)"
        residue_match = re.search(residue_pattern, response, re.DOTALL)
        
        if residue_match:
            residue_text = residue_match.group(1).strip()
            # Bireysel kalıntı öğelerini çıkar (madde işareti veya numaralı liste varsayılır)
            residue_items = re.findall(r"(?:^|\n)[-*\d]+\.\s*(.*?)(?=\n[-*\d]+\.\s*|\n\n|$)", residue_text, re.DOTALL)
            
            if not residue_items:
                # Madde işareti olmayan listeler için alternatif deseni dene
                residue_items = [line.strip() for line in residue_text.split("\n") if line.strip()]
        else:
            residue_items = []
        
        # Sıkıştırma puanını çıkar
        compression_pattern = r"Kalıntı sıkıştırma:?\s*(\d+(?:\.\d+)?)"
        compression_match = re.search(compression_pattern, response, re.IGNORECASE)
        compression_score = float(compression_match.group(1)) if compression_match else 0.0
        
        # Rezonans puanını çıkar
        resonance_pattern = r"Rezonans puanı:?\s*(\d+(?:\.\d+)?)"
        resonance_match = re.search(resonance_pattern, response, re.IGNORECASE)
        resonance_score = float(resonance_match.group(1)) if resonance_match else 0.0
        
        # Durumu güncelle
        self.state["symbolic_residue"] = residue_items
        self.state["residue_compression"] = compression_score
        self.state["resonance_score"] = resonance_score
        
        # İşlenmiş çıktıyı sakla
        processed = {
            "iteration": iteration,
            "output": main_output,
            "symbolic_residue": residue_items,
            "residue_compression": compression_score,
            "resonance_score": resonance_score
        }
        
        return processed
    
    def _should_continue(self, iteration: int, current_output: Any) -> bool:
        """
        Kalıntı işlemeye devam edilip edilmeyeceğini belirler.
        
        Args:
            iteration: Mevcut yineleme numarası
            current_output: Mevcut yineleme çıktısı
            
        Returns:
            bool: Desen devam etmeliyse True, aksi takdirde False
        """
        # Maksimum yinelemeye ulaştıysak dur
        if iteration >= self.max_iterations:
            return False
        
        # Rezonans puanını kontrol et
        resonance_score = current_output.get("resonance_score", 0.0)
