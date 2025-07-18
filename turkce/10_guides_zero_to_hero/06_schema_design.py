#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Şema Tasarımı: Yapısal Bağlam için Protokoller
===============================================

Bu modül, LLM bağlamı için yapılandırılmış şemalar tasarlamaya odaklanır.
Şema tabanlı bağlamlar, tutarlılığı artırır, doğrulanabilirlik sağlar ve
insan niyeti ile makine işlemleri arasında köprü kurar.

Ele alınan ana kavramlar:
1. Temel şema desenleri ve yapıları
2. Şema doğrulama ve uygulama
3. Özyinelemeli (fraktal) şemalar
4. Alan protokolleri ile şema tabanlı bağlamlar
5. Şema etkinliğinin ölçülmesi

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

# tiktoken için: pip install tiktoken
try:
    import tiktoken
except ImportError:
    tiktoken = None

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
tlogging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Kütüphane kontrolü
# openai için: pip install openai
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI paketi bulunamadı. Yüklemek için: pip install openai")

# jsonschema için: pip install jsonschema
try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    logger.warning("jsonschema paketi bulunamadı. Yüklemek için: pip install jsonschema")

# dotenv için: pip install python-dotenv
try:
    import dotenv
    dotenv.load_dotenv()
    ENV_LOADED = True
except ImportError:
    ENV_LOADED = False
    logger.warning("python-dotenv paketi bulunamadı. Yüklemek için: pip install python-dotenv")

# Sabitler
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000

# Yardımcı Fonksiyonlar
# ====================

def setup_client(api_key: Optional[str] = None, model: str = DEFAULT_MODEL) -> Tuple[Any, str]:
    """
    LLM etkileşimleri için API istemcisini başlatır.

    Args:
        api_key: API anahtarı (None ise ortam değişkeninden alır)
        model: Kullanılacak model adı

    Returns:
        tuple: (client, model adı)
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    if OPENAI_AVAILABLE:
        client = OpenAI(api_key=api_key)
        return client, model
    else:
        logger.error("OpenAI istemcisi bulunamadı!")
        return None, model


def count_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
    """
    Metindeki jeton sayısını uygun tokenizer ile sayar.

    Args:
        text: Jeton sayılacak metin
        model: Jetonlama için model adı

    Returns:
        int: Jeton sayısı
    """
    if tiktoken:
        return len(tiktoken.encoding_for_model(model).encode(text))
    # kaba tahmin
    return len(text.split())


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
        model: Kullanılacak model adı
        temperature: Sıcaklık parametresi
        max_tokens: Maksimum üretilecek jeton sayısı
        system_message: Sistem mesajı

    Returns:
        tuple: (yanıt metni, metrikler sözlüğü)
    """
    if client is None:
        client, model = setup_client(model=model)
        if client is None:
            return "ERROR: No API client available", {}

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
        start = time.time()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_message},
                      {"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        latency = time.time() - start
        text = response.choices[0].message.content
        metadata.update({
            "latency": latency,
            "response_tokens": count_tokens(text, model),
            "total_tokens": prompt_tokens + system_tokens + metadata.get("response_tokens", 0),
        })
        return text, metadata
    except Exception as e:
        logger.error(f"Yanıt oluşturma hatası: {e}")
        return f"ERROR: {e}", metadata

# ... sonrasında JSONSchema, SchemaContext, FractalSchema sınıf tanımları gelecek ...
