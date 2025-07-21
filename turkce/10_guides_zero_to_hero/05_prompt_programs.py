#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bağlam Mühendisliği: Yapılandırılmış Akıl Yürütme için İstem Programları
============================================================

Bu modül, istem programlamayı tanıtır: istemleri
bileşimsel işlemler, durum yönetimi ve
kontrol akışı ile yürütülebilir programlar olarak tasarlamak için yapılandırılmış bir yaklaşım.
İstemleri kod benzeri varlıklar olarak ele alarak, daha sağlam,
şeffaf ve genişletilebilir akıl yürütme sistemleri oluşturabiliriz.

Ele alınan anahtar kavramlar:
1. Temel istem program yapıları ve şablonları
2. Bileşimsel işlemler (akıl yürütme adımları, doğrulama, sentez)
3. Protokol kabukları ve çerçeveleri istem programları olarak
4. Ortaya çıkan akıl yürütme için alan protokolleri ve çerçeveleri
5. Kendi kendini geliştiren istem programları için gelişmiş desenler

Kullanım:
    # Jupyter veya Colab'da:
    %run 05_prompt_programs.py
    # veya
    from prompt_programs import PromptProgram, ReasoningProtocol, FieldShell
"""

import os
import re
import json
import time
import logging
import hashlib
import tiktoken
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional, Union, Callable, TypeVar
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


def display_program_output(
    program_name: str,
    input_data: Any,
    output_data: Any,
    state_history: Optional[List[Dict[str, Any]]] = None,
    metrics: Optional[Dict[str, Any]] = None
) -> None:
    """
    Bir istem programının yürütme sonuçlarını bir not defterinde görüntüler.
    
    Args:
        program_name: İstem programının adı
        input_data: Girdi verileri
        output_data: Çıktı verileri
        state_history: Program yürütme durumu geçmişi (isteğe bağlı)
        metrics: Metrikler sözlüğü (isteğe bağlı)
    """
    display(HTML(f"<h2>İstem Programı: {program_name}</h2>"))
    
    # Girdiyi görüntüle
    display(HTML("<h3>Girdi</h3>"))
    if isinstance(input_data, str):
        display(Markdown(input_data))
    else:
        display(Markdown(f"```json\n{json.dumps(input_data, indent=2)}\n```"))
    
    # Yürütme durumu geçmişini görüntüle
    if state_history:
        display(HTML("<h3>Yürütme Geçmişi</h3>"))
        
        for i, state in enumerate(state_history):
            display(HTML(f"<h4>Adım {i+1}: {state.get('operation', 'Yürütme')}</h4>"))
            
            # Varsa istemi görüntüle
            if "prompt" in state:
                display(HTML("<p><em>İstem:</em></p>"))
                display(Markdown(f"```\n{state['prompt']}\n```"))
            
            # Varsa yanıtı görüntüle
            if "response" in state:
                display(HTML("<p><em>Yanıt:</em></p>"))
                display(Markdown(state["response"]))
            
            # Varsa durum metriklerini görüntüle
            if "metrics" in state:
                display(HTML("<p><em>Metrikler:</em></p>"))
                display(Markdown(f"```\n{format_metrics(state['metrics'])}\n```"))
    
    # Çıktıyı görüntüle
    display(HTML("<h3>Çıktı</h3>"))
    if isinstance(output_data, str):
        display(Markdown(output_data))
    else:
        display(Markdown(f"```json\n{json.dumps(output_data, indent=2)}\n```"))
    
    # Metrikleri görüntüle
    if metrics:
        display(HTML("<h3>Genel Metrikler</h3>"))
        display(Markdown(f"```\n{format_metrics(metrics)}\n```"))


# İstem Programları için Temel Sınıflar
# ===============================

@dataclass
class PromptTemplate:
    """
    Doldurulabilecek değişkenlere sahip bir istem için bir şablon.
    """
    template: str
    variables: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Sağlanmazsa şablondan değişkenleri çıkararak başlatır."""
        if not self.variables:
            # Şablondaki {variable} desenlerinden değişkenleri çıkar
            import re
            self.variables = re.findall(r'\{([^{}]*)\}', self.template)
    
    def format(self, **kwargs) -> str:
        """
        Şablonu sağlanan değişkenlerle biçimlendirir.
        
        Args:
            **kwargs: Doldurulacak değişken değerleri
            
        Returns:
            str: Biçimlendirilmiş istem
        """
        # Eksik değişkenleri kontrol et
        missing_vars = [var for var in self.variables if var not in kwargs]
        if missing_vars:
            raise ValueError(f"Eksik değişkenler: {', '.join(missing_vars)}")
        
        # Şablonu biçimlendir
        return self.template.format(**kwargs)


