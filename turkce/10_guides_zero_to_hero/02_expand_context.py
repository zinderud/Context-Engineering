#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bağlam Genişletme Teknikleri: İstemlerden Katmanlı Bağlama
=============================================================

Bu betik, temel istemleri katmanlı, bilgi açısından zengin bağlamlara dönüştürmek için pratik stratejiler sunar.
Bu stratejiler, LLM performansını artırır. Odak noktası pratik bağlam mühendisliğidir: bağlam katmanlarını stratejik olarak nasıl ekleyeceğiniz,
yapılandıracağınız ve jeton kullanımı ile çıktı kalitesi üzerindeki etkileri sistematik olarak nasıl ölçeceğiniz.

Ele alınan anahtar kavramlar:
1. Minimal istemleri genişletilmiş, bağlam açısından zengin yapılara dönüştürme
2. Bağlam katmanlama ve bileşik istem mühendisliği ilkeleri
3. Bağlam büyüdükçe jeton kullanımının nicel olarak ölçülmesi
4. Model çıktısı iyileştirmelerinin nitel olarak değerlendirilmesi
5. Bağlamı iyileştirmek ve optimize etmek için yinelemeli yaklaşımlar

Kullanım:
    # Jupyter veya Colab'da:
    %run 02_context_expansion.py
    # veya
    # Betik hücrelerini adım adım çalıştırarak, bağlam katmanlarını değiştirip etkilerini gözlemleyin

Notlar:
    - Her bölüm modülerdir—farklı bağlam katmanlarını düzenleyerek ve çalıştırarak denemeler yapın.
    - Eklenen bağlamın maliyeti (jeton sayısı) ve performansı (çıktı kalitesi) nasıl değiştirdiğini takip edin.
    - Gelişmiş bağlam mühendisliği protokolleri geliştirmek için pratik bir temel olarak kullanın.
"""

## Kurulum ve Önkoşullar

# Gerekli kütüphaneleri içe aktaralım:
import os
import json
import time
import tiktoken  # OpenAI'nin jetonlayıcısı
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any, Optional, Union

# Ortam değişkenlerini yükleyin (.env dosyasına API anahtarınızı eklemeniz gerekecek)
# OpenAI API anahtarı için
import dotenv
dotenv.load_dotenv()

# API istemcilerini tanımlayın (tercihinize göre birini seçin)
USE_OPENAI = True  # Başka bir sağlayıcı kullanmak için False olarak ayarlayın

if USE_OPENAI:
    from openai import OpenAI
    client = OpenAI()
    MODEL = "gpt-3.5-turbo"  # gpt-4 veya diğer modellere değiştirebilirsiniz
else:
    # Alternatif API istemci kurulumunu buraya ekleyin
    # örn. Anthropic, Cohere, vb.
    pass

# Jeton sayacı kurulumu
tokenizer = tiktoken.encoding_for_model(MODEL) if USE_OPENAI else None

def count_tokens(text: str) -> int:
    """Bir dizedeki jetonları uygun jetonlayıcıyı kullanarak sayar."""
    if tokenizer:
        return len(tokenizer.encode(text))
    # OpenAI olmayan modeller için geri düşüş (kaba bir tahmin)
    return len(text.split()) * 1.3  # Kaba bir tahmin

def measure_latency(func, *args, **kwargs) -> Tuple[Any, float]:
    """Bir fonksiyonun yürütme süresini ölçer."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

## 1. Bağlam Genişletmeyi Anlama

# Önceki betikte (`01_min_prompt.ipynb`), atomik istemlerin temellerini keşfettik.
# Şimdi bu atomları stratejik olarak moleküllere (daha zengin bağlam yapıları) nasıl genişleteceğimizi göreceğiz.

