#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kontrol Döngüleri: Çok Adımlı LLM Etkileşimleri için Akış Mekanizmaları
====================================================================

Bu modül, önceki betiklerdeki bağlam genişletme tekniklerine dayanarak
karmaşık çok adımlı LLM etkileşimlerini düzenlemek için kontrol akışı mekanizmalarının
nasıl uygulanacağını gösterir. Aşağıdaki desenleri inceleriz:

1. Sıralı zincirleme (bir adımın çıktısı → sonraki adıma girdi)
2. Yinelemeli iyileştirme (bir yanıtı döngülerle geliştirme)
3. Koşullu dallanma (LLM çıktısına göre farklı yollar)
4. Kendini eleştirme ve düzeltme (çıktıların meta-değerlendirmesi)
5. Harici doğrulama döngüleri (araçlar/bilgi kullanarak doğrulama)

Desenlerde jeton verimliliği ve bağlam bütünlüğünü korumaya odaklanıyoruz.

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
# Jeton sayacı için: pip install tiktoken
try:
    import tiktoken
except ImportError:
    tiktoken = None
from typing import Dict, List, Tuple, Any, Optional, Union, Callable, TypeVar

# Daha iyi tip ipuçları için genel tip değişkenleri
type T = TypeVar('T')
Response = Union[str, Dict[str, Any]]

# Günlüğe kaydetme ve görselleştirme için
import logging
import numpy as np
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

# API istemci ayarları
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
    logger.warning("python-dotenv paketi bulunamadı. Yüklemek için: pip install python-dotenv")

# Varsayılan parametreler
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 500

# Yardımcı Fonksiyonlar
# ================

# İstemci Kurulum Fonksiyonu: API anahtarı ve model bilgisi ile LLM istemcisini başlatır.
def setup_client(api_key=None, model=DEFAULT_MODEL):
    """
    Set up the API client for LLM interactions.
    ...existing code...

 # İstemci oluşturma örneği:
 # client, model = setup_client()
 
 def count_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
     """
     Count tokens in text string using the appropriate tokenizer.
     """
     İstemdeki metni uygun tokenizer ile jetonlara çevirir ve sayısını döndürür.
 
 def generate_response(
     prompt: str,
     api_key: str = None,
     model: str = DEFAULT_MODEL,
     temperature: float = DEFAULT_TEMPERATURE,
     max_tokens: int = DEFAULT_MAX_TOKENS,
     system_message: str = "You are a helpful assistant."
 ) -> Tuple[str, Dict[str, Any]]:
     """
     Generate a response from the LLM and return with metadata.
     """
     LLM'den yanıt oluşturur, istem ve sistem mesajı metriklerini toplar, geri döner.
     try:
         start_time = time.time()
         response = client.chat.completions.create(
