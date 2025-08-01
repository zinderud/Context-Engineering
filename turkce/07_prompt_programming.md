# Prompt Programlama: Kod Benzeri Kalıplarla Yapılandırılmış Akıl Yürütme (Türkçe Özet)

Bu doküman, `00_foundations/07_prompt_programming.md` dosyasının Türkçe bir özetidir.

> "Dilimin sınırları, dünyamın sınırlarıdır." — Ludwig Wittgenstein

## Kod ve Prompt'ların Yakınsaması

Bağlam mühendisliği yolculuğumuzda atomlardan bilişsel araçlara ulaştık. Şimdi güçlü bir sentezi keşfediyoruz: **Prompt Programlama**. Bu, programlama dünyasının yapısal gücünü, prompt'ların esnekliğiyle birleştiren melez bir yaklaşımdır.

IBM gibi kurumların son araştırmalarının da vurguladığı gibi, yapılandırılmış prompt şablonları (veya "prompt programları"), insanların kullandığı zihinsel kısayollar gibi davranarak LLM'lerin akıl yürütme yeteneğini önemli ölçüde artırır.

## Prompt Programlama Neden İşe Yarar?

Bu yaklaşım, karmaşık problemleri yönetilebilir adımlara bölerek, çözümleri sistematik bir şekilde keşfetmeyi sağlayarak ve yeniden kullanılabilir akıl yürütme kalıpları oluşturarak LLM'lere rehberlik eder.

## Ana Konsept: Bilişsel Operasyonları Fonksiyon Olarak Görmek

Prompt programlamanın temel fikri, `analiz et`, `özetle`, `karşılaştır` gibi bilişsel operasyonları, parametreler alan çağrılabilir **fonksiyonlar** olarak ele almaktır.

**Geleneksel Prompt:** `"Birinci Dünya Savaşı'nın nedenlerini siyasi, ekonomik ve sosyal faktörleri göz önünde bulundurarak analiz et."`

**Prompt Programı:**
```python
analyze(
  topic="Birinci Dünya Savaşı'nın nedenleri",
  factors=["siyasi", "ekonomik", "sosyal"],
  depth="kapsamlı",
  format="yapılandırılmış"
)
```

Bu programatik versiyon, parametreleri netleştirir, sistematik varyasyonlara olanak tanır ve benzer analizler için yeniden kullanılabilir bir şablon oluşturur.

## Prompt'larda Programlama Paradigmaları

Prompt programlama, çeşitli programlama paradigmalarından ilham alır:

1.  **Fonksiyonel Programlama:** Bilişsel operasyonları, birbirine zincirlenebilen (function composition) saf fonksiyonlar olarak ele alır. `sonuç = özetle(analiz_et(araştır(...)))`
2.  **Prosedürel Programlama:** Karmaşık bir görevi, adım adım işletilen bir prosedür olarak tanımlar. `prosedür denklemiÇöz(denklem) { adım 1: ...; adım 2: ...; }`
3.  **Nesne Yönelimli Programlama:** Bir konuyu, kendi verilerine (özellikler) ve yeteneklerine (metotlar) sahip bir "nesne" olarak modeller. `analizci = new MetinAnalizcisi(metin); analizci.temalarıBul();`

## Uygulama Örnekleri

*   **Koşullu Mantık:** Problemin türüne göre (cebir, geometri vb.) farklı bir çözüm yaklaşımı ve adımları oluşturan bir prompt programı.
*   **Yinelemeli İyileştirme Döngüleri:** Bir metnin ilk taslağını oluşturan, ardından yapı, dil ve cila için art arda iyileştirme adımlarından geçiren bir program.
*   **Bilişsel Araç Entegrasyonu:** `soruyuAnla`, `ilgiliBilgiyiHatırla`, `çözümüDoğrula` gibi daha küçük, uzmanlaşmış bilişsel araçları (fonksiyonları) bir araya getirerek karmaşık bir problemi çözen bir ana program.

## Meta-Programlama: Prompt Üreten Prompt'lar

Prompt programlamanın en ileri noktası, diğer prompt programlarını veya bilişsel araçları dinamik olarak üreten "meta-programlardır". Örneğin, `uzmanlaşmışAraçOluştur(görev_tipi, karmaşıklık_seviyesi)` gibi bir meta-program, belirli bir görev için optimize edilmiş yeni bir bilişsel araç üretebilir.

## Önemli Çıkarımlar

1.  **Prompt programlama**, programlama kavramlarını doğal dil prompt'ları ile birleştirir.
2.  **Bilişsel araçlar**, belirli akıl yürütme operasyonları için modüler fonksiyonlar olarak hizmet eder.
3.  **Koşullar ve döngüler** gibi kontrol yapıları, daha karmaşık akıl yürütme sağlar.
4.  **Fonksiyon birleştirme**, basit bileşenlerden karmaşık akıl yürütme zincirleri oluşturmaya olanak tanır.
5.  **Meta-programlama**, dinamik olarak uzmanlaşmış araçların üretilmesini sağlar.
6.  Araştırmalar, bu yaklaşımın modellerde önemli performans artışları sağladığını göstermektedir.

Bu yaklaşım, LLM'lerle etkileşimi, basit talimatlar vermekten, karmaşık, yapılandırılmış ve yeniden kullanılabilir akıl yürütme sistemleri tasarlamaya doğru taşır.
