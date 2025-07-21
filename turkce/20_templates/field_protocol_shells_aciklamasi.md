# Şablon: Alan Protokol Kabukları (Field Protocol Shells) - Türkçe Açıklama

Bu doküman, `20_templates/field_protocol_shells.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, projenin en ileri düzey kavramlarından olan **Alan Protokollerini** hayata geçirmek için bir iskelet ve bir dizi yeniden kullanılabilir şablon sunar.

## Şablonun Amacı

Önceki şablonlar ve rehberler, LLM'lerle etkileşimi programatik olarak nasıl yöneteceğimizi gösterdi. Bu şablon ise bir adım daha ileri giderek, bu etkileşimleri, insan ve yapay zeka tarafından kolayca okunabilen, yüksek seviyeli ve **beyan edici (declarative)** bir dille tanımlanan **protokoller** aracılığıyla yönetmeyi hedefler. Bu dil, projede "Pareto-lang" olarak adlandırılır.

Bir "Protokol Kabuğu" (Protocol Shell), belirli bir görevi (örneğin, iki kavram arasında ortak bir zemin bulma) yerine getirmek için gereken adımları, girdileri, çıktıları ve amacı tanımlayan bir reçetedir. Bu şablon, bu reçeteleri ayrıştırmak (`parse`), doğrulamak (`validate`) ve çalıştırmak (`execute`) için gerekli altyapıyı sağlar.

Ana hedefleri şunlardır:

1.  **Yapılandırılmış Akıl Yürütme:** Karmaşık görevleri, `attractor.scan` (çekici tara), `residue.surface` (kalıntı yüzeye çıkar) gibi standartlaştırılmış operasyonlara bölerek LLM'in akıl yürütme sürecini yapılandırmak.
2.  **Yeniden Kullanılabilirlik:** Farklı görevler için standart protokoller oluşturarak, akıl yürütme desenlerini yeniden kullanılabilir hale getirmek.
3.  **Gözlemlenebilirlik ve Denetlenebilirlik:** Bir görevin hangi adımlarla tamamlandığını net bir şekilde göstererek, süreci daha şeffaf ve denetlenebilir kılmak.
4.  **Teoriyi Pratiğe Dökmek:** `00_foundations` bölümünde anlatılan "Nöral Alanlar", "Çekiciler" ve "Sembolik Kalıntı" gibi soyut kavramları, çalıştırılabilir operasyonlara dönüştürmek.

## Şablonun Yapısı ve Ana Bileşenleri

### 1. `ProtocolParser` (Protokol Ayrıştırıcı)
*   **Ne Yapar?** `.shell` uzantılı dosyalarda veya metinlerde bulunan, Pareto-lang formatındaki protokol tanımlarını okuyup, Python'un anlayabileceği bir sözlük (dictionary) yapısına dönüştürür.

### 2. `ProtocolValidator` (Protokol Doğrulayıcı)
*   **Ne Yapar?** Ayrıştırılmış bir protokolün, belirli bir JSON şemasına uyup uymadığını kontrol eder. Bu, protokollerin standart bir yapıya sahip olmasını garanti eder.

### 3. `ProtocolShell` (Protokol Kabuğu - Ana Sınıf)
*   **Ne Yapar?** Bir protokol tanımını temsil eden ana sınıftır. Protokolü bir dosyadan veya metinden yükleyebilir ve içindeki operasyonları çalıştırabilir.
*   **İşleyişi:**
    1.  Bir `.shell` dosyasını yükler ve `ProtocolParser` ile ayrıştırır.
    2.  Protokolün `process` (süreç) bölümündeki her bir operasyonu (örneğin, `attractor.scan`), kendi içindeki eşleşen bir metoda (örneğin, `attractor_scan` metodu) bağlar.
    3.  `execute` metodu çağrıldığında, bu operasyonları sırayla çalıştırır ve durum (state) bilgisini bir adımdan diğerine aktarır.

### 4. Uygulama Örnekleri (Özelleşmiş Protokoller)
*   **`AttractorCoEmergeProtocol`:** İki farklı kavram veya "alan" arasındaki ortak çekicileri (fikirleri) bulmayı ve bunları birleştirmeyi amaçlayan bir protokolü uygular.
*   **`RecursiveEmergenceProtocol`:** Bir alanın kendi kendine evrilmesini, yeni fikirler üretmesini ve kendi kendini sorgulamasını (`self-prompt`) sağlayan, projenin en gelişmiş felsefesini yansıtan bir protokolü uygular.

## Nasıl Kullanılır?

Bu şablon, belirli bir akıl yürütme görevini otomatikleştirmek istediğinizde kullanılır:

1.  Görevinizi tanımlayan bir `.shell` dosyası oluşturun. Bu dosyada görevin `niyetini`, `girdilerini`, `süreç adımlarını` ve `çıktılarını` belirtin.
2.  Bu görevin her bir süreç adımını (operasyonunu) yerine getirecek Python metotlarını içeren, `ProtocolShell` sınıfından türetilmiş yeni bir sınıf yazın.
3.  Oluşturduğunuz bu sınıfı kullanarak `.shell` dosyasını yükleyin.
4.  `execute` metodunu, başlangıç verileriyle birlikte çağırarak protokolü çalıştırın.

Bu şablon, LLM'lerle etkileşimi, basit komutlar vermekten, belirli bir amaca hizmet eden, standartlaştırılmış ve yeniden kullanılabilir **bilişsel süreçler (cognitive processes)** tasarlamaya ve otomatikleştirmeye doğru bir adımdır.