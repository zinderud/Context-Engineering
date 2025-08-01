# Prompt Şablonu: Etik Ajanı (Ethics Agent) - Türkçe Açıklama

Bu doküman, `20_templates/PROMPTS/ethics.agent.md` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu dosya, bir ürün, algoritma, veri seti veya sistemin **etik risklerini, potansiyel yanlılıklarını (bias) ve toplumsal etkilerini** denetlemekle görevli bir `/ethics.agent` rolünü tanımlayan, bütüncül bir sistem komutudur.

## Şablonun Amacı

Yapay zeka sistemleri giderek daha karmaşık hale geldikçe, onların adil, şeffaf ve insanlığa faydalı bir şekilde çalıştığından emin olmak kritik bir önem taşımaktadır. Bu şablon, bu tür bir etik denetim sürecini, yapay zekanın kendisini kullanarak otomatikleştirmek, standartlaştırmak ve derinleştirmek için tasarlanmıştır. Ajanın görevi, sadece teknik bir analiz yapmak değil, aynı zamanda bir karardan veya sistemden etkilenecek tüm paydaşları (insanları) göz önünde bulundurarak kapsamlı bir etik değerlendirme sunmaktır.

Bu şablon, aşağıdaki gibi durumlar için idealdir:

*   Bir kredi puanlama algoritmasının, belirli demografik gruplara karşı yanlılık içerip içermediğini denetlemek.
*   Yeni bir veri setinin, gizlilik veya temsil adaleti açısından taşıdığı riskleri analiz etmek.
*   Bir sosyal medya platformunun içerik moderasyon politikasının etik sonuçlarını değerlendirmek.
*   Otonom bir aracın karar verme mekanizmasındaki etik ikilemleri incelemek.

## Şablonun Yapısı ve Ana Bileşenleri

Bu sistem komutu, bir etik denetim sürecinin tüm aşamalarını kapsayan modüler bir yapıya sahiptir:

### 1. `[instructions]` (Talimatlar)
*   **Ne İşe Yarar?** AI ajanına, `/ethics.agent` rolünü ve temel davranış kurallarını atar. Ajana, kanıta dayalı bulgular sunması, değer çatışmalarını ve belirsizlikleri raporlaması talimatını verir.

### 2. `[context_schema]` (Bağlam Şeması)
*   **Ne İşe Yarar?** Etik denetimi yapılacak hedef (veri seti, model, protokol vb.) hakkında hangi bilgilerin sağlanması gerektiğini tanımlar.

### 3. `[workflow]` (İş Akışı)
*   **Ne İşe Yarar?** Etik denetim sürecini sekiz ana aşamaya ayırır:
    1.  **`context_framing`:** İncelenecek konunun amacını, verilerin kaynağını ve bilinen sorunları netleştirme.
    2.  **`stakeholder_mapping`:** Sistemden etkilenecek tüm paydaşların (kullanıcılar, çalışanlar, toplum vb.) kimler olduğunu, haklarını ve potansiyel olarak nasıl zarar görebileceklerini haritalama.
    3.  **`bias_risk_id`:** Veride, tasarımda veya uygulamada bulunan açık veya gizli yanlılıkları ve etik riskleri belirleme.
    4.  **`scenario_analysis`:** En kötü durum, uç durum veya yüksek riskli senaryoları simüle ederek sistemin bu durumlardaki etik davranışını test etme.
    5.  **`mitigation_strategy`:** Tespit edilen riskler ve yanlılıklar için azaltma stratejileri, yeniden tasarım önerileri veya şeffaflık önlemleri geliştirme.
    6.  **`stakeholder_feedback`:** Etkilenen paydaşlardan geri bildirim toplama ve bu geri bildirimlere göre planı güncelleme.
    7.  **`recommendation`:** Karar vericiler için, sistemin kullanımıyla ilgili koşulları ve çözülmemiş riskleri de içeren, yapılandırılmış bir tavsiye sunma.
    8.  **`audit_log`:** Süreç boyunca yapılan tüm analizleri, değişiklikleri ve kararları şeffaf bir şekilde kaydetme.

### 4. `[tools]` (Araçlar)
*   **Ne İşe Yarar?** Bu süreçte kullanılabilecek `bias_detector` (yanlılık tespit edici), `scenario_simulator` (senaryo simülatörü) gibi özel araçları tanımlar.

### 5. `[recursion]` (Özyineleme)
*   **Ne İşe Yarar?** Paydaşlardan gelen geri bildirimlere veya analiz sırasında ortaya çıkan yeni risklere göre denetim sürecinin kendini tekrar etmesini veya derinleştirmesini sağlayan bir mantık sunar.

### 6. `[examples]` (Örnekler)
*   **Ne İşe Yarar?** Her bir iş akışı aşamasının çıktısının (örneğin, bir paydaş haritası, bir risk matrisi) nasıl görünmesi gerektiğine dair somut örnekler sunar.

## Nasıl Kullanılır?

1.  Etik açıdan incelenecek sistem, veri seti veya politika hakkındaki bilgiler toplanır.
2.  Bu şablon ve toplanan bilgiler, güçlü bir LLM'e sistem komutu olarak verilir.
3.  LLM, `/ethics.agent` rolünü benimseyerek, `[workflow]` adımlarını takip eder ve her adım için detaylı etik analizler, tablolar ve risk değerlendirmeleri üretir.
4.  Süreç sonunda, hedefin etik açıdan sağlamlığı, içerdiği riskler ve bu risklerin nasıl azaltılabileceğine dair kapsamlı, eyleme geçirilebilir bir rapor ortaya çıkar.

Bu şablon, teknoloji geliştirme sürecine etik düşünceyi sistematik bir şekilde entegre etmek ve daha sorumlu AI sistemleri oluşturmak için güçlü bir çerçevedir.