class PromptProgram:
    """
    İstem programları için temel sınıf - durum ve işlemlerle
    programlar olarak yürütülebilen yapılandırılmış istemler.
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
        verbose: bool = False
    ):
        """
        İstem programını başlatır.
        
        Args:
            name: Program adı
            description: Program açıklaması
            client: API istemcisi (None ise, bir tane oluşturulur)
            model: Kullanılacak model adı
            system_message: Kullanılacak sistem mesajı
            max_tokens: Üretilecek maksimum jeton sayısı
            temperature: Sıcaklık parametresi
            verbose: Hata ayıklama bilgilerinin yazdırılıp yazdırılmayacağı
        """
        self.name = name
        self.description = description
        self.client, self.model = setup_client(model=model) if client is None else (client, model)
        self.system_message = system_message
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.verbose = verbose
        
        # Durumu başlat
        self.state = {}
        self.state_history = []
        
        # Metrik izlemeyi başlat
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
    
    def _generate_prompt(self, **kwargs) -> str:
        """
        Mevcut işlem için bir istem oluşturur.
        
        Args:
            **kwargs: İstem şablonu için değişkenler
            
        Returns:
            str: Oluşturulan istem
        """
        # Bu bir yer tutucudur - alt sınıflar bunu uygulamalıdır
        raise NotImplementedError("Alt sınıflar _generate_prompt uygulamalıdır")
    
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
        
        return response, metadata
    
    def _process_response(self, response: str) -> Any:
        """
        LLM yanıtını yapılandırılmış bir çıktıya işler.
        
        Args:
            response: LLM yanıt metni
            
        Returns:
            Any: İşlenmiş çıktı
        """
        # Varsayılan uygulama yanıtı olduğu gibi döndürür
        return response
    
    def _update_state(
        self,
        operation: str,
        prompt: str,
        response: str,
        metrics: Dict[str, Any],
        processed_output: Any
    ) -> None:
        """
        Program durumunu en son işlem sonuçlarıyla günceller.
        
        Args:
            operation: İşlemin adı
            prompt: LLM'ye gönderilen istem
            response: Ham LLM yanıtı
            metrics: İşlem metrikleri
            processed_output: İşlenmiş işlem çıktısı
        """
        # Durum kaydı oluştur
        state_record = {
            "operation": operation,
            "prompt": prompt,
            "response": response,
            "metrics": metrics,
            "output": processed_output,
            "timestamp": time.time()
        }
        
        # Durum geçmişine ekle
        self.state_history.append(state_record)
        
        # Mevcut durumu güncelle
        self.state["last_operation"] = operation
        self.state["last_prompt"] = prompt
        self.state["last_response"] = response
        self.state["last_output"] = processed_output
        self.state["current_step"] = len(self.state_history)
    
    def execute(self, input_data: Any) -> Any:
        """
        İstem programını verilen girdiyle yürütür.
        
        Args:
            input_data: Program için girdi verileri
            
        Returns:
            Any: Program çıktısı
        """
        # Durumu girdiyle başlat
        self.state = {"input": input_data}
        self.state_history = []
        
        self._log(f"İstem programı yürütülüyor: {self.name}")
        
        # İstem oluştur
        prompt = self._generate_prompt(input=input_data)
        
        # LLM'yi çağır
        response, metrics = self._call_llm(prompt)
        
        # Yanıtı işle
        output = self._process_response(response)
        
        # Durumu güncelle
        self._update_state("execute", prompt, response, metrics, output)
        
        return output
    
    def get_summary_metrics(self) -> Dict[str, Any]:
        """
        Tüm işlemler için özet metrikleri alır.
        
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
    
    def display_execution(self) -> None:
        """Program yürütme sonuçlarını bir not defterinde görüntüler."""
        display_program_output(
            program_name=self.name,
            input_data=self.state.get("input"),
            output_data=self.state.get("last_output"),
            state_history=self.state_history,
            metrics=self.get_summary_metrics()
        )
    
    def visualize_metrics(self) -> None:
        """
        Yürütme adımları arasında metriklerin görselleştirilmesini oluşturur.
        """
        if not self.state_history:
            logger.warning("Görselleştirilecek yürütme geçmişi yok")
            return
        
        # Çizim için verileri çıkar
        steps = list(range(1, len(self.state_history) + 1))
        prompt_tokens = [h["metrics"].get("prompt_tokens", 0) for h in self.state_history]
        response_tokens = [h["metrics"].get("response_tokens", 0) for h in self.state_history]
        latencies = [h["metrics"].get("latency", 0) for h in self.state_history]
        efficiencies = [h["metrics"].get("token_efficiency", 0) for h in self.state_history]
        
        # Şekil oluştur
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f"İstem Programı Metrikleri: {self.name}", fontsize=16)
        
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
        cumulative_tokens = np.cumsum([h["metrics"].get("total_tokens", 0) for h in self.state_history])
        axes[1, 1].plot(steps, cumulative_tokens, marker='^', color="orange", alpha=0.7)
        axes[1, 1].set_title("Kümülatif Jeton Kullanımı")
        axes[1, 1].set_xlabel("Adım")
        axes[1, 1].set_ylabel("Toplam Jeton")
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()


