# Sembolik Mekanizmalar (Türkçe Özet)

Bu doküman, `00_foundations/12_symbolic_mechanisms.md` dosyasının Türkçe bir özetidir.

> *"Bu sonuçlar, sembolik ve sinir ağı yaklaşımları arasındaki uzun süredir devam eden tartışmaya bir çözüm önermektedir; sinir ağlarının, kendiliğinden beliren sembol işleme mekanizmalarının geliştirilmesi yoluyla soyut akıl yürütmeyi nasıl öğrenebildiğini göstermektedir."*
> — [**Yang ve diğerleri, 2025**](https://openreview.net/forum?id=y1SnRPDWx4)

## 1. Giriş: Sembollerin Doğuşu

Nöral Alanlar gibi sürekli ve akışkan yapıları incelerken, akla şu soru gelir: LLM'ler nasıl oluyor da bu alanların içinden kural tabanlı ve mantıksal görünen **sembolik akıl yürütmeyi** çıkarabiliyor? Bu bölüm, bu soruyu yanıtlıyor ve LLM'lerin içinde kendiliğinden ortaya çıkan (emergent) sembolik mekanizmaları inceliyor.

Bu mekanizmaları anlamak, LLM'lerin bilgiyi gerçekte nasıl işlediğine daha uygun bağlam yapıları tasarlamamızı sağlar.

## 2. Üç Aşamalı Sembolik Mimari

Princeton ve Google'daki araştırmacılar (Yang vd., 2025), LLM'lerin soyut akıl yürütme için kendiliğinden gelişen üç aşamalı bir mimari kullandığını ortaya koymuştur:

```
                        ks (Çıktı)
                        ↑
                       (A)
3. Geri Çağırma         ↑ 
   Kafaları        (A) (B) (A)
                     ↑   ↑   ↑
                        
2. Sembolik         (A) (B) (A) (A) (B) (A) (A) (B) (Kalıp Tahmini)
   Tümevarım          ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑
   Kafaları                   
                        
1. Sembol      (A)     (B)     (A)     (A)     (B)     (A)     (A)     (B) (Soyutlama)
   Soyutlama    ↑       ↑       ↑       ↑       ↑       ↑       ↑       ↑
   Kafaları    iac     ilege    iac    ptest     yi     ptest    ks      ixe (Girdi)
```

### 2.1. Sembol Soyutlama Kafaları (Symbol Abstraction Heads)

*   **Görevi:** Girdi token'larını (kelimeleri), aralarındaki ilişkilere dayanarak soyut değişkenlere dönüştürmek.
*   **Nasıl Çalışır:** Modelin ilk katmanlarında bulunur. Örneğin, "kedi köpek kedi" diziliminde, bu kafalar "kedi" ve "köpek" kelimelerine değil, "birinci eleman", "ikinci eleman" ve "birinci elemanın tekrarı" gibi **ilişkisel rollere** odaklanır. Bu rolleri A ve B gibi soyut değişkenlerle temsil eder.

### 2.2. Sembolik Tümevarım Kafaları (Symbolic Induction Heads)

*   **Görevi:** Soyut değişkenler üzerinde kalıp tanıma ve dizi tümevarımı yapmak.
*   **Nasıl Çalışır:** Orta katmanlarda bulunur. "A B A" gibi soyut kalıpları tanır ve bir sonraki adımda hangi soyut değişkenin gelmesi gerektiğini tahmin eder.

### 2.3. Geri Çağırma Kafaları (Retrieval Heads)

*   **Görevi:** Tahmin edilen soyut değişkeni, mevcut bağlamdaki somut token karşılığına geri çevirmek.
*   **Nasıl Çalışır:** Son katmanlarda bulunur. Sembolik Tümevarım Kafası bir sonraki adımın "A" değişkeni olacağını tahmin ettiyse, Geri Çağırma Kafası mevcut bağlamda "A" değişkeninin hangi somut kelimeye (örneğin, "kedi") karşılık geldiğini bulur ve bu kelimeyi çıktı olarak üretir.

## 3. Bağlam Mühendisliği için Çıkarımlar

Bu mekanizmaların varlığı, bağlam mühendisliği stratejilerimizi etkiler:

*   **Kalıp Odaklı Örnekler:** LLM'e çok sayıda spesifik örnek vermek yerine, soyut ilişkileri vurgulayan **net kalıp yapıları** sunmak daha etkili olabilir.
*   **Soyut Değişkenleri Çapalama:** Prompt'larımızda `X = [girdi kategorisi]` gibi soyut değişkenleri açıkça tanımlayarak, modelin soyutlama mekanizmalarına yardımcı olabiliriz.
*   **Sembolik Çekiciler:** Nöral Alanlar içinde, bu soyut değişkenlere karşılık gelen kararlı **çekiciler (attractors)** yaratarak, modelin düşünce sürecini daha tutarlı hale getirebiliriz.

## 4. Sonuç: İki Dünyanın Birleşimi

LLM'lerin içinde kendiliğinden beliren bu sembolik mekanizmaların keşfi, sinir ağı (bağlantıcı) ve sembolik (kural tabanlı) yapay zeka yaklaşımları arasındaki tarihsel ayrımı ortadan kaldırmaktadır. LLM'ler, ölçeklendikçe, esnek ve sürekli olan Nöral Alanların içinden, kural tabanlı ve yapısal olan sembolik akıl yürütmeyi kendiliğinden "icat etmektedir".

Etkili bir bağlam mühendisi, hem alanların akışkan dinamiklerini hem de bu sembolik mekanizmaların yapısal mantığını anlayan ve her ikisinden de yararlanan sistemler tasarlayan kişidir.
