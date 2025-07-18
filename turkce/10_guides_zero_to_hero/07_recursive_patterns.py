#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Özyinelemeli Desenler: Kendi Kendini Geliştiren Bağlamlar
=========================================================

Bu modül, bağlam mühendisliğinde özyinelemeli desenleri inceler: LLM'lerin
kendi bağlamlarını genişletme, iyileştirme ve evrimleştirmesi için yaklaşım ve
şablonlar sunar. Bu desenler, istemler içinde geri bildirim döngüleri oluşturarak
iteratif iyileştirme, kendi kendini doğrulama ve ortaya çıkan yetenekleri sağlar.

Ele alınan ana kavramlar:
1. Temel özyinelemeli desenler (öz-yansıma, bootstrapping)
2. Alan protokolleri ve kabuklar olarak özyinelemeli çerçeveler
3. Sembolik kalıntı ve durum takibi
4. Sınır çöküşü ve gradyan sistemleri
5. Ortaya çıkan tutucu ve rezonans desenleri

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

# tiktoken için: pip install tiktoken
try:
    import tiktoken
except ImportError:
    tiktoken = None

# openai istemcisi için: pip install openai
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI paketi bulunamadı. Yüklemek için: pip install openai")

# ortam değişkenleri için: pip install python-dotenv
try:
    import dotenv
    dotenv.load_dotenv()
    ENV_LOADED = True
except ImportError:
    ENV_LOADED = False
    logging.warning("python-dotenv paketi bulunamadı. Yüklemek için: pip install python-dotenv")

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Any, Optional, Union, Callable, TypeVar, Set

# IPython.display için: pip install ipython
try:
    from IPython.display import display, Markdown, HTML, JSON
except ImportError:
    display = print
    Markdown = str
    HTML = str
    JSON = str

# Günlüğe kaydetme ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Sabitler
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000

# Yardımcı Fonksiyonlar ve Sınıflar

