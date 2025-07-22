# Şablon: Özyineli Bağlam Çerçevesi (Recursive Context Framework) - Türkçe Açıklama

Bu doküman, `20_templates/recursive_context.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, bu projedeki tüm ileri düzey kavramları bir araya getiren, kendi kendini geliştirebilen ve evrimleşebilen bir bağlam yönetimi için en kapsamlı şablonu sunar.

## Şablonun Amacı

Bu şablon, tek seferlik görevleri yerine getiren veya basit döngülerle çalışan sistemlerin ötesine geçer. Amacı, LLM'in kendi düşünce süreçlerini bir girdi olarak kullanarak, her etkileşimde daha akıllı, daha tutarlı ve daha yetenekli hale gelen **dinamik ve özyineli bir sistem** kurmaktır. Bu, projenin nihai vizyonunu, yani "canlı" ve "öğrenen" bir bağlam oluşturma fikrini hayata geçiren bir çerçevedir.

Bu şablon, aşağıdaki gibi en gelişmiş bağlam mühendisliği desenlerini tek bir yapıda birleştirir:

1.  **Nöral Alan Entegrasyonu:** Bağlamı, akışkan ve sürekli bir "alan" olarak yönetir.
2.  **Sembolik Kalıntı Takibi:** Etkileşimler sırasında ortaya çıkan gizli kalıpları ve yan fikirleri yakalar ve kullanır.
3.  **Protokol Kabuğu Orkestrasyonu:** Akıl yürütme süreçlerini, yapılandırılmış ve yüksek seviyeli protokollerle yönetir.
4.  **Özyineli Kendi Kendini İyileştirme:** Sistemin, kendi çıktılarını değerlendirip, hatalarından öğrenerek bir sonraki adımda daha iyi performans göstermesini sağlar.

## Şablonun Yapısı ve Ana Bileşenleri

Bu şablon, önceki şablonlardaki birçok sınıfı bir araya getiren ve bunları birbiriyle etkileşime sokan `RecursiveFramework` adında merkezi bir sınıf etrafında şekillenir.

### 1. `ModelInterface` (Model Arayüzü)
*   **Ne Yapar?** Farklı LLM'lerle (OpenAI, Anthropic vb.) iletişimi standartlaştırır.

### 2. `NeuralField` (Nöral Alan)
*   **Ne Yapar?** Sistemin ana "hafıza" ve "düşünce" ortamını oluşturur. Bilgi, bu alanda sönümlenen, yankılanan ve çekiciler oluşturan desenler olarak var olur.

### 3. `SymbolicResidue` ve `SymbolicResidueTracker` (Sembolik Kalıntı ve Takipçisi)
*   **Ne Yapar?** Alan içindeki etkileşimlerden doğan "yan ürünleri" (kalıntıları) temsil eder ve yönetir. Bu, sistemin daha derin ve örtük anlam katmanlarını işlemesini sağlar.

### 4. `ProtocolShell` (Protokol Kabuğu)
*   **Ne Yapar?** Sistemin belirli bir görevi yerine getirirken izleyeceği adımları (prosesi), girdileri ve çıktıları tanımlayan yapılandırılmış bir "reçete" sunar.

### 5. `RecursiveFramework` (Özyineli Çerçeve - Ana Sınıf)
*   **Ne Yapar?** Yukarıdaki tüm bileşenleri bir araya getiren ana orkestratördür.
*   **Temel İş Akışı:**
    1.  **Başlatma:** Bir görev tanımı ve başlangıç fikirleriyle (`attractors`) bir `NeuralField` oluşturur.
    2.  **Protokol Oluşturma:** O anki göreve ve alanın durumuna göre dinamik olarak bir `ProtocolShell` oluşturur.
    3.  **Komut Hazırlama:** Hem protokolü hem de alanın o anki durumunu (çekiciler, aktif desenler vb.) içeren zengin bir bağlamı LLM için hazırlar.
    4.  **LLM Çağrısı:** LLM'den, bu zengin bağlamı ve protokolü kullanarak bir cevap üretmesini ister.
    5.  **Geri Besleme:** Gelen cevabı ve bu cevapla ortaya çıkan yeni "kalıntıları" tekrar `NeuralField`'e enjekte ederek alanı günceller.
    6.  **Kendi Kendini İyileştirme:** Eğer cevap belirli kalite kriterlerini karşılamıyorsa, bir "iyileştirme protokolü" başlatır. Bu protokol, LLM'den kendi cevabını ve alanın durumunu analiz ederek daha iyi bir cevap üretmesini ister.
    7.  Bu döngü, tatmin edici bir sonuca ulaşılana veya maksimum deneme sayısına erişilene kadar devam eder.

## Nasıl Kullanılır?

Bu şablon, statik cevaplar yerine, zamanla gelişen ve öğrenen, karmaşık ve uzun soluklu görevler için bir sistem tasarlamak istediğinizde kullanılır:

1.  Bir `RecursiveFramework` nesnesi oluşturun ve temel görev tanımını belirtin.
2.  Sistemin düşünce sürecini yönlendirecek temel fikirleri (`add_attractor` ile) ve iyileştirme stratejilerini (`add_self_improvement_strategy` ile) ekleyin.
3.  `execute_recursive` metodunu bir başlangıç girdisiyle çağırarak sistemi çalıştırın.

Bu şablon, bağlam mühendisliğinin en uç noktasını temsil eder. Amacı, LLM'leri sadece birer araç olarak kullanmak değil, onları kendi bağlamlarını yönetebilen, kendi kendilerine öğrenebilen ve zamanla daha yetenekli hale gelen **otonom bilişsel ajanların** temeli olarak kullanmaktır.