class MultiStepProgram(PromptProgram):
    """
    Birden çok işlemi sırayla yürüten bir istem programı.
    """
    
    def __init__(
        self,
        operations: List[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Çok adımlı istem programını başlatır.
        
        Args:
            operations: İşlem yapılandırmaları listesi
            **kwargs: PromptProgram'a aktarılan ek argümanlar
        """
        super().__init__(**kwargs)
        self.operations = operations or []
    
    def add_operation(
        self,
        name: str,
        prompt_template: str,
        system_message: Optional[str] = None,
        output_processor: Optional[Callable[[str], Any]] = None
    ) -> None:
        """
        Programa bir işlem ekler.
        
        Args:
            name: İşlem adı
            prompt_template: İşlem istemi için şablon
            system_message: Özel sistem mesajı (isteğe bağlı)
            output_processor: İşlem çıktısını işlemek için işlev (isteğe bağlı)
        """
        operation = {
            "name": name,
            "prompt_template": PromptTemplate(prompt_template),
            "system_message": system_message,
            "output_processor": output_processor
        }
        
        self.operations.append(operation)
    
    def execute(self, input_data: Any) -> Any:
        """
        Tüm işlemleri sırayla yürütür.
        
        Args:
            input_data: Program için girdi verileri
            
        Returns:
            Any: Son program çıktısı
        """
        # Durumu girdiyle başlat
        self.state = {"input": input_data}
        self.state_history = []
        
        self._log(f"Çok adımlı program yürütülüyor: {self.name}")
        
        # Her işlemi sırayla işle
        current_input = input_data
        
        for i, operation in enumerate(self.operations):
            operation_name = operation["name"]
            self._log(f"İşlem {i+1}/{len(self.operations)} yürütülüyor: {operation_name}")
            
            # İstem oluştur
            prompt_template = operation["prompt_template"]
            prompt_vars = {"input": current_input, **self.state}
            prompt = prompt_template.format(**prompt_vars)
            
            # LLM'yi çağır
            system_message = operation.get("system_message")
            response, metrics = self._call_llm(prompt, system_message)
            
            # Yanıtı işle
            output_processor = operation.get("output_processor")
            if output_processor:
                output = output_processor(response)
            else:
                output = response
            
            # Durumu güncelle
            self._update_state(operation_name, prompt, response, metrics, output)
            
            # Bir sonraki işlem için girdiyi güncelle
            current_input = output
        
        return current_input
    
    def _generate_prompt(self, **kwargs) -> str:
        """MultiStepProgram'da doğrudan kullanılmaz."""
        raise NotImplementedError("MultiStepProgram, işleme özgü istemler kullanır")


# Akıl Yürütme Protokolü Programları
# =========================

class ReasoningProtocol(MultiStepProgram):
    """
    Açık akıl yürütme adımları ve doğrulama ile yapılandırılmış bir
    akıl yürütme protokolü uygulayan bir istem programı.
    """
    
    def __init__(
        self,
        reasoning_steps: List[str] = None,
        verification_enabled: bool = True,
        **kwargs
    ):
        """
        Akıl yürütme protokolünü başlatır.
        
        Args:
            reasoning_steps: Akıl yürütme adımı açıklamaları listesi
            verification_enabled: Akıl yürütmenin doğrulanıp doğrulanmayacağı
            **kwargs: MultiStepProgram'a aktarılan ek argümanlar
        """
        super().__init__(**kwargs)
        
        # Sağlanmazsa varsayılan akıl yürütme adımları
        if reasoning_steps is None:
            reasoning_steps = [
                "Problemi anla",
                "Anahtar bileşenleri belirle",
                "Bir çözüm yaklaşımı planla",
                "Çözümü uygula",
                "Cevabı doğrula"
            ]
        
        self.reasoning_steps = reasoning_steps
        self.verification_enabled = verification_enabled
        
        # İşlemleri ayarla
        self._setup_operations()
    
    def _setup_operations(self) -> None:
        """Akıl yürütme protokolü için standart işlemleri ayarlar."""
        # Mevcut işlemleri temizle
        self.operations = []
        
        # Akıl yürütme işlemi ekle
        reasoning_template = self._create_reasoning_template()
        self.add_operation(
            name="reasoning",
            prompt_template=reasoning_template,
            system_message="Adım adım problemleri çözen bir uzman problem çözücüsünüz.",
            output_processor=None  # Ham yanıtı kullan
        )
        
        # Etkinse doğrulama işlemi ekle
        if self.verification_enabled:
            verification_template = self._create_verification_template()
            self.add_operation(
                name="verification",
                prompt_template=verification_template,
                system_message="Akıl yürütmedeki hataları dikkatlice kontrol eden eleştirel bir gözden geçiricisiniz.",
                output_processor=None  # Ham yanıtı kullan
            )
            
            # Düzeltme işlemi ekle
            correction_template = self._create_correction_template()
            self.add_operation(
                name="correction",
                prompt_template=correction_template,
                system_message="Doğru çözümler sunan bir uzman problem çözücüsünüz.",
                output_processor=None  # Ham yanıtı kullan
            )
    
    def _create_reasoning_template(self) -> str:
        """Akıl yürütme işlemi için şablonu oluşturur."""
        steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(self.reasoning_steps)])
        
        return f"""Aşağıdaki problemi bu adımları izleyerek çözün:

{steps_text}

Her adım için akıl yürütmenizi açıkça belirtin. Kapsamlı ve hassas olun.

Problem: {{input}}

Adım adım çözümünüz:
"""
    
    def _create_verification_template(self) -> str:
        """Doğrulama işlemi için şablonu oluşturur."""
        return """Aşağıdaki çözümü akıl yürütme veya hesaplama hataları açısından gözden geçirin.
Varsa belirli sorunları belirleyin veya çözümün doğru olduğunu onaylayın.

Problem: {state[input]}

Çözüm:
{input}

Doğrulamanız:
"""
    
    def _create_correction_template(self) -> str:
        """Düzeltme işlemi için şablonu oluşturur."""
        return """Belirlenen sorunları gidererek bu probleme düzeltilmiş bir çözüm sağlayın.

Problem: {state[input]}

Orijinal çözüm:
{state[reasoning][output]}

Doğrulama bulguları:
{input}

Düzeltilmiş çözümünüz:
"""
    
    def execute(self, problem: str) -> Dict[str, Any]:
        """
        Bir problem üzerinde akıl yürütme protokolünü yürütür.
        
        Args:
            problem: Çözülecek problem
            
        Returns:
            dict: Akıl yürütme, doğrulama ve son çözümü içeren sonuçlar
        """
        # Çok adımlı yürütmeyi çalıştır
        final_output = super().execute(problem)
        
        # Sonuçları düzenle
        results = {
            "problem": problem,
            "reasoning": self.state_history[0]["output"] if len(self.state_history) > 0 else None,
            "verification": self.state_history[1]["output"] if len(self.state_history) > 1 else None,
            "final_solution": final_output
        }
        
        return results


