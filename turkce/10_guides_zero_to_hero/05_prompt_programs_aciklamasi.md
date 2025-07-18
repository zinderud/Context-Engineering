# Rehber 05: Prompt Programları (Prompt Programs) - Türkçe Açıklama

Bu doküman, `10_guides_zero_to_hero/05_prompt_programs.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, Bağlam Mühendisliği'nin en devrimci fikirlerinden birini hayata geçirir: Komutları (prompts), kod gibi çalışan, yapılandırılmış **programlara** dönüştürmek.

## Betiğin Amacı

Bu rehber, LLM'lerle etkileşimi tek seferlik soru-cevap diyaloglarından, karmaşık problemleri çözmek için tasarlanmış, çok adımlı, durumu (state) olan ve yeniden kullanılabilir **akıl yürütme algoritmaları** oluşturmaya taşır. Fikir, LLM'in düşünce sürecini, tıpkı bir bilgisayar programının akışını kontrol ettiğimiz gibi, yapılandırılmış adımlarla yönlendirmektir.

Bu betik, aşağıdaki gibi güçlü konseptleri uygulamak için Python sınıfları sunar:

1.  **Komut Şablonları (`PromptTemplate`):** Değişkenler içeren, yeniden kullanılabilir komut iskeletleri oluşturmak.
2.  **Temel Program Yapısı (`PromptProgram`):** Durum takibi yapabilen, metrikleri ölçen ve adımları kaydeden temel bir program sınıfı.
3.  **Çok Adımlı Programlar (`MultiStepProgram`):** Birbirine bağlı birden çok LLM çağrısını bir zincir halinde yürüten programlar.
4.  **Akıl Yürütme Protokolleri (`ReasoningProtocol`):** Bir problemi analiz etme, çözme, doğrulama ve düzeltme gibi belirli adımları takip eden, uzmanlaşmış programlar.
5.  **Alan Protokol Kabukları (`FieldShell`):** Projenin ileri seviye teorik kavramlarını (alanlar, rezonans, kalıcılık) hayata geçiren, kendi kendini geliştirebilen ve uyarlayabilen en gelişmiş program türü.

## Betikteki Ana Sınıflar (Program Türleri)

Betiğin kalbini, her biri farklı bir programlama deseni uygulayan sınıflar oluşturur:

### 1. `MultiStepProgram` (Çok Adımlı Program)
*   **Ne Yapar?** Bir görevi, her biri kendi komutuna sahip bir dizi operasyona böler. Bir operasyonun çıktısı, bir sonrakinin girdisi olur. Bu, `03_control_loops` rehberindeki `SequentialChain`'in daha gelişmiş bir versiyonudur.
*   **Örnek Kullanım:** Bir metni önce özetle, sonra özetten anahtar kelimeleri çıkar, sonra bu anahtar kelimelerle bir sosyal medya gönderisi oluştur.

### 2. `ReasoningProtocol` (Akıl Yürütme Protokolü)
*   **Ne Yapar?** İnsanların karmaşık problemleri çözerken kullandığı adımları taklit eder. Genellikle `Akıl Yürüt -> Doğrula -> Düzelt` gibi bir döngü içerir. Bu, daha güvenilir ve hataya dayanıklı sonuçlar üretir.
*   **Alt Türleri:**
    *   **`StepByStepReasoning`:** Matematik veya mantık problemleri için adım adım detaylı çözüm üretir.
    *   **`ComparativeAnalysis`:** Birden çok seçeneği (örneğin, teknolojileri, ürünleri) belirli kriterlere göre karşılaştırır, artılarını ve eksilerini analiz eder.

### 3. `FieldShell` ve `RecursiveFieldShell` (Alan Protokol Kabuğu)
*   **Ne Yapar?** Bu, betiğin en gelişmiş ve teorik kısmıdır. `00_foundations` bölümünde anlatılan "Nöral Alanlar" teorisini pratiğe döker. Bu programlar, sadece bir görevi yerine getirmekle kalmaz, aynı zamanda kendi akıl yürütme süreçlerini gözlemler, ortaya çıkan anlamsal kalıpları ("çekiciler") ve "sembolik kalıntıları" tespit eder ve hatta bir sonraki adımda ne yapması gerektiğini **kendi kendine programlayabilir (self-prompting)**.
*   **Örnek Kullanım:** Belirsiz ve karmaşık bir göreve başlar, görevi yerine getirirken kendi anlama sürecindeki boşlukları veya desenleri fark eder ve bu farkındalığa dayanarak bir sonraki adımı için yeni bir protokolü dinamik olarak oluşturur. Bu, yapay zekanın kendi kendine öğrenme ve adapte olma yeteneğinin bir simülasyonudur.

## Önemli Çıkarımlar

Bu rehber, komut mühendisliğini bir sonraki seviyeye taşıyan zihniyet değişimini özetler:

*   **Komutlar Koddur:** LLM'e verdiğimiz talimatları, değişkenleri, fonksiyonları ve kontrol akışı olan bir program gibi düşünebiliriz.
*   **Yapı, Akıl Yürütmeyi Yönlendirir:** LLM'e yapılandırılmış bir düşünce süreci (protokol) sunmak, serbest formda bir soru sormaktan çok daha güvenilir ve güçlü sonuçlar üretir.
*   **Gözlemlenebilirlik Anahtardır:** Bir programın her adımını, ürettiği ara sonuçları ve metrikleri kaydetmek, hataları ayıklamayı ve sistemi iyileştirmeyi kolaylaştırır.
*   **Kendi Kendini Geliştirme Mümkündür:** En gelişmiş sistemler, sadece görevleri yerine getirmekle kalmaz, aynı zamanda kendi performanslarını analiz edip zamanla daha iyi hale gelebilirler.

Bu betik, LLM'leri basit araçlar olarak kullanmaktan, onları karmaşık bilişsel mimarilerin temel yapı taşları olarak tasarlamaya geçişi temsil eder.