# Bağlam etkinliğini ölçmek için bazı yardımcı fonksiyonlar tanımlayalım:
def calculate_metrics(prompt: str, response: str, latency: float) -> Dict[str, float]:
    """Bir istem-yanıt çifti için anahtar metrikleri hesaplar."""
    prompt_tokens = count_tokens(prompt)
    response_tokens = count_tokens(response)
    
    # Basit jeton verimliliği (yanıt jetonları / istem jetonları)
    token_efficiency = response_tokens / prompt_tokens if prompt_tokens > 0 else 0
    
    # 1k jeton başına gecikme
    latency_per_1k = (latency / prompt_tokens) * 1000 if prompt_tokens > 0 else 0
    
    return {
        "prompt_tokens": prompt_tokens,
        "response_tokens": response_tokens,
        "token_efficiency": token_efficiency,
        "latency": latency,
        "latency_per_1k": latency_per_1k
    }

def generate_response(prompt: str) -> Tuple[str, float]:
    """LLM'den bir yanıt üretir ve gecikmeyi ölçer."""
    if USE_OPENAI:
        start_time = time.time()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        latency = time.time() - start_time
        return response.choices[0].message.content, latency
    else:
        # Alternatif API çağrınızı buraya ekleyin
        pass

## 2. Deney: Bağlam Genişletme Teknikleri

# Temel bir istemi genişletmek için farklı teknikleri inceleyelim ve her genişletmenin etkisini ölçelim:
# Temel istem (atom)
base_prompt = "İklim değişikliği hakkında bir paragraf yaz."

# Genişletilmiş istem varyasyonları (moleküller)
expanded_prompts = {
    "base": base_prompt,
    
    "with_role": """İklim sistemleri konusunda uzman bir çevre bilimcisisiniz. 
İklim değişikliği hakkında bir paragraf yazın.""",
    
    "with_examples": """İklim değişikliği hakkında bir paragraf yazın.

Örnek 1:
İklim değişikliği, sıcaklık ve hava desenlerindeki uzun vadeli değişimleri ifade eder. İnsan faaliyetleri, 1800'lerden bu yana iklim değişikliğinin ana itici gücü olmuştur, özellikle ısıyı hapseden gazlar üreten kömür, petrol ve gaz gibi fosil yakıtların yakılması nedeniyle.

Örnek 2:
Küresel iklim değişikliği, aşırı hava olaylarının artan sıklığı, yükselen deniz seviyeleri ve değişen yaban hayatı popülasyonlarında belirgindir. Bilimsel fikir birliği, insan faaliyetlerinin birincil neden olduğuna işaret etmektedir.""",
    
    "with_constraints": """İklim değişikliği hakkında bir paragraf yazın.
- Sayılarla en az bir bilimsel gerçek ekleyin
- Hem nedenleri hem de etkileri belirtin
- Bir eylem çağrısıyla bitirin
- Tonu bilgilendirici ama erişilebilir tutun""",
    
    "with_audience": """Çevre bilimi hakkında yeni öğrenmeye başlayan lise öğrencileri için iklim değişikliği hakkında bir paragraf yazın.
Açık açıklamalar ve ilişkilendirilebilir örnekler kullanın.""",
    
    "comprehensive": """İklim sistemleri konusunda uzman bir çevre bilimcisisiniz.

Çevre bilimi hakkında yeni öğrenmeye başlayan lise öğrencileri için iklim değişikliği hakkında bir paragraf yazın.
Açık açıklamalar ve ilişkilendirilebilir örnekler kullanın.

Yönergeler:
- Sayılarla en az bir bilimsel gerçek ekleyin
- Hem nedenleri hem de etkileri belirtin
- Bir eylem çağrısıyla bitirin
- Tonu bilgilendirici ama erişilebilir tutun

Ton ve yapı örneği:
"Okyanus asitlenmesi, deniz suyunun atmosferden CO2 emmesiyle oluşur ve pH seviyelerinin düşmesine neden olur. Sanayi Devrimi'nden bu yana okyanus pH'ı 0.1 birim azaldı, bu da asitlikte %30'luk bir artışı temsil ediyor. Bu, deniz yaşamını, özellikle kabuklu deniz hayvanlarını ve mercan resiflerini etkiler, çünkü kabuk ve iskelet oluşturma yeteneklerini bozar. Bilim insanları, emisyonların mevcut oranlarda devam etmesi halinde okyanus asitliğinin 2100 yılına kadar %150 artabileceğini ve deniz ekosistemlerini tahrip edeceğini öngörüyor. Toplu taşıma gibi basit eylemlerle karbon ayak izimizi azaltarak bu hayati okyanus habitatlarını korumaya yardımcı olabiliriz."
"""
}