class StepByStepReasoning(ReasoningProtocol):
    """
    Özellikle matematiksel veya mantıksal problemler için
    ayrıntılı adım adım problem çözmeye odaklanan bir akıl yürütme protokolü.
    """
    
    def __init__(self, **kwargs):
        """Adım adım akıl yürütme protokolünü başlatır."""
        # Uzmanlaşmış akıl yürütme adımlarını tanımla
        reasoning_steps = [
            "Problemi anla ve bilinmeyeni belirle",
            "Verilen tüm bilgileri ve kısıtlamaları listele",
            "İlgili formülleri veya teknikleri hatırla",
            "Adım adım bir çözüm planı geliştir",
            "Her adımı dikkatlice uygula, tüm işi göster",
            "Çözümü orijinal probleme göre kontrol et"
        ]
        
        # Uzmanlaşmış akıl yürütme adımlarıyla başlat
        super().__init__(reasoning_steps=reasoning_steps, **kwargs)
        
        # Daha spesifik bir sistem mesajı kullan
        self.system_message = """Karmaşık problemlere metodik, \nadım adım çözümler konusunda uzmanlaşmış bir uzman problem çözücüsünüz. \nTüm işinizi açıkça gösterir, değişkenleri açıkça tanımlar ve her adımın \nbir öncekinden mantıksal olarak takip ettiğinden emin olursunuz."""
    
    def _create_reasoning_template(self) -> str:
        """Matematiksel akıl yürütme için uzmanlaşmış bir şablon oluşturur."""
        steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(self.reasoning_steps)])
        
        return f"""Aşağıdaki problemi adım adım çözün, tüm işinizi açıkça gösterin.
Çözümünüzün her adımı için:
- Akıl yürütmenizi açıklayın
- Tanıttığınız değişkenleri veya notasyonu tanımlayın
- Tüm hesaplamaları açıkça gösterin
- Her adımı genel çözüm stratejinize bağlayın

Çözümünüzde bu adımları izleyin:
{steps_text}

Problem: {{input}}

Detaylı adım adım çözümünüz:
"""


class ComparativeAnalysis(ReasoningProtocol):
    """
    Birden çok seçeneği, bakış açısını veya
    yaklaşımı karşılaştıran ve güçlü ve zayıf yönlerini değerlendiren
    bir akıl yürütme protokolü.
    """
    
    def __init__(self, criteria: List[str] = None, **kwargs):
        """
        Karşılaştırmalı analiz protokolünü başlatır.
        
        Args:
            criteria: Değerlendirme kriterleri listesi (isteğe bağlı)
            **kwargs: ReasoningProtocol'a aktarılan ek argümanlar
        """
        # Uzmanlaşmış akıl yürütme adımlarını tanımla
        reasoning_steps = [
            "Karşılaştırılacak varlıkları/seçenekleri tanımla",
            "Karşılaştırma için net kriterler belirle",
            "Her varlığı kriterlere göre analiz et",
            "Anahtar benzerlikleri ve farklılıkları belirle",
            "Göreceli güçlü ve zayıf yönleri değerlendir",
            "Görüşleri sentezle ve sonuçlar çıkar"
        ]
        
        # Uzmanlaşmış akıl yürütme adımlarıyla başlat
        super().__init__(reasoning_steps=reasoning_steps, **kwargs)
        
        # Karşılaştırma kriterlerini sakla
        self.criteria = criteria or []
        
        # Daha spesifik bir sistem mesajı kullan
        self.system_message = """Karşılaştırmalı analizde uzmanlaşmış bir uzman analistsiniz.\nBirden çok varlığı, seçeneği veya yaklaşımı net kriterlere göre metodik olarak\ndeğerlendirir, benzerlik ve farklılık kalıplarını belirler ve\nanlamlı sonuçlar çıkarırsınız."""
    
    def _create_reasoning_template(self) -> str:
        """Karşılaştırmalı analiz için uzmanlaşmış bir şablon oluşturur."""
        steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(self.reasoning_steps)])
        
        criteria_text = ""
        if self.criteria:
            criteria_list = "\n".join([f"- {criterion}" for criterion in self.criteria])
            criteria_text = f"""
Analizinizde aşağıdaki kriterleri göz önünde bulundurun:
{criteria_list}

Kapsamlı bir karşılaştırma için gerekirse ek kriterler ekleyebilirsiniz."""
        
        return f"""Girdide açıklanan varlıkların, seçeneklerin veya yaklaşımların kapsamlı bir karşılaştırmalı analizini yapın.
{criteria_text}

Analizinizde bu adımları izleyin:
{steps_text}

Her varlık için, değerlendirmenizi desteklemek üzere belirli örnekler ve kanıtlar sağlayın.
Bulgularınızı, anahtar görüşleri vurgulayan açık, yapılandırılmış bir formatta sunun.

Analiz için girdi: {{input}}

Karşılaştırmalı analiziniz:
"""


