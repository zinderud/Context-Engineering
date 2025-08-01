# Doğrulama Şablonları

Bu belge, bir dil modelinin (LLM) ürettiği sonuçların doğruluğunu, tutarlılığını ve kalitesini **kendi kendine kontrol etmesi** için tasarlanmış yapılandırılmış istem (prompt) şablonlarını içerir. Bu şablonlar, modelin daha güvenilir olmasını sağlamak ve hataları (halüsinasyonları) en aza indirmek için kritik öneme sahiptir.

## Temel Doğrulama Şablonları

1.  **Çözüm Doğrulama Şablonu:**
    *   **Amaç:** Üretilen bir çözümün veya cevabın doğruluğunu adım adım kontrol etmek.
    *   **Süreç:** Problemin doğru anlaşılıp anlaşılmadığını, kullanılan yöntemin uygunluğunu, hesaplamaların doğruluğunu ve mantıksal adımların tutarlılığını kontrol eder.
    *   **Kullanım:** Özellikle matematik, mantık ve mühendislik gibi alanlarda üretilen çözümlerin doğruluğundan emin olmak için kullanılır.

2.  **Bilgi Kontrolü (Fact-Checking) Şablonu:**
    *   **Amaç:** Bir metin içindeki olgusal iddiaların (tarihler, isimler, istatistikler vb.) doğruluğunu teyit etmek.
    *   **Süreç:** Metindeki her bir iddiayı ayrı ayrı ele alır ve güvenilir bilgi kaynaklarına göre doğruluğunu, yanlışlığını veya belirsizliğini değerlendirir.
    *   **Kullanım:** Tarihsel veya bilimsel metinlerin, özetlerin veya haberlerin doğruluğunu kontrol etmek için idealdir.

3.  **Tutarlılık Kontrolü Şablonu:**
    *   **Amaç:** Bir metnin kendi içinde çelişki barındırıp barındırmadığını kontrol etmek.
    *   **Süreç:** Metindeki ana fikirlerin, tanımların ve argümanların birbiriyle uyumlu olup olmadığını, kullanılan terimlerin tutarlılığını ve genel mantık akışını inceler.
    *   **Kullanım:** Uzun metinlerde, karmaşık argümanlarda veya birden fazla kaynaktan sentezlenmiş içeriklerde iç tutarlılığı sağlamak için kullanılır.

## Gelişmiş Doğrulama Şablonları

1.  **Kapsamlı Hata Analizi Şablonu:**
    *   **Amaç:** Bir içeriği sadece olgusal doğruluk açısından değil, aynı zamanda mantıksal, bağlamsal, dilbilimsel ve yapısal hatalar açısından da derinlemesine incelemek.
    *   **Kullanım:** Maksimum doğruluk gerektiren kritik metinlerin (raporlar, resmi belgeler vb.) incelenmesi için kullanılır.

2.  **Alternatif Bakış Açısı Analizi Şablonu:**
    *   **Amaç:** Bir metnin taraflı olup olmadığını veya önemli bakış açılarını dışarıda bırakıp bırakmadığını analiz etmek.
    *   **Süreç:** Metnin altında yatan varsayımları sorgular ve konuya farklı bir ideolojik, kültürel veya disipliner açıdan yaklaşıldığında nasıl görüneceğini değerlendirir.
    *   **Kullanım:** Tartışmalı konularda dengeli ve adil bir içerik oluşturmak için kullanılır.

3.  **Uygulanabilirlik Doğrulaması Şablonu:**
    *   **Amaç:** Önerilen bir çözümün sadece teorik olarak değil, pratik olarak da hayata geçirilebilir olup olmadığını değerlendirmek.
    *   **Süreç:** Teknik fizibilite, maliyet, zaman, gerekli kaynaklar ve potansiyel riskler gibi gerçek dünya faktörlerini analiz eder.
    *   **Kullanım:** Mühendislik tasarımları, iş planları veya proje önerileri gibi pratik çözümlerin değerlendirilmesinde kullanılır.

## Kendi Kendini Düzeltme Döngüsü

Bu şablonların en güçlü kullanımı, modelin önce bir çözüm üretip, ardından bir doğrulama şablonu kullanarak kendi çözümünü kontrol ettiği ve bulduğu hataları düzelterek daha iyi bir sonuca ulaştığı **kendi kendini düzeltme döngüleri** oluşturmaktır. Bu, yapay zekanın daha güvenilir ve otonom hale gelmesini sağlar.
