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
        # Bu son derece kaba bir yaklaşımdır, pratikte uygun bir tokenizer kullanın
        return len(text.split())
    
    def generate(self, prompt: str) -> str:
        """
        Bir istemden metin üretir (sahte uygulama).
        Gerçek bir not defterinde, bu gerçek bir LLM API'sini çağırırdı.
        """
        # Gerçek bir uygulamada, bu API'yi çağırırdı
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return response.choices[0].message.content
        
        # Demo amaçlı, sadece istemi onaylayacağız
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
print("
----- DENEY 1: ATOMİK İSTEM -----")
print("En temel birimle başlayalım: tek bir talimat.")

atomic_prompt = "Programlama hakkında kısa bir şiir yaz."
tokens = llm.count_tokens(atomic_prompt)

print(f"
Atomik İstem: '{atomic_prompt}'")
print(f"Tokken Sayısı: {tokens}")
print("
Yanıt üretiliyor...")
response = llm.generate(atomic_prompt)
print(f"
Yanıt:
{response}")

# ----- DENEY 2: KISITLAR EKLEME -----
print("
----- DENEY 2: KISITLAR EKLEME -----")
print("Şimdi atomik istemimize kısıtlamalar ekleyip farkı gözlemleyelim.")

# Artan kısıtlamalarla üç sürüm oluşturalım
prompts = [
    "Programlama hakkında kısa bir şiir yaz.",  # Orijinal
    "Programlama hakkında 4 satırlık kısa bir şiir yaz.",  # Uzunluk kısıtı eklendi
    "Sadece basit kelimeler kullanarak programlama hakkında kısa bir haiku yaz."  # Biçim ve kelime dağarcığı kısıtları
]

# Jetonları ölç ve yanıtlar üret
results = []
for i, prompt in enumerate(prompts):
    tokens = llm.count_tokens(prompt)
    print(f"
İstem {i+1}: '{prompt}'")
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
    print(f"Yanıt:
{response}")

# ----- DENEY 3: ROI EĞRİSİNİ ÖLÇME -----
print("
----- DENEY 3: ROI EĞRİSİNİ ÖLÇME -----")
print("İstem karmaşıklığı ile çıktı kalitesi arasındaki ilişkiyi inceleyelim.")

# Gerçek bir not defterinde, her yanıt için öznel kalite puanları tanımlardınız
# Bu demo için yer tutucu değerler kullanacağız
quality_scores = [3, 6, 8]  # 1-10 ölçeğinde yer tutucu öznel puanlar

# Jetonları kaliteye karşı çiz
plt.figure(figsize=(10, 6))
tokens_list = [r["tokens"] for r in results]
plt.plot(tokens_list, quality_scores, marker='o', linestyle='-', color='blue')
plt.xlabel('İstemdeki Jetonlar')
plt.ylabel('Çıktı Kalitesi (1-10)')
plt.title('Jeton-Kalite ROI Eğrisi')
plt.grid(True)

# Ek açıklamalar ekle
for i, (x, y) in enumerate(zip(tokens_list, quality_scores)):
    plt.annotate(f"İstem {i+1}", (x, y), textcoords="offset points", 
                 xytext=(0, 10), ha='center')

# Grafiği göster (Jupyter'de bu satır içi görüntülenirdi)
# plt.show()
print("[Bir Jupyter ortamında burada bir grafik görüntülenirdi]")

# ----- DENEY 4: MİNİMAL BAĞLAM İYİLEŞTİRMESİ -----
print("
----- DENEY 4: MİNİMAL BAĞLAM İYİLEŞTİRMESİ -----")
print("Şimdi jeton sayısını düşük tutarken çıktı kalitesini artırmak için minimal bağlam ekleyeceğiz.")

# Az miktarda stratejik bağlam içeren bir istem oluşturalım
enhanced_prompt = """Görev: Programlama hakkında bir haiku yaz.

Haiku, her satırda 5, 7 ve 5 hece bulunan üç satırlık bir şiirdir.
Zor bir hatayı çözme hissine odaklanın."""

tokens = llm.count_tokens(enhanced_prompt)
print(f"
Geliştirilmiş İstem:
'{enhanced_prompt}'")
print(f"Tokken Sayısı: {tokens}")

response = llm.generate(enhanced_prompt)
print(f"
Yanıt:
{response}")

# ----- DENEY 5: TUTARLILIĞI ÖLÇME -----
print("
----- DENEY 5: TUTARLILIĞI ÖLÇME -----")
print("Minimal ve geliştirilmiş istemlerle çıktıların ne kadar tutarlı olduğunu test edelim.")

# Birden çok yanıt üretmek ve tutarlılığı ölçmek için fonksiyon
def measure_consistency(prompt: str, n_samples: int = 3) -> Dict[str, Any]:
    """Birden çok yanıt üretir ve tutarlılık metriklerini ölçer."""
    responses = []
    total_tokens = 0
    
    for _ in range(n_samples):
        response = llm.generate(prompt)
        responses.append(response)
        total_tokens += llm.count_tokens(prompt)
    
    # Gerçek bir not defterinde, yanıtlar arasında anlamsal benzerlik gibi
    # uygun tutarlılık metriklerini uygulardınız
    consistency_score = 0.5  # Yer tutucu değer
    
    return {
        "prompt": prompt,
        "responses": responses,
        "total_tokens": total_tokens,
        "consistency_score": consistency_score
    }

# Temel ve geliştirilmiş istemi karşılaştır
basic_results = measure_consistency(prompts[0])
enhanced_results = measure_consistency(enhanced_prompt)

print(f"
Temel İstem Tutarlılık Puanı: {basic_results['consistency_score']}")
print(f"Geliştirilmiş İstem Tutarlılık Puanı: {enhanced_results['consistency_score']}")

# ----- SONUÇ -----
print("
----- SONUÇ -----")
print("Deneylerimizden elde edilen temel bilgiler:")
print("1. İstemlere yapılan küçük eklemeler bile çıktı kalitesini önemli ölçüde etkileyebilir")
print("2. Jeton sayısı ve kalitenin optimal bir denge bulduğu bir ROI eğrisi vardır")
print("3. Minimal ama stratejik bağlam eklemek tutarlılığı artırır")
print("4. En iyi istemler açık, öz ve sadece yeterli bağlam sağlayanlardır")

print("
Bu not defterinde kullanılan toplam jeton:", llm.get_stats()["total_tokens"])

# ----- SONRAKİ ADIMLAR -----
print("
----- SONRAKİ ADIMLAR -----")
print("1. Bu deneyleri gerçek bir LLM API'si ile deneyin")
print("2. Uygun tutarlılık ve kalite metriklerini uygulayın")
print("3. 'Moleküller' kavramını keşfedin - birden çok talimatı birleştirme")
print("4. Bağlam penceresinde az sayıda örnekle denemeler yapın")

"""
OKUYUCU İÇİN ALIŞTIRMA:

1. Bu not defterini gerçek bir LLM API'sine (OpenAI, Anthropic, vb.) bağlayın
2. Aynı istemleri farklı model boyutlarıyla test edin
3. Önemsediğiniz bir görev için kendi jeton-kalite eğrinizi oluşturun
4. Kendi özel kullanım durumunuz için "minimum uygulanabilir bağlamı" bulun

Daha gelişmiş bağlam mühendisliği teknikleri için 02_expand_context.ipynb'ye bakın!
"""

# Bu bir Jupyter not defteri olsaydı, sonuçları burada bir dosyaya kaydederdik
# with open('experiment_results.json', 'w') as f:
#     json.dump(results, f, indent=2)