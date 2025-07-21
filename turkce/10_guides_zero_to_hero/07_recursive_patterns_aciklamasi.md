# Rehber 07: Özyineli Desenler (Recursive Patterns) - Türkçe Açıklama

Bu doküman, `10_guides_zero_to_hero/07_recursive_patterns.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, Bağlam Mühendisliği serisinin zirvesini temsil eder ve yapay zekanın kendi kendine düşünmesini, öğrenmesini ve gelişmesini sağlayan **özyineli (recursive)** desenleri tanıtır.

## Betiğin Amacı

Önceki rehberler, LLM'i belirli görevleri yerine getirmesi için nasıl yönlendireceğimizi öğretti. Bu son rehber ise LLM'e, kendi düşünce süreçlerini bir girdi olarak kullanarak, sürekli bir geri bildirim döngüsü içinde kendi kendini nasıl iyileştirebileceğini öğretir. Bu, bir görevi tek seferde çözmek yerine, onu tekrar tekrar ele alarak daha derin bir anlayışa ve daha kaliteli bir sonuca ulaşma sanatıdır.

Bu betik, aşağıdaki gibi son derece güçlü ve ileri düzey özyineli desenleri uygulamak için Python sınıfları sunar:

1.  **Kendi Üzerine Düşünme (Self-Reflection):** Modelin, ürettiği bir cevabı eleştirmesini, zayıf yönlerini bulmasını ve bu eleştirilere dayanarak daha iyi bir cevap üretmesini sağlamak.
2.  **Kendi Kendini Başlatma (Recursive Bootstrapping):** Modelin, bir probleme yönelik basit bir çözüm stratejisiyle başlayıp, her adımda kendi stratejisini daha karmaşık ve daha sofistike bir üst seviyeye taşımasını sağlamak.
3.  **Sembolik Kalıntı (Symbolic Residue):** Modelin bir metni işlerken sadece ana çıktıyı değil, aynı zamanda bu süreçte ortaya çıkan "yan ürünleri", "sezgileri" veya "gizli kalıpları" (yani sembolik kalıntıyı) fark etmesini, biriktirmesini ve bir sonraki adımda bu birikmiş bilgiyi de kullanmasını sağlamak.

## Betikteki Ana Sınıflar (Özyineli Desenler)

Betiğin kalbini, her biri farklı bir özyineli düşünce süreci uygulayan üç ana sınıf oluşturur:

### 1. `SelfReflection` (Kendi Üzerine Düşünme)
*   **Ne Yapar?** Bir ilk cevap üretir. Ardından, "Bu cevabı nasıl daha iyi yapabilirim? Hangi eksikleri var?" gibi bir komutla kendi cevabını analiz eder. Bu analizden yola çıkarak, kendini düzelten ve geliştiren yeni bir cevap üretir. Bu döngü, belirli bir kalite eşiğine ulaşana veya maksimum deneme sayısına erişene kadar devam eder.
*   **Benzetme:** Bir makale taslağı yazıp, sonra o taslağı bir editör gözüyle okuyup, kırmızı kalemle düzeltmeler yapıp son halini vermeye benzer.

### 2. `RecursiveBootstrapping` (Kendi Kendini Başlatma)
*   **Ne Yapar?** Bir problemi çözmek için önce "acemi" seviyesinde bir yaklaşım geliştirir. Sonraki adımda, bu acemi yaklaşımı bir girdi olarak alır ve "çırak" seviyesinde daha iyi bir yaklaşım geliştirir. Bu süreç, "usta" ve "yenilikçi" seviyelerine kadar devam eder. Her adım, bir öncekinin üzerine inşa edilir.
*   **Benzetme:** Bir müzisyenin önce temel akorları öğrenmesi, sonra bu temelle basit şarkılar çalması, ardından daha karmaşık besteler yapması ve en sonunda kendi özgün stilini yaratması gibidir.

### 3. `SymbolicResidue` (Sembolik Kalıntı)
*   **Ne Yapar?** Bu, en soyut ve güçlü desendir. LLM bir metni işlerken, sadece istenen çıktıyı üretmekle kalmaz, aynı zamanda bu süreçte aklına gelen yan fikirleri, belirsizlikleri, ortaya çıkan yeni bağlantıları veya "söylenmemiş gerçekleri" de bir kenara not eder. Bir sonraki adımda, hem orijinal görevi hem de bu birikmiş "kalıntıyı" dikkate alarak daha derin ve daha bütüncül bir çıktı üretir.
*   **Benzetme:** Bir dedektifin bir olay yerini incelerken sadece bariz delilleri (çıktı) toplamakla kalmayıp, aynı zamanda atmosferdeki tuhaflıkları, insanların davranışlarındaki gariplikleri ve kendi sezgilerini (kalıntı) de bir deftere not alıp, sonunda tüm bu parçaları birleştirerek olayı çözmesine benzer.

## Önemli Çıkarımlar

Bu son rehber, Bağlam Mühendisliği'nin nihai hedefini özetler: LLM'leri, talimatları körü körüne uygulayan araçlar olmaktan çıkarıp, kendi düşünce süreçlerinin farkında olan, kendilerini geliştirebilen ve daha derin bir "anlayışa" ulaşabilen sistemlere dönüştürmek.

*   **Özyineleme, Derinlik Katar:** Bir problemi tek seferde çözmek yerine, döngüsel olarak tekrar ele almak, daha katmanlı ve sağlam çözümler üretir.
*   **Meta-Biliş (Metacognition) Güçtür:** Bir modelin kendi düşüncesi hakkında düşünebilmesi (`SelfReflection`), onun en büyük yeteneklerinden biridir.
*   **Gelişim Bir Süreçtir:** Karmaşık yetenekler, basit temellerin üzerine katman katman inşa edilir (`RecursiveBootstrapping`).
*   **Görünmeyeni Görmek:** En değerli içgörüler, genellikle doğrudan çıktıda değil, işlem sırasında ortaya çıkan yan ürünlerde ve kalıntılarda gizlidir (`SymbolicResidue`).

Bu rehberle birlikte, `10_guides_zero_to_hero` serisi tamamlanmış olur. Artık Bağlam Mühendisliği'nin temel teorilerinden en gelişmiş pratik uygulamalarına kadar tüm süreci görmüş oldunuz.