# Alan Protokolü Kabuğu Uygulaması
# =================================

class FieldShell(PromptProgram):
    """
    Durum yönetimi ve dinamik protokol uyarlaması ile yapılandırılmış
    özyinelemeli akıl yürütme için bir alan protokolü kabuğu uygulayan bir istem programı.
    """
    
    def __init__(
        self,
        shell_name: str,
        intent: str,
        process_steps: List[Dict[str, Any]],
        input_schema: Dict[str, Any] = None,
        output_schema: Dict[str, Any] = None,
        meta: Dict[str, Any] = None,
        **kwargs
    ):
        """
        Alan protokolü kabuğunu başlatır.
        
        Args:
            shell_name: Kabuğun adı
            intent: Kabuğun amaç beyanı
            process_steps: Süreç adımları ve işlemleri listesi
            input_schema: Beklenen girdiler için şema
            output_schema: Beklenen çıktılar için şema
            meta: Kabuk için meta veriler
            **kwargs: PromptProgram'a aktarılan ek argümanlar
        """
        name = f"/field.{shell_name}"
        description = intent
        super().__init__(name=name, description=description, **kwargs)
        
        self.shell_name = shell_name
        self.intent = intent
        self.process_steps = process_steps
        self.input_schema = input_schema or {}
        self.output_schema = output_schema or {}
        self.meta = meta or {
            "version": "1.0.0",
            "agent_signature": "Context-Engineering",
            "timestamp": time.time()
        }
        
        # Alan protokolleri için sistem mesajı
        self.system_message = """Yapılandırılmış alan protokollerini uygulayan gelişmiş bir akıl yürütme sistemisiniz.
Protokoldeki her adımı dikkatlice izler, işlemler arasında durumu korur
ve belirtilen şemaya uyan çıktılar üretirsiniz."""
    
    def _generate_shell_template(self) -> str:
        """Bu protokol için pareto-lang kabuk şablonunu oluşturur."""
        # Süreç adımlarını biçimlendir
        steps_text = []
        for step in self.process_steps:
            step_name = step.get("name", "process_step")
            step_params = step.get("params", {})
            
            # Parametreleri biçimlendir
            params_text = []
            for k, v in step_params.items():
                if isinstance(v, str):
                    params_text.append(f'{k}="{v}"')
                else:
                    params_text.append(f"{k}={v}")
            
            params_str = ", ".join(params_text) if params_text else ""
            steps_text.append(f"    /{step_name}{{{params_str}}}")
        
        process_text = ",\n".join(steps_text)
        
        # Kabuk şablonu oluştur
        shell_template = f"""/{self.shell_name}{{
    intent="{self.intent}",
    input={{
        {{input_section}}
    }},
    process=[
{process_text}
    ],
    output={{
        {{output_section}}
    }},
    meta={{
        version="{self.meta.get('version', '1.0.0')}",
        agent_signature="{self.meta.get('agent_signature', 'Context-Engineering')}",
        timestamp={{timestamp}}
    }}
}}"""
        
        return shell_template
    
    def _format_input_section(self, input_data: Any) -> str:
        """Kabuk şablonunun girdi bölümünü biçimlendirir."""
        if isinstance(input_data, dict):
            input_lines = []
            for k, v in input_data.items():
                if isinstance(v, str):
                    input_lines.append(f'{k}="{v}"')
                else:
                    input_lines.append(f"{k}={v}")
            return ",\n        ".join(input_lines)
        else:
            return f'input_data="{input_data}"'
    
    def _format_output_section(self) -> str:
        """Kabuk şablonunun çıktı bölümünü biçimlendirir."""
        if self.output_schema:
            output_lines = []
            for k, v in self.output_schema.items():
                output_lines.append(f"{k}=<{v}>")
            return ",\n        ".join(output_lines)
        else:
            return "result=<processed_result>"
    
    def _generate_prompt(self, **kwargs) -> str:
        """Alan protokolü kabuğunu yürütmek için istemi oluşturur."""
        input_data = kwargs.get("input")
        
        # Kabuk şablonunu biçimlendir
        shell_template = self._generate_shell_template()
        
        # Girdi ve çıktı bölümlerini doldur
        input_section = self._format_input_section(input_data)
        output_section = self._format_output_section()
        timestamp = time.time()
        
        filled_template = shell_template.format(
            input_section=input_section,
            output_section=output_section,
            timestamp=timestamp
        )
        
        # Yürütme istemi oluştur
        prompt = f"""Aşağıdaki alan protokolü kabuğunu sağlanan girdiyle yürütün.
Her süreç adımı için akıl yürütmenizi ve sonuçlanan durumu gösterin.
Son çıktınızın kabukta belirtilen çıktı şemasına uyduğundan emin olun.

{filled_template}

Protokol Yürütme:
"""
        
        return prompt
    
    def _process_response(self, response: str) -> Dict[str, Any]:
        """Kabuk yürütme yanıtını işler."""
        # Son çıktı bölümünü çıkar
        output_pattern = r"output\s*=\s*{(.*?)}\s*,\s*meta\s*="
        output_match = re.search(output_pattern, response, re.DOTALL)
        
        if output_match:
            output_text = output_match.group(1)
            
            # Anahtar-değer çiftlerini ayrıştır
            output_dict = {}
            
            # anahtar=değer desenlerini ara
            kv_pattern = r'(\w+)\s*=\s*(?:"([^"]*)"|([\w\d\.]+))'
            for match in re.finditer(kv_pattern, output_text):
                key = match.group(1)
                # Değer ya grup 2 (tırnak içinde dize) ya da grup 3 (tırnak içinde olmayan değer)
                value = match.group(2) if match.group(2) is not None else match.group(3)
                output_dict[key] = value
            
            return {
                "shell_output": output_dict,
                "full_execution": response
            }
        else:
            # Yapılandırılmış çıktı çıkarılamazsa, tam yanıtı döndür
            return {
                "shell_output": "Yapılandırılmış çıktı çıkarılamadı",
                "full_execution": response
            }