# Deneyleri çalıştır
results = {}
responses = {}

for name, prompt in expanded_prompts.items():
    print(f"İstem test ediliyor: {name}")
    response, latency = generate_response(prompt)
    responses[name] = response
    metrics = calculate_metrics(prompt, response, latency)
    results[name] = metrics
    print(f"  İstem jetonları: {metrics['prompt_tokens']}")
    print(f"  Yanıt jetonları: {metrics['response_tokens']}")
    print(f"  Gecikme: {metrics['latency']:.2f}s")
    print("-" * 40)

## 3. Sonuçları Görselleştirme ve Analiz Etme
# Görselleştirme için verileri hazırla
prompt_types = list(results.keys())
prompt_tokens = [results[k]['prompt_tokens'] for k in prompt_types]
response_tokens = [results[k]['response_tokens'] for k in prompt_types]
latencies = [results[k]['latency'] for k in prompt_types]

# Birden çok alt grafikle şekil oluştur
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Grafik 1: Jeton Kullanımı
axes[0, 0].bar(prompt_types, prompt_tokens, label='İstem Jetonları', alpha=0.7, color='blue')
axes[0, 0].bar(prompt_types, response_tokens, bottom=prompt_tokens, label='Yanıt Jetonları', alpha=0.7, color='green')
axes[0, 0].set_title('İstem Türüne Göre Jeton Kullanımı')
axes[0, 0].set_ylabel('Jeton Sayısı')
axes[0, 0].legend()
plt.setp(axes[0, 0].get_xticklabels(), rotation=45, ha='right')

# Grafik 2: Jeton Verimliliği (Yanıt Jetonları / İstem Jetonları)
token_efficiency = [results[k]['token_efficiency'] for k in prompt_types]
axes[0, 1].bar(prompt_types, token_efficiency, color='purple', alpha=0.7)
axes[0, 1].set_title('Jeton Verimliliği (Yanıt/İstem)')
axes[0, 1].set_ylabel('Verimlilik Oranı')
plt.setp(axes[0, 1].get_xticklabels(), rotation=45, ha='right')

# Grafik 3: Gecikme
axes[1, 0].bar(prompt_types, latencies, color='red', alpha=0.7)
axes[1, 0].set_title('Yanıt Gecikmesi')
axes[1, 0].set_ylabel('Saniye')
plt.setp(axes[1, 0].get_xticklabels(), rotation=45, ha='right')

