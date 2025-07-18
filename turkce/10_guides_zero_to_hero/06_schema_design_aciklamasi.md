# Rehber 06: Şema Tasarımı (Schema Design) - Türkçe Açıklama

Bu doküman, `10_guides_zero_to_hero/06_schema_design.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, yapay zeka ile insan arasındaki iletişimi daha sağlam, tutarlı ve öngörülebilir hale getirmek için **veri şemalarının** nasıl kullanılacağını öğretir.

## Betiğin Amacı

LLM'ler doğal dilde harikadır, ancak bazen çıktıları dağınık, tutarsız veya programatik olarak işlenmesi zor olabilir. Bu rehber, bu sorunu çözmek için bir "sözleşme" oluşturma fikrini sunar. Bu sözleşme, bir **şema** (genellikle JSON Schema formatında) kullanılarak yapılır. Şema, LLM'e hem ondan ne beklediğimizi net bir şekilde anlatır hem de onun ürettiği çıktının istediğimiz yapıda olup olmadığını otomatik olarak kontrol etmemizi sağlar.

Bu betik, şema tabanlı bağlam mühendisliği için pratik araçlar ve desenler sunar. Ana hedefleri şunlardır:

1.  **Şema Tabanlı İletişimi Tanıtmak:** LLM'e, cevabını uyması gereken bir yapı (şema) vererek nasıl daha tutarlı çıktılar alınacağını göstermek.
2.  **Otomatik Doğrulama Sağlamak:** LLM tarafından üretilen çıktının, tanımlanan şemaya uyup uymadığını programatik olarak doğrulayan (`validate`) mekanizmalar kurmak.
3.  **Kendi Kendini Düzelten Döngüler Oluşturmak:** Eğer LLM'in çıktısı şemaya uymazsa, hata mesajını LLM'e geri besleyerek kendi hatasını düzeltmesini ve geçerli bir çıktı üretmesini sağlamak.
4.  **Karmaşık ve Özyineli (Recursive) Veri Yapıları Tasarlamak:** Bir dosya sistemi ağacı gibi, kendi içinde kendini tekrar eden karmaşık veri yapılarını modellemek için **fraktal şemalar** oluşturmak.
5.  **Şema Etkinliğini Ölçmek:** Bir şema kullanmanın, LLM'in ne kadar başarılı (veya başarısız) bir şekilde yapılandırılmış veri ürettiğini metrikler ve görselleştirmelerle analiz etmek.

## Betikteki Ana Sınıflar ve Kavramlar

Betiğin kalbini, şema tabanlı etkileşimleri yöneten üç ana sınıf oluşturur:

### 1. `JSONSchema`
*   **Ne Yapar?** Bir JSON şemasını temsil eden, onu yöneten ve onunla ilgili işlemler yapan temel sınıftır.
*   **Temel Yetenekleri:**
    *   **`validate(instance)`:** Verilen bir JSON nesnesinin şemaya uyup uymadığını kontrol eder.
    *   **`generate_example()`:** LLM'i kullanarak, şemaya uygun örnek bir JSON nesnesi üretir.
    *   **`generate_prompt_with_schema(task)`:** Bir görevi, "cevabın bu şemaya uymalı" talimatıyla birlikte paketleyerek LLM için hazır bir komut oluşturur.

### 2. `SchemaContext`
*   **Ne Yapar?** `JSONSchema` sınıfını kullanarak, LLM ile baştan sona şema tabanlı bir diyalog yönetir.
*   **Temel İş Akışı:**
    1.  Kullanıcının isteğini ve uyması gereken şemayı birleştirerek bir komut oluşturur.
    2.  LLM'den bir cevap alır.
    3.  Gelen cevabı ayrıştırır (`parse`) ve şemaya göre doğrular (`validate`).
    4.  Eğer cevap geçersizse ve yeniden deneme açıksa, hata mesajıyla birlikte LLM'e yeni bir istek göndererek hatasını düzeltmesini ister.
    5.  Sonunda geçerli bir yapılandırılmış cevap döner.

### 3. `FractalSchema` (Fraktal Şema)
*   **Ne Yapar?** Kendi içinde kendini tekrar eden (özyineli) veri yapılarını tanımlamak ve doğrulamak için kullanılır. Bir klasörün içinde başka klasörlerin olması gibi.
*   **Temel Yetenekleri:**
    *   Bir şema içindeki özyineli yolları (`recursion_paths`) tanımlar.
    *   Üretilen bir örnekteki iç içe geçmişlik (özyineli) derinliğini analiz eder.
    *   LLM'den belirli bir derinlikte özyineli örnekler üretmesini isteyebilir.

## Önemli Çıkarımlar

Bu rehber, LLM'lerle çalışırken yapı ve öngörülebilirliğin önemini vurgular:

*   **Şemalar Sözleşmelerdir:** Şema kullanmak, LLM ile aranızda bir "arayüz sözleşmesi" oluşturur. Bu, hem beklentileri netleştirir hem de sonuçları güvenilir kılar.
*   **Doğrula, Güvenme:** LLM'in her zaman mükemmel yapılandırılmış JSON üreteceğini varsaymayın. Her zaman doğrulayın.
*   **Hatalardan Öğret:** Doğrulama hataları bir sorun değil, LLM'in kendini düzeltmesi için bir fırsattır. Hata mesajlarını geri beslemek, sistemin sağlamlığını artırır.
*   **Yapı, Düşünceyi Şekillendirir:** LLM'e karmaşık bir şema vermek, onu sadece belirli bir formatta çıktı vermeye zorlamakla kalmaz, aynı zamanda o yapıya uygun şekilde düşünmeye de teşvik eder.
*   **Fraktal Yapılar Her Yerde:** Organizasyon şemaları, dosya sistemleri, tartışma başlıkları gibi birçok gerçek dünya problemi, fraktal şemalarla zarif bir şekilde modellenebilir.

Bu betik, serbest metin üreten bir LLM'i, güvenilir ve yapılandırılmış veri üreten bir API'ye dönüştürmenin yol haritasını sunar.