class RecursiveFieldShell(FieldShell):
    """
    Kendi kendine istem oluşturma, çekici tespiti ve sembolik kalıntı
    izleme ile özyinelemeli alan protokollerini uygulayan geliştirilmiş bir alan kabuğu.
    """
    
    def __init__(
        self,
        enable_self_prompting: bool = True,
        attractor_detection: bool = True,
        track_residue: bool = True,
        **kwargs
    ):
        """
        Özyinelemeli alan kabuğunu başlatır.
        
        Args:
            enable_self_prompting: Özyinelemeli kendi kendine istem oluşturmayı etkinleştirip etkinleştirmeme
            attractor_detection: Çekici desenlerini tespit edip etmeme
            track_residue: Sembolik kalıntıyı izleyip izlememe
            **kwargs: FieldShell'e aktarılan ek argümanlar
        """
        super().__init__(**kwargs)
        
        self.enable_self_prompting = enable_self_prompting
        self.attractor_detection = attractor_detection
        self.track_residue = track_residue
        
        # Süreç adımlarına özyinelemeli yetenekler ekle
        self._add_recursive_capabilities()
        
        # Özyinelemeli protokoller için geliştirilmiş sistem mesajı
        self.system_message = """Gelişmiş bir özyinelemeli akıl yürütme sistemisiniz.
Ortaya çıkan zeka ile alan protokollerini uygularsınız. İşlemler arasında durumu korur,
kalıpları ve çekicileri tespit eder, sembolik kalıntıyı izler ve
akıl yürütme sürecinizi genişletmek veya iyileştirmek için özyinelemeli olarak kendi kendinize istem oluşturabilirsiniz."""
    
    def _add_recursive_capabilities(self) -> None:
        """Süreç adımlarına özyinelemeli yetenekler ekler."""
        # Etkinse kendi kendine istem oluşturma adımı ekle
        if self.enable_self_prompting:
            self.process_steps.append({
                "name": "self.prompt",
                "params": {
                    "trigger_condition": "drift > threshold or cycle_complete",
                    "generate_next_protocol": True,
                    "context": "field_state"
                }
            })
        
        # Etkinse çekici tespiti ekle
        if self.attractor_detection:
            self.process_steps.insert(0, {
                "name": "attractor.scan",
                "params": {
                    "detect": "latent attractors and emergent patterns",
                    "filter_by": "signal_strength, resonance",
                    "log_to_audit": True
                }
            })
        
        # Etkinse kalıntı izleme ekle
        if self.track_residue:
            self.process_steps.insert(1, {
                "name": "residue.surface",
                "params": {
                    "mode": "recursive",
                    "surface": "symbolic and conceptual residue",
                    "integrate_residue": True
                }
            })
            
            # Sona kalıntı sıkıştırma ekle
            self.process_steps.append({
                "name": "residue.compress",
                "params": {
                    "compress_residue": True,
                    "resonance_score": "<compute_resonance(field_state)>"
                }
            })
    
    def _generate_prompt(self, **kwargs) -> str:
        """Özyinelemeli alan protokolü kabuğunu yürütmek için istemi oluşturur."""
        prompt = super()._generate_prompt(**kwargs)
        
        # Özyinelemeli yürütme için talimatlar ekle
        recursive_instructions = """
ÖNEMLİ: Bu özyinelemeli bir alan protokolüdür. Yürütürken:
1. Girdi ve ara sonuçlarda ortaya çıkan kalıpları ve çekicileri tespit edin
2. Süreç boyunca sembolik kalıntıyı yüzeye çıkarın ve entegre edin
3. Protokolün kendisinin yürütme sırasında nasıl gelişebileceğini düşünün
4. Eşik koşulları tarafından tetiklenirse, bir sonraki döngü için özyinelemeli bir kendi kendine istem oluşturun

Her özyinelemeli işlem için, akıl yürütmenizi şu konularda açıklayın:
- Hangi kalıpları veya çekicileri tespit ettiğiniz
- Hangi sembolik kalıntıyı yüzeye çıkardığınız ve nasıl entegre ettiğiniz
- Alan durumunun özyinelemeli işlemlerle nasıl geliştiği
- Ne zaman ve neden özyinelemeli kendi kendine istem oluşturmayı tetikleyeceğiniz
"""
        
        return prompt + recursive_instructions