def setup_client(api_key: str = None, model: str = DEFAULT_MODEL) -> Tuple[Any, str]:
    """
    API istemcisini yapılandırır.

    Args:
        api_key: API anahtarı (None ise ortam değişkeninden alır)
        model: Kullanılacak model adı

    Returns:
        tuple: (istemci, model adı)
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key and not ENV_LOADED:
            logger.warning("API anahtarı bulunamadı. OPENAI_API_KEY ortam değişkenini ayarlayın veya api_key parametresini geçin.")
    if OPENAI_AVAILABLE:
        client = OpenAI(api_key=api_key)
        return client, model
    else:
        logger.error("OpenAI paketi gerekli. Yüklemek için: pip install openai")
        return None, model


def count_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
    """
    Metindeki token sayısını sayar.

    Args:
        text: Analiz edilecek metin
        model: Tokenizer için model adı

    Returns:
        int: Token sayısı
    """
    if tiktoken:
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception as e:
            logger.warning(f"{model} için tiktoken kullanılamadı: {e}")
    # Kabaca tahmin: 1 token ≈ 4 karakter
    return len(text) // 4


def generate_response(
    prompt: str,
    client=None,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    system_message: str = "You are a helpful assistant."
) -> Tuple[str, Dict[str, Any]]:
    """
    LLM'den yanıt oluşturur ve metriklerle birlikte döner.

    Args:
        prompt: Gönderilecek istem metni
        client: API istemcisi (None ise oluşturulur)
        model: Kullanılacak model
        temperature: Sıcaklık değeri
        max_tokens: Maksimum üretilecek token sayısı
        system_message: Sistem mesajı

    Returns:
        tuple: (yanıt metni, metrikler)
    """
    if client is None:
        client, model = setup_client(model=model)
        if client is None:
            return "HATA: API istemcisi bulunamadı", {"error": "No API client"}
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
        logger.error(f"Yanıt oluşturma hatası: {e}")
        metadata["error"] = str(e)
        return f"HATA: {e}", metadata


def format_metrics(metrics: Dict[str, Any]) -> str:
    """
    Metrikleri okunabilir bir formata çevirir.

    Args:
        metrics: Metrikler sözlüğü

    Returns:
        str: Biçimlendirilmiş metrikler dizisi
    """
    kritik = {
        "prompt_tokens": metrics.get("prompt_tokens", 0),
        "response_tokens": metrics.get("response_tokens", 0),
        "total_tokens": metrics.get("total_tokens", 0),
        "latency": f"{metrics.get('latency', 0):.2f}s",
        "token_efficiency": f"{metrics.get('token_efficiency', 0):.2f}"
    }
    return " | ".join([f"{k}: {v}" for k, v in kritik.items()])


def display_recursive_pattern(
    pattern_name: str,
    input_data: Any,
    iterations: List[Dict[str, Any]],
    final_output: Any,
    metrics: Dict[str, Any] = None
) -> None:
    """
    Özyinelemeli desenin yürütmesini Jupyter'da gösterir.

    Args:
        pattern_name: Desen adı
        input_data: Başlangıç girdisi
        iterations: Döngüsel adım verileri
        final_output: Nihai çıktı
        metrics: Genel metrikler (isteğe bağlı)
    """
    display(HTML(f"<h2>Özyinelemeli Desen: {pattern_name}</h2>"))
    # Başlangıç girdisini göster
    display(HTML("<h3>Başlangıç Girdisi</h3>"))
    if isinstance(input_data, str):
        display(Markdown(input_data))
    else:
        display(Markdown(f"```json\n{json.dumps(input_data, indent=2)}\n```"))

    # Özyinelemeli yinelemeleri göster
    display(HTML("<h3>Özyinelemeli Yinelemeler</h3>"))
    for idx, it in enumerate(iterations):
        display(HTML(f"<h4>Yineleme {idx+1}</h4>"))
        # İstem metni
        if "prompt" in it:
            display(HTML("<p><em>İstem:</em></p>"))
            display(Markdown(f"```\n{it['prompt']}\n```"))
        # Yanıt metni
        if "response" in it:
            display(HTML("<p><em>Yanıt:</em></p>"))
            display(Markdown(it['response']))
        # Durum
        if "state" in it:
            display(HTML("<p><em>Durum:</em></p>"))
            state_data = it['state']
            if isinstance(state_data, str):
                display(Markdown(state_data))
            else:
                display(Markdown(f"```json\n{json.dumps(state_data, indent=2)}\n```"))
        # Metrikler
        if "metrics" in it:
            display(HTML("<p><em>Metrikler:</em></p>"))
            display(Markdown(f"```\n{format_metrics(it['metrics'])}\n```"))

    # Nihai çıktıyı göster
    display(HTML("<h3>Nihai Çıktı</h3>"))
    if isinstance(final_output, str):
        display(Markdown(final_output))
    else:
        display(Markdown(f"```json\n{json.dumps(final_output, indent=2)}\n```"))

    # Genel metrikleri göster
    if metrics:
        display(HTML("<h3>Genel Metrikler</h3>"))
        display(Markdown(f"```\n{format_metrics(metrics)}\n```"))

# Özyinelemeli Desenler için Temel Sınıf
class RecursivePattern:
    """
    Özyinelemeli desenler için temel sınıf: LLM'lerin kendi bağlamlarını
    genişletme, iyileştirme ve evrimleştirme yaklaşımlarını tanımlar.
    """
    def __init__(
        self,
        name: str,
        description: str = "",
        client=None,
        model: str = DEFAULT_MODEL,
        system_message: str = "You are a helpful assistant.",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        max_iterations: int = 5,
        verbose: bool = False
    ):
        """
        Özyinelemeli desen başlatıcısını yapılandırır.

        Args:
            name: Desen adı
            description: Desen açıklaması
            client: API istemcisi (None ise otomatik oluşturulur)
            model: Kullanılacak model
            system_message: Sistem mesajı
            max_tokens: Maksimum token sayısı
            temperature: Sıcaklık parametresi
            max_iterations: Maksimum yineleme sayısı
            verbose: Ayrıntılı çıktı modu
        """
        self.name = name
        self.description = description
        self.client, self.model = setup_client(model=model) if client is None else (client, model)
        self.system_message = system_message
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.max_iterations = max_iterations
        self.verbose = verbose

        # Durum ve metrik takibi
        self.state: Dict[str, Any] = {}
        self.iterations: List[Dict[str, Any]] = []
        self.metrics = {
            "total_prompt_tokens": 0,
            "total_response_tokens": 0,
            "total_tokens": 0,
            "total_latency": 0,
            "iterations": 0
        }

    def _log(self, message: str) -> None:
        """
        verbose modda günlükleme yapar.
        """
        if self.verbose:
            logger.info(message)

    def _generate_recursive_prompt(self, iteration: int, **kwargs) -> str:
        """
        Mevcut yineleme için istem metni oluşturur.
        Alt sınıflarda uygulanmalıdır.
        """
        raise NotImplementedError("Alt sınıflar _generate_recursive_prompt metodunu uygulamalı")

    def _call_llm(
        self,
        prompt: str,
        custom_system_message: Optional[str] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        LLM'e istek gönderir ve metrikleri günceller.
        """
        sys_msg = custom_system_message or self.system_message
        response_text, metadata = generate_response(
            prompt=prompt,
            client=self.client,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            system_message=sys_msg
        )
        # Metrik güncelleme
        self.metrics["total_prompt_tokens"] += metadata.get("prompt_tokens", 0)
        self.metrics["total_response_tokens"] += metadata.get("response_tokens", 0)
        self.metrics["total_tokens"] += metadata.get("total_tokens", 0)
        self.metrics["total_latency"] += metadata.get("latency", 0)
        self.metrics["iterations"] += 1
        return response_text, metadata

    def _process_response(self, response: str, iteration: int) -> Any:
        """
        LLM yanıtını işler. Alt sınıflar gerekirse genişletebilir.
        """
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
        Döngü kaydını günceller ve mevcut durumu kaydeder.
        """
        record = {
            "iteration": iteration,
            "prompt": prompt,
            "response": response,
            "output": processed_output,
            "state": self.state.copy(),
            "metrics": metrics,
            "timestamp": time.time()
        }
        self.iterations.append(record)
        # Durum güncelleme
        self.state["current_iteration"] = iteration
        self.state["last_prompt"] = prompt
        self.state["last_response"] = response
        self.state["last_output"] = processed_output

    def _should_continue(self, iteration: int, current_output: Any) -> bool:
        """
        Döngüye devam edilip edilmeyeceğine karar verir.
        Default: max_iterations sayısına kadar devam eder.
        """
        return iteration < self.max_iterations

    def run(self, input_data: Any) -> Tuple[Any, List[Dict[str, Any]]]:
        """
        Özyinelemeyi verilen girdi ile çalıştırır.

        Args:
            input_data: Başlangıç girdisi

        Returns:
            tuple: (son çıktı, yineleme geçmişi)
        """
        self.state = {"input": input_data}
        self.iterations = []
        self._log(f"Desen başlatılıyor: {self.name}")
        current_output = input_data
        iteration = 0
        # Döngü
        while True:
            iteration += 1
            self._log(f"Yineleme {iteration}/{self.max_iterations}")
            prompt = self._generate_recursive_prompt(
                iteration=iteration,
                input=input_data,
                current_output=current_output,
                **self.state
            )
            response, metrics = self._call_llm(prompt)
            processed = self._process_response(response, iteration)
            self._update_state(iteration, prompt, response, processed, metrics)
            current_output = processed
            if not self._should_continue(iteration, current_output):
                self._log(f"{iteration}. yinelemede duruldu.")
                break
        return current_output, self.iterations

    def get_summary_metrics(self) -> Dict[str, Any]:
        """
        Tüm yinelemelerin özet metriklerini döner.
        """
        summary = self.metrics.copy()
        if summary.get("iterations", 0) > 0:
            summary["avg_latency_per_iteration"] = summary["total_latency"] / summary["iterations"]
            if summary.get("total_prompt_tokens", 0) > 0:
                summary["overall_efficiency"] = (
                    summary["total_response_tokens"] / summary["total_prompt_tokens"]
                )
        return summary

    def display_execution(self) -> None:
        """
        Yineleme sürecini Jupyter'da görselleştirir.
        """
        display_recursive_pattern(
            pattern_name=self.name,
            input_data=self.state.get("input"),
            iterations=self.iterations,
            final_output=self.state.get("last_output"),
            metrics=self.get_summary_metrics()
        )

    def visualize_metrics(self) -> None:
        """
        Metrikleri grafik halinde gösterir.
        """
        if not self.iterations:
            logger.warning("Görselleştirilecek yineleme verisi yok.")
            return
        # Grafik çizme işlemleri
        iters = list(range(1, len(self.iterations) + 1))
        prompt_tokens = [it['metrics'].get('prompt_tokens', 0) for it in self.iterations]
        response_tokens = [it['metrics'].get('response_tokens', 0) for it in self.iterations]
        latencies = [it['metrics'].get('latency', 0) for it in self.iterations]
        efficiencies = [it['metrics'].get('token_efficiency', 0) for it in self.iterations]
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f"Özyinelemeli Desen Metrikleri: {self.name}", fontsize=16)
        # Jeton kullanımı
        axes[0, 0].bar(iters, prompt_tokens, label="İstem Jetonları", color="blue", alpha=0.7)
        axes[0, 0].bar(iters, response_tokens, bottom=prompt_tokens, label="Yanıt Jetonları", color="green", alpha=0.7)
        axes[0, 0].set_title("Yineleme Başına Jeton Kullanımı")
        axes[0, 0].set_xlabel("Yineleme")
        axes[0, 0].set_ylabel("Jeton Sayısı")
        axes[0, 0].legend()
        axes[0, 0].grid(alpha=0.3)
        # Gecikme
        axes[0, 1].plot(iters, latencies, marker='o', color="red", alpha=0.7)
        axes[0, 1].set_title("Yineleme Başına Gecikme")
        axes[0, 1].set_xlabel("Yineleme")
        axes[0, 1].set_ylabel("Saniye")
        axes[0, 1].grid(alpha=0.3)
        # Jeton verimliliği
        axes[1, 0].plot(iters, efficiencies, marker='s', color="purple", alpha=0.7)
        axes[1, 0].set_title("Jeton Verimliliği (Yanıt/İstem)")
        axes[1, 0].set_xlabel("Yineleme")
        axes[1, 0].set_ylabel("Oran")
        axes[1, 0].grid(alpha=0.3)
        # Birikimli jeton kullanımı
        cumulative = np.cumsum([it['metrics'].get('total_tokens', 0) for it in self.iterations])
        axes[1, 1].plot(iters, cumulative, marker='^', color="orange", alpha=0.7)
        axes[1, 1].set_title("Birikimli Jeton Kullanımı")
        axes[1, 1].set_xlabel("Yineleme")
        axes[1, 1].set_ylabel("Toplam Jeton")
        axes[1, 1].grid(alpha=0.3)
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()
