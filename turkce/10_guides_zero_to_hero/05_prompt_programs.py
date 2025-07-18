"""
Prompt Programlama: Yapısal Akıl Yürütme için Betik Şablonları
===========================================================

Bu modül, istemleri yürütülebilir programlar gibi ele alarak
bileşik işlemler, durum yönetimi ve kontrol akışı içeren yapısal bir
yaklaşım sunar. Böylece daha dayanıklı, şeffaf ve genişletilebilir
akıl yürütme sistemleri oluşturabiliriz.

Ele alınan ana kavramlar:
1. Temel istem program yapıları ve şablonlar
2. Bileşik işlemler (akıl yürütme adımları, doğrulama, sentez)
3. Protokol kabukları ve çerçeveler
4. Ortaya çıkan akıl yürütme için alan protokolleri
5. Kendi kendini geliştiren istem programları için ileri teknikler

Kullanım:
    # Jupyter veya Colab'da:
    %run 05_prompt_programs.py
    # veya
    from prompt_programs import PromptProgram, ReasoningProtocol, FieldShell
"""

import hashlib
# tiktoken yüklemek için: pip install tiktoken
try:
    import tiktoken
except ImportError:
    tiktoken = None
import os
import json
import time
import logging

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

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional, Union, Callable, TypeVar
# IPython.display için: pip install ipython
try:
    from IPython.display import display, Markdown, HTML
except ImportError:
    display = print
    Markdown = str
    HTML = str

def setup_client(api_key=None, model=DEFAULT_MODEL):
    """
    LLM etkileşimleri için API istemcisini başlatır.

    Args:
        api_key: API anahtarı (None ise ortam değişkeninden alır)
        model: Kullanılacak model adı

    Returns:
        tuple: (client, model adı)
    """

def count_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
    """
    Metindeki jeton sayısını uygun tokenizer ile sayar.

    Args:
        text: Jeton sayılacak metin
        model: Jetonlama için model adı

    Returns:
        int: Jeton sayısı
    """

def generate_response(
    prompt: str,
    client=None,
    model=DEFAULT_MODEL,
    temperature=0.5,
    max_tokens=100,
    system_message=None,
):
    """
    LLM'den yanıt oluşturur ve metriklerle birlikte döner.

    Args:
        prompt: Gönderilecek istem metni
        client: API istemcisi (None ise oluşturulur)
        model: Kullanılacak model adı
        temperature: Sıcaklık parametresi
        max_tokens: Maksimum üretilecek jeton sayısı
        system_message: Sistem mesajı

    Returns:
        tuple: (yanıt metni, metrikler sözlüğü)
    """