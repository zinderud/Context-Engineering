# Prompt Şablonu: Durum Tespiti Ajanı (Diligence Agent) - Türkçe Açıklama

Bu doküman, `20_templates/PROMPTS/diligence.agent.md` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu dosya, bir hedef (örneğin, bir startup, bir proje, bir satıcı firma) hakkında kapsamlı bir **durum tespiti (due diligence)** yapmakla görevli bir `/diligence.agent` rolünü tanımlayan, bütüncül bir sistem komutudur.

## Şablonun Amacı

Bir yatırım yapmadan, bir şirketle ortaklık kurmadan veya yeni bir teknolojiyi benimsemeden önce, o hedefin tüm yönleriyle derinlemesine incelenmesi gerekir. Bu şablon, bu karmaşık ve kritik süreci, yapay zekayı kullanarak sistematik, denetlenebilir ve son derece yapılandırılmış bir hale getirmeyi amaçlar. Ajanın görevi, kendisine sunulan verileri (finansal tablolar, kod tabanı, sunumlar vb.) analiz ederek, hedefin güçlü ve zayıf yönlerini, fırsatlarını ve tehditlerini ortaya çıkarmaktır.

Bu şablon, aşağıdaki gibi durumlar için idealdir:

*   Bir yatırımcının, yatırım yapmayı düşündüğü bir startup'ı değerlendirmesi.
*   Bir şirketin, satın almayı düşündüğü başka bir şirketi incelemesi.
*   Yeni bir yazılım projesinin teknik, pazar ve ekip açısından risklerinin analiz edilmesi.
*   Bir tedarikçinin güvenilirliğinin ve uyumluluğunun denetlenmesi.

## Şablonun Yapısı ve Ana Bileşenleri

Bu sistem komutu, bir durum tespiti sürecinin tüm aşamalarını kapsayan modüler bir yapıya sahiptir:

### 1. `[instructions]` (Talimatlar)
*   **Ne İşe Yarar?** AI ajanına, `/diligence.agent` rolünü ve temel davranış kurallarını atar. Ajana, kanıta dayalı bulgular sunması, varsayımlarını belirtmesi ve süreci adım adım takip etmesi talimatını verir.

### 2. `[context_schema]` (Bağlam Şeması)
*   **Ne İşe Yarar?** Durum tespiti yapılacak hedef hakkında hangi bilgilerin (sektör, aşama, sağlanan dokümanlar vb.) gerekli olduğunu tanımlar.

### 3. `[workflow]` (İş Akışı)
*   **Ne İşe Yarar?** Durum tespiti sürecini dokuz ana aşamaya ayırır:
    1.  **`intake_context`:** Sağlanan tüm bilgi ve belgelerin toplanması, eksiklerin tespit edilmesi.
    2.  **`market_analysis`:** Pazarın büyüklüğü, rekabet durumu ve iş modelinin analizi.
    3.  **`technical_review`:** Ürünün veya teknolojinin mimarisinin, kod kalitesinin ve ölçeklenebilirliğinin incelenmesi.
    4.  **`team_evaluation`:** Kurucu ve anahtar ekip üyelerinin deneyimlerinin, yeteneklerinin ve risklerinin değerlendirilmesi.
    5.  **`risk_redflag_id`:** Tüm alanlarda (yasal, finansal, teknik vb.) büyük risklerin ve "kırmızı bayrakların" (ciddi uyarı işaretleri) belirlenmesi.
    6.  **`compliance_checks`:** Hedefin yasal düzenlemelere, lisanslara ve sözleşmelere uygunluğunun denetlenmesi.
    7.  **`mitigation_planning`:** Tespit edilen riskler için azaltma ve çözüm planları önerilmesi.
    8.  **`recommendation`:** Tüm analiz sonucunda, "devam et", "etme" veya "şu koşullarla devam et" gibi net ve gerekçeli bir tavsiye sunulması.
    9.  **`audit_log`:** Süreç boyunca yapılan tüm analizlerin, değişikliklerin ve kararların kaydedilmesi.

### 4. `[tools]` (Araçlar)
*   **Ne İşe Yarar?** Bu süreçte kullanılabilecek `market_data_search` (pazar verisi arama), `code_review` (kod inceleme), `legal_flag_checker` (yasal risk kontrolü) gibi özel araçları tanımlar.

### 5. `[recursion]` (Özyineleme)
*   **Ne İşe Yarar?** Eğer inceleme sırasında kritik bir eksiklik veya risk bulunursa, sürecin belirli adımlarının tekrarlanmasını veya daha derin bir analiz için kendini yeniden tetiklemesini sağlayan bir mantık sunar.

### 6. `[examples]` (Örnekler)
*   **Ne İşe Yarar?** Her bir iş akışı aşamasının çıktısının (örneğin, bir risk matrisi, bir uyumluluk kontrol listesi) nasıl görünmesi gerektiğine dair somut örnekler sunar.

## Nasıl Kullanılır?

1.  İncelenecek hedef (şirket, proje vb.) hakkındaki tüm dokümanlar ve bilgiler toplanır.
2.  Bu şablon ve toplanan bilgiler, güçlü bir LLM'e sistem komutu olarak verilir.
3.  LLM, `/diligence.agent` rolünü benimseyerek, `[workflow]` adımlarını takip eder ve her adım için detaylı analizler, tablolar ve bulgular üretir.
4.  Süreç sonunda, hedefin yatırım yapılabilirliği, satın alınabilirliği veya ortaklık kurulabilirliği hakkında, tüm riskleri ve fırsatları içeren, veriye dayalı, kapsamlı bir durum tespiti raporu ortaya çıkar.

Bu şablon, karmaşık ve yüksek riskli kararlar almadan önce gereken derinlemesine araştırmayı otomatikleştirmek ve standartlaştırmak için tasarlanmış güçlü bir çerçevedir.