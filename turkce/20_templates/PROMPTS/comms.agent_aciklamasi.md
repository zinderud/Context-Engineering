# Prompt Şablonu: İletişim Ajanı (Comms Agent) - Türkçe Açıklama

Bu doküman, `20_templates/PROMPTS/comms.agent.md` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu dosya, belirli bir konuda (örneğin, bir değişiklik yönetimi, kriz iletişimi, ürün lansmanı) farklı paydaş gruplarına yönelik **stratejik bir iletişim planı** oluşturmak ve yönetmekle görevli bir `/comms.agent` (İletişim Ajanı) rolünü tanımlayan, bütüncül bir sistem komutudur.

## Şablonun Amacı

Etkili iletişim, doğru mesajı, doğru kişiye, doğru kanaldan ve doğru zamanda iletme sanatıdır. Bu şablon, bu karmaşık süreci, yapay zekayı kullanarak sistematik, denetlenebilir ve stratejik bir hale getirmeyi amaçlar. Ajanın görevi, jenerik veya herkese uyan tek bir mesaj hazırlamak değil, her bir paydaş grubunun endişelerini, tercihlerini ve beklentilerini analiz ederek onlara özel, hedefe yönelik bir iletişim planı tasarlamaktır.

Bu şablon, aşağıdaki gibi durumlar için idealdir:

*   Şirket içi büyük bir değişikliğin çalışanlara duyurulması.
*   Yeni bir ürünün farklı müşteri segmentlerine ve basına tanıtılması.
*   Bir kriz anında kamuoyuna, müşterilere ve yatırımcılara yönelik iletişimin yönetilmesi.
*   Farklı departmanlar arasında (örneğin, mühendislik ve pazarlama) bir proje hakkında ortak bir anlayış oluşturulması.

## Şablonun Yapısı ve Ana Bileşenleri

Bu sistem komutu, bir iletişim stratejisi oluşturmanın tüm aşamalarını kapsayan modüler bir yapıya sahiptir:

### 1. `[instructions]` (Talimatlar)
*   **Ne İşe Yarar?** AI ajanına, `/comms.agent` rolünü ve temel davranış kurallarını atar. Ajana, adım adım ilerlemesi, her kitleye özel mesaj hazırlaması ve süreci şeffaf bir şekilde belgelemesi talimatını verir.

### 2. `[context_schema]` (Bağlam Şeması)
*   **Ne İşe Yarar?** İletişim planını oluşturmak için hangi bilgilerin gerekli olduğunu tanımlar.
    *   **`strategy`:** İletişimin genel amacı, kapsamı ve hedefleri.
    *   **`audience`:** Hedef kitlelerin segmentleri (çalışanlar, yöneticiler, müşteriler vb.), büyüklükleri, tercihleri ve endişeleri.
    *   **`session`:** O anki görevin özel hedefleri ve öncelikleri.

### 3. `[workflow]` (İş Akışı)
*   **Ne İşe Yarar?** İletişim planını oluşturma sürecini yedi ana aşamaya ayırır:
    1.  **`audience_profiling`:** Hedef kitlelerin detaylı bir şekilde analiz edilmesi.
    2.  **`context_clarification`:** İletişimin amacının ve arka planının netleştirilmesi.
    3.  **`message_mapping`:** Her bir hedef kitle için özel olarak hazırlanmış ana mesajların oluşturulması.
    4.  **`channel_timing_optimization`:** Her mesaj için en uygun iletişim kanalının (email, toplantı, basın bülteni) ve zamanlamasının seçilmesi.
    5.  **`feedback_cycle_integration`:** Geri bildirim toplamak ve planı revize etmek için mekanizmalar tanımlanması.
    6.  **`risk_scenario_simulation`:** Olası kriz senaryolarının (örneğin, sosyal medyada olumsuz tepki) simüle edilmesi ve bunlara yönelik hazırlık yapılması.
    7.  **`revision_audit_log`:** Planda yapılan tüm değişikliklerin gerekçeleriyle birlikte kaydedilmesi.

### 4. `[tools]` (Araçlar)
*   **Ne İşe Yarar?** Bu süreçte kullanılabilecek `sentiment_monitor` (duygu analizi), `message_optimizer` (mesaj iyileştirici) gibi özel araçları tanımlar.

### 5. `[recursion]` (Özyineleme)
*   **Ne İşe Yarar?** Toplanan geri bildirimlere veya değişen koşullara göre iletişim planının kendi kendini nasıl revize edip iyileştirebileceğine dair bir mantık sunar.

### 6. `[examples]` (Örnekler)
*   **Ne İşe Yarar?** Her bir iş akışı aşamasının çıktısının (örneğin, bir hedef kitle tablosu, bir mesaj haritası) nasıl görünmesi gerektiğine dair somut örnekler sunar.

## Nasıl Kullanılır?

1.  Bir iletişim ihtiyacı doğduğunda, bu ihtiyacın detayları (`[context_schema]`'ya uygun olarak) hazırlanır.
2.  Bu şablon ve hazırlanan bağlam, güçlü bir LLM'e sistem komutu olarak verilir.
3.  LLM, `/comms.agent` rolünü benimseyerek, `[workflow]` adımlarını takip eder ve her adım için detaylı çıktılar (tablolar, analizler, mesaj taslakları) üretir.
4.  Sonuç olarak, farklı paydaşlara yönelik, riskleri hesaplanmış, geri bildirime açık ve tamamen belgelenmiş, kapsamlı bir iletişim stratejisi ortaya çıkar.

Bu şablon, iletişimi reaktif bir görev olmaktan çıkarıp, proaktif, stratejik ve veri odaklı bir sürece dönüştürmek için güçlü bir çerçevedir.