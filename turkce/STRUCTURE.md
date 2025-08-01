# Context-Engineering – Yapısal Bakış (Türkçe Özet)

Bu doküman, projenin `STRUCTURE.md` dosyasının Türkçe bir özetidir ve projenin yapısını, felsefesini ve öğrenme yolunu ana hatlarıyla açıklar.

## Projenin Amacı ve Felsefesi

Bu projenin temel amacı, "Prompt Mühendisliği"nin ötesine geçmektir:

*   **Prompt Mühendisliği:** Modele **ne söylediğinize** odaklanır.
*   **Bağlam Mühendisliği:** Modelin gördüğü **diğer her şeye** odaklanır.

Proje, bu "diğer her şeyi" temel prensiplerden başlayarak, basit ve çalışan kod örnekleriyle öğretmeyi hedefler.

## 1. Klasörlerin Haritası ve Metaforlar

Proje, karmaşık konuları somutlaştırmak için biyolojik metaforlar kullanır. Her klasörün rolü aşağıda özetlenmiştir:

| Klasör | Rolü (Açık Türkçe) | Temel Prensip Metaforu |
|---|---|---|
| `00_foundations` | Teori ve sezgiler. Kısa ve öz okumalar. | Atomlar → Moleküller → Hücreler → Organlar → Sinir Sistemleri → Alanlar |
| `10_guides_zero_to_hero` | Çalıştırabileceğiniz, değiştirebileceğiniz interaktif rehberler. | Kimya seti |
| `20_templates` | Kopyalayıp yapıştırabileceğiniz hazır kod parçacıkları. | Lego tuğlaları |
| `30_examples` | Baştan sona tamamlanmış, giderek zorlaşan mini uygulamalar. | Model organizmalar |
| `40_reference` | Derinlemesine teknik incelemeler ve değerlendirme kılavuzları. | Ders kitabı ekleri |
| `50_contrib` | Topluluk katkıları için ayrılmış alan. | Açık laboratuvar tezgahı |
| `60_protocols` | Yapılandırılmış protokoller ve kabuklar (shells). | DNA dizilimleri |
| `70_agents` | Protokolleri kullanan bağımsız ajan demoları. | Kök hücre kültürleri |
| `80_field_integration` | Alan protokolleri ile tamamlanmış projeler. | Bütün organizmalar |
| `cognitive-tools` | Gelişmiş bilişsel çerçeveler ve mimariler. | Genişletilmiş sinir sistemleri |

## 2. Öğrenme Yolu (Sıfırdan İleri Seviyeye)

Proje, adım adım ilerleyen bir öğrenme yolu sunar:

1.  **Temelleri Anlama (`00_foundations`):**
    *   `README.md` ve `01_atoms_prompting.md` ile başlayarak bağlamın ne anlama geldiğini ve tekil komutların neden yetersiz kaldığını öğrenin.
    *   Biyolojik metafor zincirini takip ederek (`02_molecules`'den `10_field_orchestration`'a kadar) bilginizi katman katman inşa edin.

2.  **Pratik Yapma (`10_guides_zero_to_hero`):**
    *   Jupyter Notebook formatındaki rehberleri çalıştırarak, değiştirerek ve sonuçları gözlemleyerek uygulamalı deneyim kazanın.

3.  **Uygulama Geliştirme (`20_templates` ve `30_examples`):**
    *   `20_templates` klasöründeki hazır şablonları kendi projeleriniz için bir başlangıç noktası olarak kullanın.
    *   `30_examples` klasöründeki giderek karmaşıklaşan gerçek dünya örneklerini inceleyerek öğrendiklerinizi pekiştirin.

4.  **Ustalığa Ulaşma (`40_reference`, `60_protocols`, `cognitive-tools`):**
    *   Daha derinlemesine teknik bilgi için referans dokümanlarını okuyun.
    *   Protokoller ve bilişsel araçlar gibi ileri seviye çerçeveleri keşfedin.

## 3. İleri Seviye Kavramlar

*   **Protokol Kabuk Çerçevesi (`60_protocols`):** Karmaşık bağlam operasyonlarını düzenlemek için yapılandırılmış "kabuklar" (şablonlar) sunar. Bu, işlemleri beyan etmeyi, yinelemeli kendini iyileştirmeyi ve denetlenebilirliği kolaylaştırır.

*   **Bilişsel Araçlar Çerçevesi (`cognitive-tools`):** Modelin yeteneklerini artıran, yeniden kullanılabilir akıl yürütme kalıpları sağlar. Bunlar, farklı akıl yürütme modları için şablonlar ve programlar içerir.

*   **Sinirsel Alan Çerçevesi (Neural Fields):** Bağlamı ayrık "token"lar yerine sürekli bir ortam olarak ele alır. Bu yaklaşım, bilginin kalıcılığı (rezonans), anlam kümelerinin oluşumu (çekiciler - attractors) ve karmaşık görevler için alanların düzenlenmesi gibi kavramları içerir.

## 4. Projenin Tasarım Prensipleri

Proje, Andrej Karpathy'den ilham alan şu basit kuralları benimser:

1.  **Minimal Başla:** Mümkün olan en küçük, çalışabilir bağlam ile başla.
2.  **Yinelemeli Ekle:** Sadece modelin eksik olduğu kanıtlanan şeyi ekle.
3.  **Her Şeyi Ölç:** Token maliyeti, gecikme süresi, kalite puanı gibi metrikleri sürekli ölç.
4.  **Acımasızca Sil:** Gereksiz bilgiyi eklemek yerine, alakasız olanı çıkarmak daha iyidir.
5.  **Kod > Slaytlar:** Her kavramın çalıştırılabilir bir kod örneği vardır.
6.  **Yinelemeli Düşün:** Kendi kendini geliştiren bağlamlar oluştur.