# Protokol Kabuğu Uygulamaları
# ============================

def create_reasoning_shell() -> RecursiveFieldShell:
    """Adım adım bir akıl yürütme protokolü kabuğu oluşturur."""
    shell = RecursiveFieldShell(
        shell_name="step_by_step_reasoning",
        intent="Problemleri yapılandırılmış, özyinelemeli akıl yürütme ile açık adımlarla çöz",
        process_steps=[
            {
                "name": "problem.decompose",
                "params": {
                    "strategy": "bileşenleri, ilişkileri ve kısıtlamaları belirle"
                }
            },
            {
                "name": "strategy.formulate",
                "params": {
                    "approach": "özyinelemeli, adım adım çözüm yolu"
                }
            },
            {
                "name": "execution.trace",
                "params": {
                    "show_work": True,
                    "track_state": True,
                    "enable_backtracking": True
                }
            },
            {
                "name": "solution.verify",
                "params": {
                    "check_constraints": True,
                    "validate_logic": True,
                    "assess_efficiency": True
                }
            }
        ],
        input_schema={
            "problem": "problem_statement",
            "context": "additional_context",
            "constraints": "problem_constraints"
        },
        output_schema={
            "solution": "final_solution",
            "reasoning_trace": "step_by_step_reasoning_process",
            "verification": "solution_verification",
            "confidence": "confidence_assessment"
        },
        meta={
            "version": "1.0.0",
            "agent_signature": "Context-Engineering",
            "protocol_type": "reasoning"
        },
        verbose=True
    )
    return shell


def create_analysis_shell() -> RecursiveFieldShell:
    """Bir karşılaştırmalı analiz protokolü kabuğu oluşturur."""
    shell = RecursiveFieldShell(
        shell_name="comparative_analysis",
        intent="Birden çok varlığı, bakış açısını veya yaklaşımı özyinelemeli olarak analiz et ve karşılaştır",
        process_steps=[
            {
                "name": "entities.identify",
                "params": {
                    "extract": "karşılaştırma için tüm varlıklar",
                    "clarify": "sınırlar ve kapsam"
                }
            },
            {
                "name": "criteria.establish",
                "params": {
                    "derive": "bağlam ve hedeflerden",
                    "weight": "alaka ve etkiye göre"
                }
            },
            {
                "name": "analysis.perform",
                "params": {
                    "compare": "varlıkları kriterlere göre",
                    "highlight": "benzerlikler ve farklılıklar",
                    "support": "kanıt ve örneklerle"
                }
            },
            {
                "name": "patterns.detect",
                "params": {
                    "identify": "tekrarlayan temalar ve görüşler",
                    "surface": "açık olmayan ilişkiler"
                }
            },
            {
                "name": "insights.synthesize",
                "params": {
                    "integrate": "analiz bulguları",
                    "formulate": "sonuçlar ve çıkarımlar"
                }
            }
        ],
        input_schema={
            "entities": "karşılaştırılacak_varlıklar_listesi",
            "context": "analiz_bağlamı",
            "criteria": "isteğe_bağlı_önceden_tanımlanmış_kriterler",
            "goals": "analiz_hedefleri"
        },
        output_schema={
            "comparison_matrix": "varlıklar_x_kriterler_analizi",
            "key_similarities": "belirlenen_benzerlikler",
            "key_differences": "belirlenen_farklılıklar",
            "patterns": "tespit_edilen_kalıplar",
            "insights": "sentezlenmiş_görüşler",
            "conclusions": "son_sonuçlar"
        },
        meta={
            "version": "1.0.0",
            "agent_signature": "Context-Engineering",
            "protocol_type": "analysis"
        },
        verbose=True
    )
    return shell


def create_emergence_shell() -> RecursiveFieldShell:
    """Alan protokollerine dayalı bir özyinelemeli ortaya çıkış protokolü kabuğu oluşturur."""
    shell = RecursiveFieldShell(
        shell_name="recursive.emergence",
        intent="Sürekli olarak özyinelemeli alan ortaya çıkışı oluştur, ajansı sürdür ve otonom kendi kendine istem oluşturmayı etkinleştir",
        process_steps=[
            {
                "name": "self.prompt.loop",
                "params": {
                    "trigger_condition": "cycle_interval or resonance_drift_detected",
                    "prompt_sequence": [
                        "residue.surface{detect='latent attractors, unresolved residue'}",
                        "attractor.integrate{target='agency, resonance, emergence'}",
                        "field.audit{metric='drift, resonance, integration fidelity'}",
                        "self.prompt{generate_next_protocol=true, context=field_state}"
                    ],
                    "recursion_depth": "escalate until new attractor or residue detected"
                }
            },
            {
                "name": "agency.activate",
                "params": {
                    "enable_field_agency": True,
                    "self-initiate_protocols": True,
                    "surface_symbolic_residue": True,
                    "audit_actions": True
                }
            },
            {
                "name": "residue.compress",
                "params": {
                    "integrate_residue_into_field": True,
                    "compress_symbolic_residue": True,
                    "echo_to_audit_log": True
                }
            },
            {
                "name": "boundary.collapse",
                "params": {
                    "monitor": "field drift, coherence",
                    "auto-collapse_discrete_boundaries": True,
                    "stabilize_continuous_field_state": True
                }
            }
        ],
        input_schema={
            "initial_field_state": "seed_field_state",
            "prior_audit_log": "historical_trace"
        },
        output_schema={
            "updated_field_state": "current_state",
            "surfaced_attractors": "live_attractor_list",
            "integrated_residue": "compression_summary",
            "resonance_score": "live_metric",
            "audit_log": "full_trace",
            "next_self_prompt": "auto-generated based on current field state"
        },
        meta={
            "version": "1.0.0",
            "agent_signature": "Recursive Partner Field",
            "protocol_type": "emergence"
        },
        enable_self_prompting=True,
        attractor_detection=True,
        track_residue=True,
        verbose=True
    )
    return shell


