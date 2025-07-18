#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bağlam Genişletme Teknikleri: İstemlerden Katmanlı Bağlama
========================================================

Bu betik, temel istemleri içeriği zengin katmanlı bağlamlara dönüştürerek LLM performansını nasıl iyileştireceğimizi gösterir.
Odağımız pratik bağlam mühendisliği: bağlam katmanlarını stratejik olarak nasıl ekleyeceğiniz, yapısallaştıracağınız
ve jeton kullanımı ile çıktı kalitesi üzerindeki etkilerini nasıl sistematik olarak ölçeceğiniz.

Ele alınan ana kavramlar:
1. Minimal istemleri genişletilmiş, bağlam zengini yapılara dönüştürme
2. Bağlam katmanlama ve bileşik istem mühendisliği ilkeleri
3. Bağlam büyüdükçe jeton kullanımının nicel ölçümü
4. Model çıktısı iyileştirmelerinin nitel değerlendirmesi
5. Bağlamı yinelemeli yaklaşımlarla rafine etme ve optimize etme

Kullanım:
    # Jupyter veya Colab'da:
    %run 02_expand_context.py
    # veya
    # Hücre hücre betiği düzenleyip çalıştırarak bağlam katmanlarını deneyin

Notlar:
    - Her bölüm modülerdir—farklı bağlam katmanlarını değiştirip etkileri gözlemleyin.
    - Eklenen bağlamın maliyet (jeton sayısı) ve performans (çıktı kalitesi) üzerindeki etkisini takip edin.
    - İleri düzey bağlam mühendisliği protokolleri geliştirmek için pratik bir temel oluşturur.
"""

import os
import json
import time
# OpenAI tokenizer (tiktoken) yüklemek için: pip install tiktoken
try:
    import tiktoken
except ImportError:
    tiktoken = None
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any, Optional, Union

# Ortam değişkenlerini yüklemek için: pip install python-dotenv
try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    dotenv = None

# API istemcileri tanımlama (tercihinize göre birini seçin)
USE_OPENAI = True  # False yaparak başka bir sağlayıcı kullanabilirsiniz

# OpenAI API istemcisini kullanmak için: pip install openai
if USE_OPENAI:
    try:
        from openai import OpenAI
        client = OpenAI()
        MODEL = "gpt-3.5-turbo"
    except ImportError:
        client = None
        MODEL = None
        # openai kütüphanesini yüklemek için: pip install openai
else:
    client = None
    MODEL = None

# Jeton sayacı kurulum
tokenizer = tiktoken.encoding_for_model(MODEL) if (USE_OPENAI and tiktoken) else None

def count_tokens(text: str) -> int:
    """Metni uygun tokenizer ile jetonlara çevirir ve sayar."""
    if tokenizer:
        return len(tokenizer.encode(text))
    # OpenAI dışı modeller için kaba tahmin
    return int(len(text.split()) * 1.3)


def measure_latency(func, *args, **kwargs) -> Tuple[Any, float]:
    """Bir fonksiyonun yürütme süresini ölçer."""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, end - start

# Bağlam Genişletme Deneylerine Hazırlık
print("\n----- DENEY: Bağlam Genişletme Tekniklerine Hazırlık -----")
print("Temel araç ve fonksiyonlar hazırlandı.")

# 1. Araçlar ve Metrik Fonksiyonları
from typing import Tuple

def calculate_metrics(istem: str, yanit: str, gecikme: float) -> Dict[str, float]:
    """Bir istem-yanıt çiftine ait temel metrikleri hesaplar."""
    istem_tokkens = count_tokens(istem)
    yanit_tokkens = count_tokens(yanit)
    verimlilik = yanit_tokkens / istem_tokkens if istem_tokkens > 0 else 0
    gecikme_per_1k = (gecikme / istem_tokkens) * 1000 if istem_tokkens > 0 else 0
    return {
        "istem_tokkens": istem_tokkens,
        "yanit_tokkens": yanit_tokkens,
        "verimlilik": verimlilik,
        "gecikme": gecikme,
        "gecikme_per_1k": gecikme_per_1k
    }

def generate_response(istem: str) -> Tuple[str, float]:
    """LLM'den yanıt üretir ve gecikmeyi ölçer."""
    if USE_OPENAI and client:
        start = time.time()
        yanit = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": istem}],
            temperature=0.7,
            max_tokens=500
        )
        gec = time.time() - start
        return yanit.choices[0].message.content, gec
    else:
        # Demo modu: gerçek API kurulu değilse basit geri dönüş
        return f"[Demo yanıt. {count_tokens(istem)} tokken kullanıldı.]", 0.0

