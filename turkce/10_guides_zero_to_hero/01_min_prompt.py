#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal İstem Keşfi: Bağlam Mühendisliğinin Temelleri
===================================================

Bu betik, minimal ve atomik istemler kullanarak LLM çıktıları ve davranışı üzerindeki doğrudan etkiyi keşfederek bağlam mühendisliğinin temel ilkelerini tanıtır.

Ele alınan ana kavramlar:
1. Maksimum netlik ve kontrol için atomik istemler oluşturma
2. Jeton sayısı ve model yanıt kalitesi ile etkinliği ölçme
3. Hızlı geri bildirim döngüleri için yinelemeli istem değişikliği
4. Bağlam sürüklenmesini ve minimal istem sınırlarını gözlemleme
5. Atomik istemlerden protokolleştirilmiş yapraklara ölçekleme temelleri

Kullanım:
    # Jupyter veya Colab'da:
    %run 01_min_prompt.py
    # veya
    # Her bölümü bağımsız olarak düzenleyip çalıştırarak istem etkilerini deneyin

Notlar:
    - Bu betiğin her bölümü uygulamalı deneyler için tasarlanmıştır.
    - İstemleri değiştirin ve çıktıdaki değişiklikleri gözlemleyin.
    - Bu, ileri düzey bağlam mühendisliği iş akışları için bir temel oluşturur.
"""

import os
import time
import json
from typing import Dict, List, Any, Tuple, Optional
import matplotlib.pyplot as plt

# Eğer OpenAI API kullanıyorsanız, aşağıdaki satırların yorumunu kaldırıp API anahtarınızı ekleyin
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")  # API anahtarınızı ortam değişkeni olarak ayarlayın

# Başka bir sağlayıcı kullanıyorsanız, buna göre ayarlayın
# Gösterim amaçlı basit bir LLM sınıfı
class SimpleLLM:
    """Gösterim amaçlı minimal LLM arayüzü."""
    def __init__(self, model_name: str = "dummy-model"):
        """LLM arayüzünü başlatır."""
        self.model_name = model_name
        self.total_tokens_used = 0
        self.total_requests = 0
        
    def count_tokens(self, text: str) -> int:
        """
        Metin içindeki tokkenleri çok basit bir yaklaşımla sayar.
        Üretimde, modelin tokenizer'ını kullanın.
        """
        return len(text.split())
    
    def generate(self, prompt: str) -> str:
        """
        Bir istemden metin üretir (sahte uygulama).
        Gerçek kullanımda bir LLM API çağrısı yapar.
        """
        tokens = self.count_tokens(prompt)
        self.total_tokens_used += tokens
        self.total_requests += 1
        
        return f"[Bu alana LLM yanıtı gelecektir. İstemin yaklaşık {tokens} tokken kullandığı tahmin ediliyor.]"
    
    def get_stats(self) -> Dict[str, Any]:
        """Kullanım istatistiklerini döndürür."""
        return {
            "total_tokens": self.total_tokens_used,
            "total_requests": self.total_requests,
            "avg_tokens_per_request": self.total_tokens_used / max(1, self.total_requests)
        }

# LLM arayüzümüzü başlatıyoruz
llm = SimpleLLM()

# ----- DENEY 1: ATOMİK İSTEM -----
print("\n----- DENEY 1: ATOMİK İSTEM -----")
print("En temel birimle başlayalım: tek bir talimat.")

atomic_prompt = "Write a short poem about programming."  # Atomik istem
tokens = llm.count_tokens(atomic_prompt)

print(f"\nAtomik İstem: '{atomic_prompt}'")
print(f"Tokken Sayısı: {tokens}")
print("\nYanıt üretiliyor...")
response = llm.generate(atomic_prompt)
print(f"\nYanıt:\n{response}")

# ----- DENEY 2: KISITLAR EKLEME -----
print("\n----- DENEY 2: KISITLAR EKLEME -----")
print("Atomik istemimize kısıtlamalar ekleyip farkı gözlemleyelim.")

# Artan kısıtlamalarla üç sürüm oluşturalım
prompts = [
    "Write a short poem about programming.",  # Orijinal
    "Write a short poem about programming in 4 lines.",  # Uzunluk kısıtı
    "Write a short haiku about programming using only simple words."  # Biçim ve kelime kısıtı
]

results = []
for i, prompt in enumerate(prompts):
    tokens = llm.count_tokens(prompt)
    print(f"\nİstem {i+1}: '{prompt}'")
    print(f"Tokken Sayısı: {tokens}")
    
    start_time = time.time()
    response = llm.generate(prompt)
    end_time = time.time()
    
    results.append({
        "prompt": prompt,
        "tokens": tokens,
        "response": response,
        "latency": end_time - start_time
    })
    
    print(f"Gecikme: {results[-1]['latency']:.4f} saniye")
    print(f"Yanıt:\n{response}")

# ... ve devamı (DENEY 3, 4, 5 ve sonuçlar) ...
# ----- DENEY 3: ROI EĞRİSİ ÖLÇÜMÜ -----
print("\n----- DENEY 3: ROI EĞRİSİ ÖLÇÜMÜ -----")
print("İstem karmaşıklığı ile çıktı kalitesi arasındaki ilişkiyi inceleyelim.")
quality_scores = [3, 6, 8]  # Örnek kalite puanları (1-10 arası)
plt.figure(figsize=(10, 6))
tokens_list = [r["tokens"] for r in results]
plt.plot(tokens_list, quality_scores, marker='o', linestyle='-', color='green')
plt.xlabel('İstemdeki Tokken Sayısı')
plt.ylabel('Çıktı Kalitesi (1-10)')
plt.title('Tokken-Kalite ROI Eğrisi')
plt.grid(True)
for i, (x, y) in enumerate(zip(tokens_list, quality_scores)):
    plt.annotate(f"İstem {i+1}", (x, y), textcoords="offset points",
                 xytext=(0, 10), ha='center')
print("[Bu ortamda bir grafik görüntülenirdi]")

# ----- DENEY 4: MİNİMAL BAĞLAM İYİLEŞTİRMESİ -----
print("\n----- DENEY 4: MİNİMAL BAĞLAM İYİLEŞTİRMESİ -----")
print("Düşük tokken sayısı ile çıktı kalitesini artırmak için minimal bağlam ekleyelim.")
enhanced_prompt = """Task: Write a haiku about programming.