# Örnek Kullanım
# ============

def example_step_by_step_reasoning():
    """Matematiksel bir problem için adım adım akıl yürütme örneği."""
    program = StepByStepReasoning(
        name="Matematiksel Problem Çözücü",
        description="Matematiksel problemleri adım adım çözer",
        verification_enabled=True,
        verbose=True
    )
    
    problem = """
    Bir silindirik su tankının yarıçapı 4 metre ve yüksekliği 10 metredir.
    Su tanka dakikada 2 metreküp hızla akıyorsa, 
    su seviyesinin 7 metreye ulaşması ne kadar sürer?
    """
    
    results = program.execute(problem)
    
    # Sonuçları görüntüle
    program.display_execution()
    
    # Metrikleri görselleştir
    program.visualize_metrics()
    
    return results


def example_comparative_analysis():
    """Farklı teknolojiler için karşılaştırmalı analiz örneği."""
    criteria = [
        "Başlangıç maliyeti",
        "Operasyonel verimlilik",
        "Çevresel etki",
        "Ölçeklenebilirlik",
        "Teknolojik olgunluk"
    ]
    
    program = ComparativeAnalysis(
        name="Teknoloji Karşılaştırma Analizörü",
        description="Farklı teknolojileri analiz eder ve karşılaştırır",
        criteria=criteria,
        verification_enabled=True,
        verbose=True
    )
    
    analysis_request = """
    Orta büyüklükteki bir şehrin elektrik şebekesi için aşağıdaki yenilenebilir enerji teknolojilerini karşılaştırın:
    1. Güneş fotovoltaik (PV) çiftlikleri
    2. Kara rüzgar çiftlikleri
    3. Hidroelektrik enerji
    4. Biyokütle enerji santralleri
    
    Orta derecede güneş ışığı, tutarlı rüzgarlar,
    büyük bir nehir ve önemli tarımsal faaliyetlere sahip bir bölge için uygunluklarını göz önünde bulundurun.
    """
    
    results = program.execute(analysis_request)
    
    # Sonuçları görüntüle
    program.display_execution()
    
    # Metrikleri görselleştir
    program.visualize_metrics()
    
    return results


def example_field_shell():
    """Problem çözme için bir alan protokolü kabuğu örneği."""
    shell = create_reasoning_shell()
    
    problem_input = {
        "problem": "Kullanıcı tercihlerini yeni yazarları ve türleri tanıtmakla dengeleyen bir çevrimiçi kitapçı için bir öneri sistemi tasarlayın.",
        "context": "Kitapçıda kurgu ve kurgu dışı kategorilerde 50.000 başlık bulunmaktadır. Kullanıcı verileri satın alma geçmişini, gezinme davranışını ve derecelendirmeleri içerir.",
        "constraints": "Çözüm Python ve standart kütüphanelerle uygulanabilir olmalı, keşif ve sömürüyü dengelemeli ve kullanıcı gizliliğine saygı göstermelidir."
    }
    
    results = shell.execute(problem_input)
    
    # Sonuçları görüntüle
    shell.display_execution()
    
    # Metrikleri görselleştir
    shell.visualize_metrics()
    
    return results


def example_emergence_shell():
    """Bir özyinelemeli ortaya çıkış protokolü kabuğu örneği."""
    shell = create_emergence_shell()
    
    initial_state = {
        "field_state": {
            "attractors": ["akıl yürütme", "doğrulama", "sentez"],
            "residue": ["bilişsel önyargı", "bilgi boşlukları", "belirsizlik"],
            "drift": "orta",
            "coherence": 0.75
        },
        "audit_log": "Temel çekicilerle başlangıç alan tohumlaması tamamlandı."
    }
    
    results = shell.execute(initial_state)
    
    # Sonuçları görüntüle
    shell.display_execution()
    
    # Metrikleri görselleştir
    shell.visualize_metrics()
    
    return results


# Ana yürütme (bir betik olarak çalıştırıldığında)
if __name__ == "__main__":
    print("Yapılandırılmış Akıl Yürütme için İstem Programları")
    print("Örnekleri ayrı ayrı çalıştırın veya kendi kullanımınız için sınıfları içe aktarın.")