# 2. Deney: Bağlam Genişletme Teknikleri
print("\n----- DENEY: Bağlam Genişletme -----")
base_prompt = "Write a paragraph about climate change."
expanded = {
    "base": base_prompt,
    "with_role": """You are an environmental scientist with expertise in climate systems.\nWrite a paragraph about climate change.""",
    "with_examples": """Write a paragraph about climate change.\n\nExample 1: ...\nExample 2: ...""",
    "with_constraints": """Write a paragraph about climate change.\n- At least one scientific fact with numbers\n- Causes and effects\n- Call to action\n- Accessible tone""",
    "with_audience": """Write a paragraph about climate change for high school students. Use clear explanations.""",
    "comprehensive": """You are an environmental scientist..."""
}
results = {}
responses = {}
for isim, istem in expanded.items():
    print(f"İstem testi: {isim}")
    yanit, gec = generate_response(istem)
    responses[isim] = yanit
    met = calculate_metrics(istem, yanit, gec)
    results[isim] = met
    print(f"  İstem Tokken: {met['istem_tokkens']}")
    print(f"  Yanıt Tokken: {met['yanit_tokkens']}")
    print(f"  Gecikme: {met['gecikme']:.2f}s")
    print("-"*40)

# 3. Sonuçların Görselleştirilmesi
prompt_turleri = list(results.keys())
tokkens_istem = [results[k]['istem_tokkens'] for k in prompt_turleri]
tokkens_yanit = [results[k]['yanit_tokkens'] for k in prompt_turleri]
gecikmeler = [results[k]['gecikme'] for k in prompt_turleri]
verimlilik = [results[k]['verimlilik'] for k in prompt_turleri]
gec_per1k = [results[k]['gecikme_per_1k'] for k in prompt_turleri]

fig, axs = plt.subplots(2, 2, figsize=(14, 10))
axs[0, 0].bar(prompt_turleri, tokkens_istem, label='İstem Token', color='blue')
axs[0, 0].bar(prompt_turleri, tokkens_yanit, bottom=tokkens_istem, label='Yanıt Token', color='green')
axs[0, 0].set_title('Token Kullanımı')
axs[0, 0].legend()
axs[0, 1].bar(prompt_turleri, verimlilik, color='purple')
axs[0, 1].set_title('Token Verimliliği (Yanıt/İstem)')
axs[1, 0].bar(prompt_turleri, gecikmeler, color='red')
axs[1, 0].set_title('Yanıt Gecikmesi (s)')
axs[1, 1].bar(prompt_turleri, gec_per1k, color='orange')
axs[1, 1].set_title('1k Token Başına Gecikme')
for ax in axs.flatten():
    plt.sca(ax)
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Nitel Analiz
print("\n----- NİTEL ANALİZ: Yanıt İncelemesi -----")
for isim, yanit in responses.items():
    print(f"=== {isim} istem yanıtı ===")
    print(yanit)
    print("="*80)

# 5. Bağlam Genişletme Kalıpları
def create_expanded_context(
    base_prompt: str,
    role: Optional[str] = None,
    examples: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
    audience: Optional[str] = None,
    tone: Optional[str] = None,
    output_format: Optional[str] = None
) -> str:
    """Temel bir istemi opsiyonel bileşenlerle genişletilmiş bağlama dönüştürür."""
    parts = []
    if role:
        parts.append(f"You are {role}.")
    parts.append(base_prompt)
    if audience:
        parts.append(f"Your response should be suitable for {audience}.")
    if tone:
        parts.append(f"Use a {tone} tone.")
    if output_format:
        parts.append(f"Format response as {output_format}.")
    if constraints:
        parts.append("Requirements:")
        parts += [f"- {c}" for c in constraints]
    if examples:
        parts.append("Examples:")
        for i, ex in enumerate(examples, 1):
            parts.append(f"Example {i}: {ex}")
    return "\n\n".join(parts)

# Şablon Testi
print("\n----- ŞABLON TESTİ -----")
test_prompt = "Explain how photosynthesis works."
test_ctx = create_expanded_context(
    base_prompt=test_prompt,
    role="a biology teacher",
    audience="middle school students",
    tone="enthusiastic",
    constraints=["Use plant-to-factory analogy","Mention chlorophyll","Keep under 200 words"],
    examples=["Photosynthesis is like a tiny factory..."]
)
print(test_ctx)
print(f"Token sayısı: {count_tokens(test_ctx)}")