# Grafik 4: 1k jeton başına gecikme
latency_per_1k = [results[k]['latency_per_1k'] for k in prompt_types]
axes[1, 1].bar(prompt_types, latency_per_1k, color='orange', alpha=0.7)
axes[1, 1].set_title('1k Jeton Başına Gecikme')
axes[1, 1].set_ylabel('1k Jeton Başına Saniye')
plt.setp(axes[1, 1].get_xticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.show()

## 4. Nitel Analiz

# Kalite farklılıklarını değerlendirmek için gerçek yanıtları inceleyelim:
for name, response in responses.items():
    print(f"=== {name} istemi için yanıt ===")
    print(response)
    print("
" + "=" * 80 + "
")

## 5. Bağlam Genişletme Desenleri

# Deneylerimize dayanarak, birkaç etkili bağlam genişletme deseni belirleyebiliriz:
# 1. Rol Atama: Modelin kim olarak hareket etmesi gerektiğini tanımlama
# 2. Az Sayıda Örnek: Yanıt formatını ve kalitesini yönlendirmek için örnek çıktılar sağlama
# 3. Kısıtlama Tanımı: Yanıt için sınırlar ve gereksinimler belirleme
# 4. Kitle Belirtimi: Yanıtın kime yönelik olduğunu açıklama
# 5. Kapsamlı Bağlam: Birden çok bağlam öğesini stratejik olarak birleştirme

# Bu desenleri yeniden kullanılabilir bir şablona dönüştürelim:
def create_expanded_context(
    base_prompt: str, 
    role: Optional[str] = None,
    examples: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
    audience: Optional[str] = None,
    tone: Optional[str] = None,
    output_format: Optional[str] = None
) -> str:
    """
    İsteğe bağlı bileşenlerle temel bir istemden genişletilmiş bir bağlam oluşturur.
    
    Args:
        base_prompt: Temel talimat veya soru
        role: Modelin kim olarak hareket etmesi gerektiği
        examples: Modeli yönlendirmek için örnek çıktıların listesi
        constraints: Gereksinimlerin veya sınırların listesi
        audience: Çıktının kime yönelik olduğu
        tone: Yanıtın istenen tonu
        output_format: Belirli format gereksinimleri
        
    Returns:
        Genişletilmiş bağlam dizesi
    """
    context_parts = []
    
    # Rol sağlanmışsa ekle
    if role:
        context_parts.append(f"Siz {role} rolündesiniz.")
    
    # Temel istemi ekle
    context_parts.append(base_prompt)
    
    # Kitle sağlanmışsa ekle
    if audience:
        context_parts.append(f"Yanıtınız {audience} için uygun olmalıdır.")
    
    # Ton sağlanmışsa ekle
    if tone:
        context_parts.append(f"Yanıtınızda {tone} bir ton kullanın.")
    
    # Çıktı formatı sağlanmışsa ekle
    if output_format:
        context_parts.append(f"Yanıtınızı {output_format} olarak biçimlendirin.")
    
    # Kısıtlamalar sağlanmışsa ekle
    if constraints and len(constraints) > 0:
        context_parts.append("Gereksinimler:")
        for constraint in constraints:
            context_parts.append(f"- {constraint}")
    
    # Örnekler sağlanmışsa ekle
    if examples and len(examples) > 0:
        context_parts.append("Örnekler:")
        for i, example in enumerate(examples, 1):
            context_parts.append(f"Örnek {i}:
{example}")
    
    # Tüm parçaları uygun boşluklarla birleştir
    expanded_context = "

".join(context_parts)
    
    return expanded_context

# Şablonumuzu yeni bir istemle test edelim:
# Şablonumuzu test et
new_base_prompt = "Fotosentezin nasıl çalıştığını açıklayın."

new_expanded_context = create_expanded_context(
    base_prompt=new_base_prompt,
    role="15 yıllık deneyime sahip bir biyoloji öğretmeni",
    audience="ortaokul öğrencileri",
    tone="coşkulu ve eğitici",
    constraints=[
        "Bitki-fabrika benzetmesi kullanın",
        "Klorofilin rolünü belirtin",
        "Dünya ekosistemi için önemini açıklayın",
        "200 kelimenin altında tutun"
    ],
    examples=[
        "Fotosentez, bitkilerin içindeki küçük bir fabrika gibidir. Bir fabrikanın ürün yapmak için hammadde, enerji ve işçilere ihtiyacı olduğu gibi, bitkilerin de glikoz (şeker) ve oksijen yapmak için karbondioksit, su, güneş ışığı ve klorofile ihtiyacı vardır. Güneş ışığı enerji kaynağıdır, klorofil molekülleri bu enerjiyi yakalayan işçilerdir, karbondioksit ve su ise hammaddelerdir. Fabrikanın ürünleri, bitkinin büyüme ve enerji depolaması için kullandığı glikoz ve bizim gibi hayvanların nefes alması için havaya salınan oksijendir. Bu süreç, ihtiyacımız olan oksijeni sağladığı ve atmosferden karbondioksiti uzaklaştırdığı için Dünya'daki yaşam için gereklidir."
    ]
)

print("Şablon tarafından oluşturulan genişletilmiş bağlam:")
print("-" * 80)
print(new_expanded_context)
print("-" * 80)
print(f"Jeton sayısı: {count_tokens(new_expanded_context)}")

# Genişletilmiş bağlamımızı kullanarak bir yanıt üret
response, latency = generate_response(new_expanded_context)
metrics = calculate_metrics(new_expanded_context, response, latency)

print("
Yanıt:")
print("-" * 80)
print(response)
print("-" * 80)
print(f"Yanıt jetonları: {metrics['response_tokens']}")
print(f"Gecikme: {metrics['latency']:.2f}s")

## 10. Sonuç: Bağlam Genişletme En İyi Uygulamaları

# Deneylerimize dayanarak, etkili bağlam genişletmesi için anahtar en iyi uygulamalar şunlardır:
# 1. Minimal başla: İşe yarayabilecek en basit istemle başlayın
# 2. Etkiyi ölç: Her genişletme için jeton kullanımını, gecikmeyi ve kalite metriklerini takip edin
# 3. Stratejik olarak katmanla: Bağlamı, ayrı ayrı test edilebilecek belirgin, modüler katmanlar halinde ekleyin
# 4. Mümkün olduğunda sıkıştır: Jeton kullanımını azaltmak için özetleme, madde işaretleri veya anahtar kelimeler kullanın
# 5. Acımasızca buda: Yanıt kalitesini artırmayan bağlam katmanlarını kaldırın
# 6. Şablonları kullan: Farklı bağlam genişletme desenleri için yeniden kullanılabilir şablonlar oluşturun
# 7. Geri almayı düşün: Büyük bilgi tabanları için, bağlamı dinamik olarak genişletmek için geri almayı kullanın
# 8. Özgüllük ve genellik arasında denge kur: Daha spesifik bağlam halüsinasyonu azaltır ancak yaratıcılığı kısıtlayabilir

### Bağlam Genişletme Karar Verme Şablonu

# 1. Temel hedefi tanımla
#    ↓
# 2. Minimal istem oluştur
#    ↓
# 3. Temel performansı ölç
#    ↓
# 4. Potansiyel bağlam katmanlarını belirle
#    │  - Rol atama
#    │  - Az sayıda örnek
#    │  - Kısıtlamalar/gereksinimler
#    │  - Kitle belirtimi
#    │  - Ton/stil rehberliği
#    ↓
# 5. Her katmanı ayrı ayrı test et
#    ↓
# 6. Umut verici katmanları birleştir
#    ↓
# 7. Etkiyi ölç:
#    │  - Jeton kullanımı
#    │  - Yanıt kalitesi
#    │  - Gecikme
#    ↓
# 8. Gereksiz katmanları buda
#    ↓
# 9. Kalan bağlamı sıkıştır
#    ↓
# 10. Son optimizasyon (jeton verimliliği)

# Unutmayın: Amaç, mümkün olan en büyük bağlamı oluşturmak değil, hem kalite hem de verimlilik için optimize edilmiş en etkili olanı oluşturmaktır.

## Sonraki Adımlar

# Bir sonraki betikte (`03_control_loops.ipynb`), çok adımlı LLM etkileşimleri için daha karmaşık kontrol akışı mekanizmaları oluşturmak üzere bu bağlam genişletme tekniklerinin üzerine nasıl inşa edeceğimizi keşfedeceğiz.