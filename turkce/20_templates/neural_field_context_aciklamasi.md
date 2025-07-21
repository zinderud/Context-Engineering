# Şablon: Nöral Alan Bağlamı (Neural Field Context) - Türkçe Açıklama

Bu doküman, `20_templates/neural_field_context.yaml` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu YAML dosyası, projenin en ileri ve teorik konsepti olan **Nöral Alanları** yapılandırmak ve yönetmek için kullanılan kapsamlı bir şablondur.

## Şablonun Amacı

`minimal_context.yaml` şablonu, bağlamı ayrık parçalar (metin, geçmiş, örnekler) olarak ele alırken, bu şablon bağlamı tamamen farklı bir şekilde, yani **sürekli bir alan** olarak modeller. Bu alanda bilgi, belirli bir konuma sahip token'lar olarak değil, alan boyunca yayılan, birbiriyle etkileşen (rezonans), zamanla sönümlenen (decay) ve kararlı yapılar (çekiciler) oluşturan desenler (patterns) olarak var olur.

Bu şablonun amacı, bu dinamik ve akışkan alanın davranışını kontrol eden tüm fiziksel parametreleri, operasyonları ve kuralları tek bir yerden yapılandırmaktır. Bu, LLM'in daha çok insan beyninin çalışma şekline benzer şekilde, yani esnek, kalıcı ve kendi kendini organize eden bir yapıda bilgi işlemesini sağlamayı hedefler.

## Şablonun Yapısı ve Ana Bileşenleri

Bu şablon, bir nöral alanın neredeyse tüm yönlerini kontrol eden çok sayıda bölüm içerir:

### 1. `field` (Alan Parametreleri)
*   **Ne İşe Yarar?** Alanın temel "fizik kurallarını" belirler.
*   **Önemli Alanlar:**
    *   `decay_rate`: Bilgi desenlerinin alanda ne hızla sönümleneceğini (unutulacağını) belirler.
    *   `boundary_permeability`: Yeni bilginin alana ne kadar kolay girebileceğini kontrol eder.
    *   `resonance_bandwidth`: Fikirlerin birbiriyle ne kadar geniş bir alanda etkileşime gireceğini ayarlar.
    *   `attractor_formation_threshold`: Bir fikrin, alanın ana teması (çekici) haline gelmesi için ne kadar güçlü olması gerektiğini belirler.

### 2. `attractors` (Başlangıç Çekicileri)
*   **Ne İşe Yarar?** Alanı boş bir tuval olarak başlatmak yerine, ona başlangıçta bir "şekil" veya "eğilim" verir. Bunlar, alanın etrafında organize olacağı temel, kararlı fikirlerdir (örneğin, modelin temel rolü veya görevi).

### 3. `resonance` (Rezonans Yapılandırması)
*   **Ne İşe Yarar?** Alanın, iki fikir arasındaki anlamsal ilişkiyi veya uyumu nasıl hesaplayacağını tanımlar.

### 4. `persistence` (Kalıcılık Mekanizmaları)
*   **Ne İşe Yarar?** Bilginin alanda zamanla nasıl hayatta kalacağını yönetir. Örneğin, önemli fikirlerin (çekicilerin) daha yavaş unutulmasını sağlar (`attractor_protection`).

### 5. `operations` (Alan Operasyonları)
*   **Ne İşe Yarar?** Alan üzerinde gerçekleştirilebilecek temel işlemleri (yeni bilgi ekleme, bir fikri zayıflatma veya güçlendirme) yapılandırır.

### 6. `symbolic_residue` (Sembolik Kalıntı Takibi)
*   **Ne İşe Yarar?** `07_recursive_patterns` rehberinde tanıtılan "sembolik kalıntı" kavramının takibini etkinleştirir ve yapılandırır.

### 7. `metrics` (Ölçüm ve Metrikler)
*   **Ne İşe Yarar?** Alanın sağlığını ve durumunu ölçmek için kullanılacak metriklerin (tutarlılık, kararlılık vb.) nasıl hesaplanacağını tanımlar.

### 8. `output` (Çıktı Yapılandırması)
*   **Ne İşe Yarar?** Alanın o anki durumunun, LLM'e gönderilecek komuta nasıl bir formatta ekleneceğini belirler.

### 9. `integration` (Entegrasyon Seçenekleri)
*   **Ne İşe Yarar?** Alanın durumunun kaydedilmesi, yüklenmesi veya harici sistemlerle entegrasyonu gibi teknik detayları yapılandırır.

### 10. `recursive` (Özyineli Alan Uzantıları)
*   **Ne İşe Yarar?** Alanın kendi durumunu analiz edip, kendini iyileştirmek için özyineli döngüler başlatma yeteneğini etkinleştirir ve yapılandırır.

### 11. `protocols` (Protokol Entegrasyonu)
*   **Ne İşe Yarar?** Bu alanın, `field_protocol_shells.py` şablonunda tanımlanan yapılandırılmış protokollerle nasıl etkileşime gireceğini belirler.

### 12. `advanced` (Gelişmiş Alan Dinamikleri)
*   **Ne İşe Yarar?** Çoklu alan orkestrasyonu (örneğin, biri mantık, diğeri yaratıcılık için iki ayrı alanın birlikte çalışması) veya alanın "kaosun kenarında" çalışmasını sağlama gibi en ileri düzey deneysel özellikleri içerir.

## Nasıl Kullanılır?

Bu YAML dosyası, `20_templates/control_loop.py` içindeki `NeuralFieldControlLoop` gibi, nöral alanları destekleyen bir kontrol mekanizması tarafından yüklenir. Bir Python betiği, bu yapılandırma dosyasını okuyarak bir `NeuralField` nesnesi oluşturur ve alanın tüm davranışlarını bu dosyadaki parametrelere göre yönetir.

Bu şablon, LLM etkileşimlerini yönetmek için statik ve ayrık bir yaklaşımdan, projenin temel felsefesini yansıtan dinamik, sürekli ve kendi kendini organize eden bir yaklaşıma geçişi temsil eder.