A haiku is a three-line poem with 5, 7, and 5 syllables per line.
Focus on the feeling of solving a difficult bug."""
tokens = llm.count_tokens(enhanced_prompt)
print(f"\nGeliştirilmiş İstem:\n'{enhanced_prompt}'")
print(f"Tokken Sayısı: {tokens}")
response = llm.generate(enhanced_prompt)
print(f"\nYanıt:\n{response}")

# ----- DENEY 5: TUTARLILIK ÖLÇÜMÜ -----
print("\n----- DENEY 5: TUTARLILIK ÖLÇÜMÜ -----")
print("Minimal ve geliştirilmiş istemlerin tutarlılığını ölçelim.")
def measure_consistency(prompt: str, n_samples: int = 3) -> Dict[str, Any]:
    responses = []
    total_tokens = 0
    for _ in range(n_samples):
        response = llm.generate(prompt)
        responses.append(response)
        total_tokens += llm.count_tokens(prompt)
    consistency_score = 0.5  # Örnek tutarlılık skoru
    return {
        "prompt": prompt,
        "responses": responses,
        "total_tokens": total_tokens,
        "consistency_score": consistency_score
    }
basic_results = measure_consistency(prompts[0])
enhanced_results = measure_consistency(enhanced_prompt)
print(f"\nTemel İstem Tutarlılık Skoru: {basic_results['consistency_score']}")
print(f"Geliştirilmiş İstem Tutarlılık Skoru: {enhanced_results['consistency_score']}")

# ----- SONUÇ -----
print("\n----- SONUÇ -----")
print("Deneylerden çıkan temel bulgular:")
print("1. Küçük eklemeler bile çıktı kalitesini önemli ölçüde etkileyebilir")
print("2. Tokken sayısı ile kalite arasında optimal bir denge bulunur (ROI eğrisi)")
print("3. Minimal ama stratejik bağlam eklemek tutarlılığı artırır")
print("4. En iyi istemler net, öz ve yeterli bağlam sağlar")

print("\nBu betikte kullanılan toplam tokken sayısı:", llm.get_stats()["total_tokens"])

# ----- SONRAKİ ADIMLAR -----
print("\n----- SONRAKİ ADIMLAR -----")
print("1. Gerçek bir LLM API'si ile bu deneyleri tekrarlayın")
print("2. Tutarlılık ve kalite metriklerini gerçek verilerle uygulayın")
print("3. 'Moleküller' kavramını keşfedin - çoklu talimat kombinasyonları")
print("4. Az örnekli öğrenme (few-shot) ile bağlam genişlemesini deneyin")
