#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bağlam Mühendisliği: Çok Adımlı LLM Etkileşimleri için Kontrol Döngüleri
=================================================================

Bu modül, karmaşık çok adımlı LLM etkileşimlerini düzenlemek için
kontrol akış mekanizmalarının nasıl uygulanacağını gösterir. Önceki
betiklerdeki bağlam genişletme tekniklerine dayanarak, şimdi
şu desenleri keşfediyoruz:

1. Sıralı zincirleme (bir adımın çıktısı → bir sonrakinin girdisi)
2. Yinelemeli iyileştirme (bir yanıtı döngülerle iyileştirme)
3. Koşullu dallanma (LLM çıktısına göre farklı yollar)
4. Kendi kendini eleştirme ve düzeltme (çıktıların meta-değerlendirmesi)
5. Harici doğrulama döngüleri (doğrulamak için araçları/bilgiyi kullanma)

Desenler, jeton verimliliği ve adımlar arasında bağlam tutarlılığını
korumaya odaklanılarak uygulanır.

Kullanım:
    # Jupyter veya Colab'da:
    %run 03_control_loops.py
    # veya
    from control_loops import SequentialChain, IterativeRefiner, ConditionalBrancher
"""

import os
import re
import json
import time
import tiktoken
from typing import Dict, List, Tuple, Any, Optional, Union, Callable, TypeVar

# Daha iyi tür ipuçları için tür değişkenleri
T = TypeVar('T')
Response = Union[str, Dict[str, Any]]

# Günlüğe kaydetme ve görselleştirme için
import logging
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, HTML

# Günlüğe kaydetmeyi yapılandır
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API istemcileri için kurulum
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
DEFAULT_MAX_TOKENS = 500


# Yardımcı Fonksiyonlar
# ================

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


def display_response(
    prompt: str,
    response: str,
    metrics: Dict[str, Any],
    show_prompt: bool = True
) -> None:
    """
    Bir istem-yanıt çiftini bir not defterinde metriklerle birlikte görüntüler.
    
    Args:
        prompt: İstem metni
        response: Yanıt metni
        metrics: Metrikler sözlüğü
        show_prompt: İstem metninin gösterilip gösterilmeyeceği
    """
    if show_prompt:
        display(HTML("<h4>İstem:</h4>"))
        display(Markdown(f"```
{prompt}
```"))
    
    display(HTML("<h4>Yanıt:</h4>"))
    display(Markdown(response))
    
    display(HTML("<h4>Metrikler:</h4>"))
    display(Markdown(f"```
{format_metrics(metrics)}
```"))


# Kontrol Döngüsü Temel Sınıfları
# ========================

class ControlLoop:
    """
    Tüm kontrol döngüsü uygulamaları için temel sınıf.
    Metrikleri ve geçmişi izlemek için ortak işlevsellik sağlar.
    """
    
    def __init__(
        self,
        client=None,
        model: str = DEFAULT_MODEL,
        system_message: str = "Yardımcı bir asistansınız.",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        verbose: bool = False
    ):
        """
        Kontrol döngüsünü başlatır.
        
        Args:
            client: API istemcisi (None ise, bir tane oluşturulur)
            model: Kullanılacak model adı
            system_message: Kullanılacak sistem mesajı
            max_tokens: Üretilecek maksimum jeton sayısı
            temperature: Sıcaklık parametresi
            verbose: Hata ayıklama bilgilerinin yazdırılıp yazdırılmayacağı
        """
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
            "steps": 0
        }
    
    def _log(self, message: str) -> None:
        """
        Ayrıntılı mod etkinse bir mesajı günlüğe kaydeder.
        
        Args:
            message: Günlüğe kaydedilecek mesaj
        """
        if self.verbose:
            logger.info(message)
    
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
        self.metrics["steps"] += 1
        
        # Geçmişe ekle
        step_record = {
            "prompt": prompt,
            "response": response,
            "metrics": metadata,
            "timestamp": time.time()
        }
        self.history.append(step_record)
        
        return response, metadata
    
    def get_summary_metrics(self) -> Dict[str, Any]:
        """
        Tüm adımlar için özet metrikleri alır.
        
        Returns:
            dict: Özet metrikler
        """
        summary = self.metrics.copy()
        
        # Türetilmiş metrikleri ekle
        if summary["steps"] > 0:
            summary["avg_latency_per_step"] = summary["total_latency"] / summary["steps"]
            
        if summary["total_prompt_tokens"] > 0:
            summary["overall_efficiency"] = (
                summary["total_response_tokens"] / summary["total_prompt_tokens"]
            )
        
        return summary
    
    def visualize_metrics(self) -> None:
        """
        Adımlar arasında metriklerin görselleştirilmesini oluşturur.
        """
        if not self.history:
            logger.warning("Görselleştirilecek geçmiş yok")
            return
        
        # Çizim için verileri çıkar
        steps = list(range(1, len(self.history) + 1))
        prompt_tokens = [h["metrics"].get("prompt_tokens", 0) for h in self.history]
        response_tokens = [h["metrics"].get("response_tokens", 0) for h in self.history]
        latencies = [h["metrics"].get("latency", 0) for h in self.history]
        efficiencies = [h["metrics"].get("token_efficiency", 0) for h in self.history]
        
        # Şekil oluştur
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("Adıma Göre Kontrol Döngüsü Metrikleri", fontsize=16)
        
        # Grafik 1: Jeton kullanımı
        axes[0, 0].bar(steps, prompt_tokens, label="İstem Jetonları", color="blue", alpha=0.7)
        axes[0, 0].bar(steps, response_tokens, bottom=prompt_tokens, label="Yanıt Jetonları", 
                       color="green", alpha=0.7)
        axes[0, 0].set_title("Jeton Kullanımı")
        axes[0, 0].set_xlabel("Adım")
        axes[0, 0].set_ylabel("Jetonlar")
        axes[0, 0].legend()
        axes[0, 0].grid(alpha=0.3)
        
        # Grafik 2: Gecikme
        axes[0, 1].plot(steps, latencies, marker='o', color="red", alpha=0.7)
        axes[0, 1].set_title("Gecikme")
        axes[0, 1].set_xlabel("Adım")
        axes[0, 1].set_ylabel("Saniye")
        axes[0, 1].grid(alpha=0.3)
        
        # Grafik 3: Jeton Verimliliği
        axes[1, 0].plot(steps, efficiencies, marker='s', color="purple", alpha=0.7)
        axes[1, 0].set_title("Jeton Verimliliği (Yanıt/İstem)")
        axes[1, 0].set_xlabel("Adım")
        axes[1, 0].set_ylabel("Oran")
        axes[1, 0].grid(alpha=0.3)
        
        # Grafik 4: Kümülatif Jetonlar
        cumulative_tokens = np.cumsum([h["metrics"].get("total_tokens", 0) for h in self.history])
        axes[1, 1].plot(steps, cumulative_tokens, marker='^', color="orange", alpha=0.7)
        axes[1, 1].set_title("Kümülatif Jeton Kullanımı")
        axes[1, 1].set_xlabel("Adım")
        axes[1, 1].set_ylabel("Toplam Jeton")
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()


class SequentialChain(ControlLoop):
    """
    Her adımın çıktısının bir sonraki adımın girdisi olduğu,
    birden çok adımı sırayla zincirleyen bir kontrol döngüsü.
    """
    
    def __init__(self, steps: List[Dict[str, Any]], **kwargs):
        """
        Sıralı zinciri başlatır.
        
        Args:
            steps: Her biri şunları içeren adım yapılandırmaları listesi:
                - prompt_template: {input} yer tutucusuna sahip str
                - system_message: (isteğe bağlı) özel sistem mesajı
                - name: (isteğe bağlı) adım adı
            **kwargs: ControlLoop'a aktarılan ek argümanlar
        """
        super().__init__(**kwargs)
        self.steps = steps
        self._validate_steps()
    
    def _validate_steps(self) -> None:
        """Adım yapılandırmalarını doğrular."""
        for i, step in enumerate(self.steps):
            if "prompt_template" not in step:
                raise ValueError(f"Adım {i} 'prompt_template' eksik")
            
            # Her adımın bir adı olduğundan emin ol
            if "name" not in step:
                step["name"] = f"adım_{i+1}"
    
    def run(self, initial_input: str) -> Tuple[str, Dict[str, Any]]:
        """
        Sıralı zinciri verilen başlangıç girdisiyle çalıştırır.
        
        Args:
            initial_input: İlk adımın girdisi
            
        Returns:
            tuple: (son_çıktı, tüm_çıktılar)
        """
        current_input = initial_input
        all_outputs = {"initial_input": initial_input}
        
        for i, step in enumerate(self.steps):
            step_name = step["name"]
            self._log(f"Adım {i+1}/{len(self.steps)} çalıştırılıyor: {step_name}")
            
            # Mevcut girdiyi kullanarak istemi biçimlendir
            prompt = step["prompt_template"].format(input=current_input)
            system_message = step.get("system_message", self.system_message)
            
            # LLM'yi çağır
            response, metadata = self._call_llm(prompt, system_message)
            
            # Çıktıyı sakla
            all_outputs[step_name] = {
                "prompt": prompt,
                "response": response,
                "metrics": metadata
            }
            
            # Bir sonraki adım için girdiyi güncelle
            current_input = response
        
        return current_input, all_outputs
    
    def display_chain_results(self, all_outputs: Dict[str, Any]) -> None:
        """
        Zincirdeki her adımın sonuçlarını görüntüler.
        
        Args:
            all_outputs: run() işlevinden gelen çıktı sözlüğü
        """
        display(HTML("<h2>Sıralı Zincir Sonuçları</h2>"))
        
        # Başlangıç girdisini görüntüle
        display(HTML("<h3>Başlangıç Girdisi</h3>"))
        display(Markdown(all_outputs["initial_input"]))
        
        # Her adımı görüntüle
        for i, step in enumerate(self.steps):
            step_name = step["name"]
            if step_name in all_outputs:
                step_output = all_outputs[step_name]
                
                display(HTML(f"<h3>Adım {i+1}: {step_name}</h3>"))
                
                # İstem görüntüle
                display(HTML("<h4>İstem:</h4>"))
                display(Markdown(f"```
{step_output['prompt']}
```"))
                
                # Yanıt görüntüle
                display(HTML("<h4>Yanıt:</h4>"))
                display(Markdown(step_output["response"]))
                
                # Metrikleri görüntüle
                display(HTML("<h4>Metrikler:</h4>"))
                display(Markdown(f"```
{format_metrics(step_output['metrics'])}
```"))
        
        # Özet metrikleri görüntüle
        display(HTML("<h3>Özet Metrikler</h3>"))
        summary = self.get_summary_metrics()
        display(Markdown(f"""
        - Toplam Adım: {summary['steps']}
        - Toplam Jeton: {summary['total_tokens']}
        - Toplam Gecikme: {summary['total_latency']:.2f}s
        - Adım Başına Ort. Gecikme: {summary.get('avg_latency_per_step', 0):.2f}s
        - Genel Verimlilik: {summary.get('overall_efficiency', 0):.2f}
        """))


class IterativeRefiner(ControlLoop):
    """
    Bir çıktıyı, bir durdurma koşulu karşılanana kadar birden çok
    geri bildirim ve iyileştirme döngüsüyle yinelemeli olarak iyileştiren bir kontrol döngüsü.
    """
    
    def __init__(
        self,
        max_iterations: int = 5,
        refinement_template: str = "Lütfen aşağıdaki metni iyileştirin: {previous_response}

Gereken özel iyileştirmeler: {feedback}",
        feedback_template: str = "Bu yanıtın kalitesini değerlendirin ve özel iyileştirmeler önerin: {response}",
        stopping_condition: Optional[Callable[[str, Dict[str, Any]], bool]] = None,
        **kwargs
    ):
        """
        Yinelemeli iyileştiriciyi başlatır.
        
        Args:
            max_iterations: Maksimum iyileştirme yinelemesi sayısı
            refinement_template: İyileştirme istemleri için şablon
            feedback_template: Geri bildirim oluşturmak için şablon
            stopping_condition: (yanıt, meta_veriler) alan ve iyileştirmenin
                               durması gerekip gerekmediğini belirten True döndüren işlev
            **kwargs: ControlLoop'a aktarılan ek argümanlar
        """
        super().__init__(**kwargs)
        self.max_iterations = max_iterations
        self.refinement_template = refinement_template
        self.feedback_template = feedback_template
        self.stopping_condition = stopping_condition
    
    def generate_feedback(self, response: str) -> Tuple[str, Dict[str, Any]]:
        """
        Mevcut yanıt hakkında geri bildirim oluşturur.
        
        Args:
            response: Değerlendirilecek mevcut yanıt
            
        Returns:
            tuple: (geri_bildirim, meta_veriler)
        """
        prompt = self.feedback_template.format(response=response)
        return self._call_llm(prompt)
    
    def refine_response(
        self,
        previous_response: str,
        feedback: str
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Yanıtı geri bildirime göre iyileştirir.
        
        Args:
            previous_response: İyileştirilecek önceki yanıt
            feedback: İyileştirme için kullanılacak geri bildirim
            
        Returns:
            tuple: (iyileştirilmiş_yanıt, meta_veriler)
        """
        prompt = self.refinement_template.format(
            previous_response=previous_response,
            feedback=feedback
        )
        return self._call_llm(prompt)
    
    def run(
        self,
        initial_prompt: str,
        use_auto_feedback: bool = True
    ) -> Tuple[str, Dict[str, List[Dict[str, Any]]]]:
        """
        Yinelemeli iyileştirme sürecini çalıştırır.
        
        Args:
            initial_prompt: İlk yanıtı oluşturmak için başlangıç istemi
            use_auto_feedback: Otomatik geri bildirim oluşturulup oluşturulmayacağı (False ise,
                              geri bildirimi manuel olarak sağlamanız gerekir)
                              
        Returns:
            tuple: (son_yanıt, iyileştirme_geçmişi)
        """
        # Başlangıç yanıtını oluştur
        self._log("Başlangıç yanıtı oluşturuluyor")
        current_response, metadata = self._call_llm(initial_prompt)
        
        refinement_history = {
            "initial": {
                "prompt": initial_prompt,
                "response": current_response,
                "metrics": metadata
            },
            "iterations": []
        }
        
        # Yinelemeli iyileştirme döngüsü
        iteration = 0
        should_continue = True
        
        while should_continue and iteration < self.max_iterations:
            iteration += 1
            self._log(f"İyileştirme yinelemesi {iteration}/{self.max_iterations}")
            
            # Geri bildirim oluştur
            if use_auto_feedback:
                feedback, feedback_metadata = self.generate_feedback(current_response)
                self._log(f"Otomatik geri bildirim: {feedback}")
            else:
                # Manuel geri bildirim modu
                print(f"

Mevcut yanıt (yineleme {iteration}):")
                print("-" * 80)
                print(current_response)
                print("-" * 80)
                feedback = input("Geri bildiriminizi girin (veya iyileştirmeyi sonlandırmak için 'dur'): ")
                
                if feedback.lower() == 'dur':
                    break
                
                feedback_metadata = {"manual": True}
            
            # Yanıtı iyileştir
            refined_response, refine_metadata = self.refine_response(current_response, feedback)
            
            # Yinelemeyi kaydet
            refinement_history["iterations"].append({
                "iteration": iteration,
                "feedback": feedback,
                "feedback_metrics": feedback_metadata,
                "refined_response": refined_response,
                "refinement_metrics": refine_metadata
            })
            
            # Mevcut yanıtı güncelle
            current_response = refined_response
            
            # Durdurma koşulunu kontrol et
            if self.stopping_condition:
                should_continue = not self.stopping_condition(current_response, refine_metadata)
        
        return current_response, refinement_history
    
    def display_refinement_history(self, refinement_history: Dict[str, Any]) -> None:
        """
        İyileştirme geçmişini bir not defterinde görüntüler.
        
        Args:
            refinement_history: run() işlevinden gelen iyileştirme geçmişi
        """
        display(HTML("<h2>Yinelemeli İyileştirme Sonuçları</h2>"))
        
        # Başlangıç istemini ve yanıtını görüntüle
        display(HTML("<h3>Başlangıç İstemi</h3>"))
        display(Markdown(f"```
{refinement_history['initial']['prompt']}
```"))
        
        display(HTML("<h3>Başlangıç Yanıtı</h3>"))
        display(Markdown(refinement_history['initial']['response']))
        
        # İyileştirme yinelemelerini görüntüle
        for iteration in refinement_history["iterations"]:
            iteration_num = iteration["iteration"]
            
            display(HTML(f"<h3>Yineleme {iteration_num}</h3>"))
            
            # Geri bildirimi görüntüle
            display(HTML("<h4>Geri bildirim:</h4>"))
            display(Markdown(iteration["feedback"]))
            
            # İyileştirilmiş yanıtı görüntüle
            display(HTML("<h4>İyileştirilmiş Yanıt:</h4>"))
            display(Markdown(iteration["refined_response"]))
            
            # Metrikleri görüntüle
            display(HTML("<h4>Metrikler:</h4>"))
            metrics = iteration["refinement_metrics"]
            display(Markdown(f"```
{format_metrics(metrics)}
```"))
        
        # Özeti görüntüle
        display(HTML("<h3>İyileştirme Özeti</h3>"))
        total_iterations = len(refinement_history["iterations"])
        display(Markdown(f"""
        - Başlangıç istemi jetonları: {refinement_history['initial']['metrics']['prompt_tokens']}
        - Başlangıç yanıtı jetonları: {refinement_history['initial']['metrics']['response_tokens']}
        - Toplam iyileştirme yinelemesi: {total_iterations}
        - Son yanıt jetonları: {refinement_history['iterations'][-1]['refinement_metrics']['response_tokens'] if total_iterations > 0 else refinement_history['initial']['metrics']['response_tokens']}
        """))


class ConditionalBrancher(ControlLoop):
    """
    LLM çıktılarına dayalı olarak koşullu dallanmayı uygulayan,
    koşullara bağlı olarak farklı yürütme yollarına izin veren bir kontrol döngüsü.
    """
    
    def __init__(
        self,
        branches: Dict[str, Dict[str, Any]],
        classifier_template: str = "Aşağıdaki girdiyi analiz edin ve tam olarak şu kategorilerden birine sınıflandırın: {categories}.

Girdi: {input}

Kategori:",
        **kwargs
    ):
        """
        Koşullu dallandırıcıyı başlatır.
        
        Args:
            branches: Dal adlarını yapılandırmalara eşleyen sözlük:
                - prompt_template: {input} yer tutucusuna sahip str
                - system_message: (isteğe bağlı) özel sistem mesajı
            classifier_template: Sınıflandırma istemi için şablon
            **kwargs: ControlLoop'a aktarılan ek argümanlar
        """
        super().__init__(**kwargs)
        self.branches = branches
        self.classifier_template = classifier_template
        self._validate_branches()
    
    def _validate_branches(self) -> None:
        """Dal yapılandırmalarını doğrular."""
        if not self.branches:
            raise ValueError("Dal tanımlanmadı")
        
        for branch_name, config in self.branches.items():
            if "prompt_template" not in config:
                raise ValueError(f"Dal '{branch_name}' 'prompt_template' eksik")
    
    def classify_input(self, input_text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Hangi dala gidileceğini belirlemek için girdiyi sınıflandırır.
        
        Args:
            input_text: Sınıflandırılacak girdi metni
            
        Returns:
            tuple: (dal_adı, meta_veriler)
        """
        categories = list(self.branches.keys())
        categories_str = ", ".join(categories)
        
        prompt = self.classifier_template.format(
            categories=categories_str,
            input=input_text
        )
        
        # Sınıflandırma için belirli bir sistem mesajı kullan
        system_message = "Girdileri hassas ve doğru bir şekilde kategorize eden bir sınıflandırıcısınız."
        response, metadata = self._call_llm(prompt, system_message)
        
        # Yanıttan dal adını çıkar
        # Önce bir kategoriyi tam olarak eşleştirmeyi dene
        for category in categories:
            if category.lower() in response.lower():
                return category, metadata
        
        # Tam eşleşme yoksa, ilk satırı yanıt olarak al ve en yakın eşleşmeyi bul
        first_line = response.strip().split('
')[0].lower()
        
        best_match = None
        best_score = 0
        
        for category in categories:
            # Basit dize benzerlik puanı
            cat_lower = category.lower()
            matches = sum(c in first_line for c in cat_lower)
            score = matches / len(cat_lower) if len(cat_lower) > 0 else 0
            
            if score > best_score:
                best_score = score
                best_match = category
        
        if best_match and best_score > 0.5:
            return best_match, metadata
        
        # Eşleşme bulunamazsa ilk kategoriye geri dön
        self._log(f"Uyarı: Girdi sınıflandırılamadı. İlk dal kullanılıyor: {categories[0]}")
        return categories[0], metadata
    
    def execute_branch(
        self,
        branch_name: str,
        input_text: str
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Belirli bir dalı verilen girdiyle yürütür.
        
        Args:
            branch_name: Yürütülecek dalın adı
            input_text: Dal için girdi metni
            
        Returns:
            tuple: (yanıt, meta_veriler)
        """
        if branch_name not in self.branches:
            raise ValueError(f"Bilinmeyen dal: {branch_name}")
        
        branch_config = self.branches[branch_name]
        prompt = branch_config["prompt_template"].format(input=input_text)
        system_message = branch_config.get("system_message", self.system_message)
        
        return self._call_llm(prompt, system_message)
    
    def run(
        self,
        input_text: str,
        branch_name: Optional[str] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Koşullu dallanma sürecini çalıştırır.
        
        Args:
            input_text: İşlenecek girdi metni
            branch_name: Kullanılacak isteğe bağlı dal (sınıflandırmayı atlar)
            
        Returns:
            tuple: (yanıt, çalışma_detayları)
        """
        run_details = {"input": input_text}
        
        # Dal belirtilmemişse girdiyi sınıflandır
        if branch_name is None:
            self._log("Girdi sınıflandırılıyor")
            branch_name, classification_metadata = self.classify_input(input_text)
            run_details["classification"] = {
                "branch": branch_name,
                "metrics": classification_metadata
            }
        
        self._log(f"Dal yürütülüyor: {branch_name}")
        
        # Seçilen dalı yürüt
        response, metadata = self.execute_branch(branch_name, input_text)
        
        run_details["execution"] = {
            "branch": branch_name,
            "response": response,
            "metrics": metadata
        }
        
        return response, run_details
    
    def display_branching_results(self, run_details: Dict[str, Any]) -> None:
        """
        Koşullu dallanma sonuçlarını bir not defterinde görüntüler.
        
        Args:
            run_details: run() işlevinden gelen çalışma detayları
        """
        display(HTML("<h2>Koşullu Dallanma Sonuçları</h2>"))
        
        # Girdiyi görüntüle
        display(HTML("<h3>Girdi</h3>"))
        display(Markdown(run_details["input"]))
        
        # Varsa sınıflandırmayı görüntüle
        if "classification" in run_details:
            display(HTML("<h3>Sınıflandırma</h3>"))
            branch = run_details["classification"]["branch"]
            display(Markdown(f"Seçilen dal: **{branch}**"))
            
            # Sınıflandırma metriklerini görüntüle
            display(HTML("<h4>Sınıflandırma Metrikleri:</h4>"))
            metrics = run_details["classification"]["metrics"]
            display(Markdown(f"```
{format_metrics(metrics)}
```"))
        
        # Yürütme sonuçlarını görüntüle
        display(HTML("<h3>Yürütme Sonuçları</h3>"))
        display(HTML("<h4>Dal:</h4>"))
        display(Markdown(f"**{run_details['execution']['branch']}**"))
        
        display(HTML("<h4>Yanıt:</h4>"))
        display(Markdown(run_details['execution']['response']))
        
        display(HTML("<h4>Yürütme Metrikleri:</h4>"))
        metrics = run_details['execution']['metrics']
        display(Markdown(f"```
{format_metrics(metrics)}
```"))


class SelfCritique(ControlLoop):
    """
    Bir yanıt üreten, ardından onu eleştiren ve iyileştiren bir kontrol döngüsü,
    iyileştirme için birden çok API çağrısı gerektirmeden tek bir akışta.
    """
    
    def __init__(
        self,
        critique_template: str = "Adım 1: Soruya bir yanıt oluşturun.
Adım 2: Yanıtınızı herhangi bir hata, eksiklik veya iyileştirme için eleştirin.
Adım 3: Eleştirinize dayanarak son, iyileştirilmiş bir yanıt sağlayın.

Soru: {input}",
        parse_sections: bool = True,
        **kwargs
    ):
        """
        Kendi kendini eleştirme kontrol döngüsünü başlatır.
        
        Args:
            critique_template: Kendi kendini eleştirme istemi için şablon
            parse_sections: Yanıtın bölümlere ayrılıp ayrılmayacağı
            **kwargs: ControlLoop'a aktarılan ek argümanlar
        """
        super().__init__(**kwargs)
        self.critique_template = critique_template
        self.parse_sections = parse_sections
    
    def run(self, input_text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Kendi kendini eleştirme sürecini çalıştırır.
        
        Args:
            input_text: Yanıtlanacak girdi
            
        Returns:
            tuple: (son_yanıt, çalışma_detayları)
        """
        # İstem biçimlendir
        prompt = self.critique_template.format(input=input_text)
        
        # Kendi kendini eleştirme yanıtı oluştur
        response, metadata = self._call_llm(prompt)
        
        # İstenirse bölümleri ayrıştır
        sections = {}
        if self.parse_sections:
            # Başlangıç yanıtını, eleştiriyi ve son yanıtı ayrıştırmaya çalış
            initial_match = re.search(r"Adım 1:(.*?)Adım 2:", response, re.DOTALL)
            critique_match = re.search(r"Adım 2:(.*?)Adım 3:", response, re.DOTALL)
            final_match = re.search(r"Adım 3:(.*?)$", response, re.DOTALL)
            
            if initial_match:
                sections["initial_response"] = initial_match.group(1).strip()
            if critique_match:
                sections["critique"] = critique_match.group(1).strip()
            if final_match:
                sections["final_response"] = final_match.group(1).strip()
        
        # Ayrıştırma başarısız olursa, tam yanıtı kullan
        if not sections and self.parse_sections:
            self._log("Yanıttan bölümler ayrıştırılamadı")
            sections["full_response"] = response
        
        # Çalışma detayları oluştur
        run_details = {
            "input": input_text,
            "full_response": response,
            "sections": sections,
            "metrics": metadata
        }
        
        # Son yanıtı döndür (veya ayrıştırma başarısız olursa tam yanıtı)
        final_response = sections.get("final_response", response)
        return final_response, run_details
    
    def display_results(self, run_details: Dict[str, Any]) -> None:
        """
        Kendi kendini eleştirme sonuçlarını bir not defterinde görüntüler.
        
        Args:
            run_details: run() işlevinden gelen çalışma detayları
        """
        display(HTML("<h2>Kendi Kendini Eleştirme Sonuçları</h2>"))
        
        # Girdiyi görüntüle
        display(HTML("<h3>Girdi</h3>"))
        display(Markdown(run_details["input"]))
        
        # Varsa ayrıştırılmış bölümleri görüntüle
        if "sections" in run_details and run_details["sections"]:
            sections = run_details["sections"]
            
            if "initial_response" in sections:
                display(HTML("<h3>Başlangıç Yanıtı</h3>"))
                display(Markdown(sections["initial_response"]))
            
            if "critique" in sections:
                display(HTML("<h3>Kendi Kendini Eleştirme</h3>"))
                display(Markdown(sections["critique"]))
            
            if "final_response" in sections:
                display(HTML("<h3>Son Yanıt</h3>"))
                display(Markdown(sections["final_response"]))
        
        # Bölüm yoksa tam yanıtı görüntüle
        elif "full_response" in run_details:
            display(HTML("<h3>Tam Yanıt</h3>"))
            display(Markdown(run_details["full_response"]))
        
        # Metrikleri görüntüle
        display(HTML("<h3>Metrikler</h3>"))
        metrics = run_details["metrics"]
        display(Markdown(f"```
{format_metrics(metrics)}
```"))


class ExternalValidation(ControlLoop):
    """
    LLM yanıtlarını doğrulamak ve düzeltmek için harici araçları veya bilgiyi
    kullanan, kapalı bir geri bildirim döngüsü oluşturan bir kontrol döngüsü.
    """
    
    def __init__(
        self,
        validator_fn: Callable[[str], Tuple[bool, str]],
        correction_template: str = "Önceki yanıtınızda bazı sorunlar vardı:

{validation_feedback}

Lütfen bu sorunları gidermek için yanıtınızı düzeltin:

{previous_response}",
        max_attempts: int = 3,
        **kwargs
    ):
        """
        Harici doğrulama döngüsünü başlatır.
        
        Args:
            validator_fn: Bir yanıt alan ve (geçerli_mi, geri_bildirim_mesajı)
                        döndüren işlev
            correction_template: Düzeltme istemleri için şablon
            max_attempts: Maksimum doğrulama denemesi
            **kwargs: ControlLoop'a aktarılan ek argümanlar
        """
        super().__init__(**kwargs)
        self.validator_fn = validator_fn
        self.correction_template = correction_template
        self.max_attempts = max_attempts
    
    def run(self, input_text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Harici doğrulama sürecini çalıştırır.
        
        Args:
            input_text: Yanıtlanacak girdi
            
        Returns:
            tuple: (son_yanıt, çalışma_detayları)
        """
        # Başlangıç yanıtını oluştur
        response, metadata = self._call_llm(input_text)
        
        attempts = []
        current_response = response
        is_valid = False
        validation_feedback = ""
        
        # Başlangıç denemesini ekle
        attempts.append({
            "attempt": 1,
            "response": current_response,
            "metrics": metadata,
            "validation": {
                "pending": True
            }
        })
        
        # Doğrulama döngüsü
        for attempt in range(1, self.max_attempts + 1):
            # Mevcut yanıtı doğrula
            self._log(f"Deneme {attempt} doğrulanıyor")
            is_valid, validation_feedback = self.validator_fn(current_response)
            
            # Mevcut deneme için doğrulama sonuçlarını güncelle
            attempts[-1]["validation"] = {
                "is_valid": is_valid,
                "feedback": validation_feedback,
                "pending": False
            }
            
            # Geçerliyse dur
            if is_valid:
                self._log(f"Deneme {attempt}'de geçerli yanıt")
                break
            
            # Maksimum denemeye ulaşılırsa dur
            if attempt >= self.max_attempts:
                self._log(f"Maksimum deneme ({self.max_attempts}) geçerli yanıt olmadan ulaşıldı")
                break
            
            # Düzeltme istemi oluştur
            self._log(f"Düzeltme deneniyor (deneme {attempt+1})")
            correction_prompt = self.correction_template.format(
                validation_feedback=validation_feedback,
                previous_response=current_response
            )
            
            # Düzeltilmiş yanıt oluştur
            corrected_response, correction_metadata = self._call_llm(correction_prompt)
            current_response = corrected_response
            
            # Yeni deneme ekle
            attempts.append({
                "attempt": attempt + 1,
                "response": current_response,
                "metrics": correction_metadata,
                "validation": {
                    "pending": True
                }
            })
        
        # Çalışma detayları oluştur
        run_details = {
            "input": input_text,
            "attempts": attempts,
            "final_response": current_response,
            "is_valid": is_valid,
            "validation_feedback": validation_feedback,
            "attempts_count": len(attempts)
        }
        
        return current_response, run_details
    
    def display_results(self, run_details: Dict[str, Any]) -> None:
        """
        Harici doğrulama sonuçlarını bir not defterinde görüntüler.
        
        Args:
            run_details: run() işlevinden gelen çalışma detayları
        """
        display(HTML("<h2>Harici Doğrulama Sonuçları</h2>"))
        
        # Girdiyi görüntüle
        display(HTML("<h3>Girdi</h3>"))
        display(Markdown(run_details["input"]))
        
        # Denemeleri görüntüle
        for attempt_data in run_details["attempts"]:
            attempt_num = attempt_data["attempt"]
            display(HTML(f"<h3>Deneme {attempt_num}</h3>"))
            
            # Yanıtı görüntüle
            display(HTML("<h4>Yanıt:</h4>"))
            display(Markdown(attempt_data["response"]))
            
            # Doğrulama sonuçlarını görüntüle
            if not attempt_data["validation"]["pending"]:
                is_valid = attempt_data["validation"]["is_valid"]
                display(HTML("<h4>Doğrulama:</h4>"))
                
                if is_valid:
                    display(HTML("<p style='color: green; font-weight: bold;'>✓ Geçerli</p>"))
                else:
                    display(HTML("<p style='color: red; font-weight: bold;'>✗ Geçersiz</p>"))
                    display(HTML("<h4>Geri bildirim:</h4>"))
                    display(Markdown(attempt_data["validation"]["feedback"]))
            
            # Metrikleri görüntüle
            display(HTML("<h4>Metrikler:</h4>"))
            metrics = attempt_data["metrics"]
            display(Markdown(f"```
{format_metrics(metrics)}
```"))
        
        # Özeti görüntüle
        display(HTML("<h3>Özet</h3>"))
        is_valid = run_details["is_valid"]
        status = "✓ Geçerli" if is_valid else "✗ Geçersiz"
        display(Markdown(f"""
        - Son durum: **{status}**
        - Toplam deneme: {run_details['attempts_count']}
        - Toplam jeton: {self.metrics['total_tokens']}
        - Toplam gecikme: {self.metrics['total_latency']:.2f}s
        """))


# Örnek Kullanım
# ============

def example_sequential_chain():
    """Veri analizi için sıralı bir zincir örneği."""
    steps = [
        {
            "name": "varlıkları_çıkar",
            "prompt_template": "Bu metinden ana varlıkları (kişiler, yerler, kuruluşlar) çıkarın. Her varlık için kısa bir açıklama yapın.

Metin: {input}",
            "system_message": "Metinden adlandırılmış varlıkları çıkarmada ve kategorize etmede uzmansınız."
        },
        {
            "name": "ilişkileri_analiz_et",
            "prompt_template": "Bu varlıklara dayanarak, aralarındaki ilişkileri analiz edin:

{input}",
            "system_message": "Varlıklar arasındaki ilişkileri analiz etmede uzmansınız."
        },
        {
            "name": "rapor_oluştur",
            "prompt_template": "Bu ilişki analizine dayanarak kısa bir özet rapor oluşturun:

{input}",
            "system_message": "Açık, kısa raporlar oluşturmada uzmansınız."
        }
    ]
    
    chain = SequentialChain(steps=steps, verbose=True)
    
    sample_text = """
    1995 yılında Jeff Bezos, Amazon'u Seattle'da kurdu. Başlangıçta bir çevrimiçi kitapçı olan 
    Amazon, Bezos'un liderliğinde hızla genişledi. 2021 yılına gelindiğinde Amazon, 
    dünyanın en değerli şirketlerinden biri haline gelmişti ve Bezos, dünyanın en zengin kişisi 
    olarak Elon Musk'ı kısa bir süreliğine geçmişti. Tesla ve SpaceX'in CEO'su olan Musk, 
    daha sonra Tesla'nın hisselerinin yükselmesinin ardından zirveyi geri aldı. Bu arada, 
    1975'te Albuquerque'de Bill Gates tarafından kurulan Microsoft, CEO Satya Nadella 
    yönetiminde önemli bir teknoloji rakibi olmaya devam etti.
    """
    
    final_output, all_outputs = chain.run(sample_text)
    
    # Sonuçları görüntüle
    chain.display_chain_results(all_outputs)
    
    # Metrikleri görselleştir
    chain.visualize_metrics()
    
    return final_output, all_outputs


def example_iterative_refiner():
    """Makale yazımı için yinelemeli iyileştirme örneği."""
    # Bir kalite eşiğine dayalı bir durdurma koşulu tanımla
    def quality_threshold(response, metadata):
        # Yanıt 500 jetondan fazlaysa ve gecikme kabul edilebilirse dur
        response_tokens = metadata.get("response_tokens", 0)
        latency = metadata.get("latency", 0)
        return response_tokens > 500 and latency < 5.0
    
    refiner = IterativeRefiner(
        max_iterations=3,
        stopping_condition=quality_threshold,
        verbose=True
    )
    
    prompt = "Yapay zekanın geleceği üzerine kısa bir makale yazın."
    
    final_response, refinement_history = refiner.run(prompt)
    
    # Sonuçları görüntüle
    refiner.display_refinement_history(refinement_history)
    
    # Metrikleri görselleştir
    refiner.visualize_metrics()
    
    return final_response, refinement_history


def example_conditional_brancher():
    """Sorgu yönlendirme için koşullu dallanma örneği."""
    branches = {
        "teknik": {
            "prompt_template": "Bu konuyu uzman bir kitle için teknik, ayrıntılı bir şekilde açıklayın:

{input}",
            "system_message": "Ayrıntılı, hassas açıklamalar sağlayan bir teknik uzmansınız."
        },
        "basitleştirilmiş": {
            "prompt_template": "Bu konuyu 10 yaşındaki bir çocuğun anlayacağı basit terimlerle açıklayın:

{input}",
            "system_message": "Karmaşık konuları basit, erişilebilir bir dilde açıklayan bir eğitimcisiniz."
        },
        "pratik": {
            "prompt_template": "Bu konuda pratik, eyleme geçirilebilir tavsiyeler verin:

{input}",
            "system_message": "Somut, eyleme geçirilebilir rehberlik sağlayan pratik bir danışmansınız."
        }
    }
    
    brancher = ConditionalBrancher(branches=branches, verbose=True)
    
    queries = [
        "Kuantum hesaplama nasıl çalışır?",
        "İklim değişikliği nedir?",
        "Topluluk önünde konuşma becerilerimi nasıl geliştirebilirim?"
    ]
    
    results = []
    for query in queries:
        response, run_details = brancher.run(query)
        results.append((query, response, run_details))
        
        # Sonuçları görüntüle
        brancher.display_branching_results(run_details)
    
    # Metrikleri görselleştir
    brancher.visualize_metrics()
    
    return results


def example_self_critique():
    """Gerçek kontrolü için kendi kendini eleştirme örneği."""
    critique = SelfCritique(
        critique_template="""
        Aşağıdaki soruyu olgusal bilgilerle yanıtlayın:
        
        Soru: {input}
        
        Adım 1: İlgili olduğunu düşündüğünüz tüm bilgileri içeren bir başlangıç yanıtı yazın.
        
        Adım 2: Yanıtınızı eleştirel bir şekilde gözden geçirin. Şunları kontrol edin:
        - Olgusal hatalar veya yanlışlıklar
        - Eksik önemli bilgiler
        - Potansiyel önyargılar veya tek taraflı bakış açıları
        - Emin olmadığınız ve daha az güven ifade etmeniz gereken alanlar
        
        Adım 3: Eleştirinizde belirlediğiniz sorunları gideren iyileştirilmiş bir son yanıt yazın.
        """,
        verbose=True
    )
    
    query = "Birinci Dünya Savaşı'nın başlıca nedenleri nelerdi ve çatışmaya nasıl yol açtılar?"
    
    final_response, run_details = critique.run(query)
    
    # Sonuçları görüntüle
    critique.display_results(run_details)
    
    # Metrikleri görselleştir
    critique.visualize_metrics()
    
    return final_response, run_details


def example_external_validation():
    """Kod üretimi için harici doğrulama örneği."""
    # Python sözdizimi hatalarını kontrol eden basit bir doğrulayıcı işlevi
    def python_validator(code_response):
        # Kod bloklarını çıkar
        import re
        code_blocks = re.findall(r"```python(.*?)```", code_response, re.DOTALL)
        
        if not code_blocks:
            return False, "Yanıtta Python kod bloğu bulunamadı."
        
        # Her bloğu sözdizimi hataları için kontrol et
        for i, block in enumerate(code_blocks):
            try:
                compile(block, "<string>", "exec")
            except SyntaxError as e:
                return False, f"Kod bloğu {i+1}'de sözdizimi hatası: {str(e)}"
        
        return True, "Kod sözdizimi geçerli."
    
    validator = ExternalValidation(
        validator_fn=python_validator,
        max_attempts=3,
        verbose=True
    )
    
    prompt = "Bir dizenin palindrom olup olmadığını kontrol etmek için bir Python işlevi yazın."
    
    final_response, run_details = validator.run(prompt)
    
    # Sonuçları görüntüle
    validator.display_results(run_details)
    
    # Metrikleri görselleştir
    validator.visualize_metrics()
    
    return final_response, run_details


# Ana yürütme (bir betik olarak çalıştırıldığında)
if __name__ == "__main__":
    print("Çok Adımlı LLM Etkileşimleri için Kontrol Döngüleri")
    print("Örnekleri ayrı ayrı çalıştırın veya kendi kullanımınız için sınıfları içe aktarın.")
