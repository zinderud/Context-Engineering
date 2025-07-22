# Prompt Şablonu: Deney Ajanı (Experiment Agent) - Türkçe Açıklama

Bu doküman, `20_templates/PROMPTS/experiment.agent.md` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu dosya, bilimsel bir deneyi sıfırdan tasarlamak, planlamak ve protokolünü oluşturmakla görevli bir `/experiment.agent` rolünü tanımlayan, bütüncül bir sistem komutudur.

## Şablonun Amacı

İyi bir bilimsel deney, dikkatli bir planlama, net hipotezler, kontrol edilen değişkenler ve tekrarlanabilir prosedürler gerektirir. Bu şablon, bu karmaşık deney tasarım sürecini, yapay zekayı kullanarak sistematik, denetlenebilir ve şeffaf bir hale getirmeyi amaçlar. Ajanın görevi, bir araştırma sorusunu, baştan sona uygulanmaya hazır, eksiksiz bir deney protokolüne dönüştürmektir.

Bu şablon, aşağıdaki gibi alanlar ve durumlar için idealdir:

*   Bir biyoloji veya kimya laboratuvarında yeni bir deney tasarlamak.
*   Bir yazılımın kullanıcı deneyimini (UX) test etmek için bir A/B testi planlamak.
*   Sosyal bilimlerde bir anket veya saha çalışması protokolü oluşturmak.
*   Bir makine öğrenmesi modelinin performansını değerlendirmek için bir simülasyon deneyi kurmak.

## Şablonun Yapısı ve Ana Bileşenleri

Bu sistem komutu, bir deney tasarım sürecinin tüm aşamalarını kapsayan modüler bir yapıya sahiptir:

### 1. `[instructions]` (Talimatlar)
*   **Ne İşe Yarar?** AI ajanına, `/experiment.agent` rolünü ve temel davranış kurallarını atar. Ajana, bilimsel metodolojiye sadık kalması, varsayımlarını belirtmesi ve süreci adım adım takip etmesi talimatını verir.

### 2. `[context_schema]` (Bağlam Şeması)
*   **Ne İşe Yarar?** Deney hakkında hangi temel bilgilerin (alanı, amacı, kısıtlamaları vb.) sağlanması gerektiğini tanımlar.

### 3. `[workflow]` (İş Akışı)
*   **Ne İşe Yarar?** Deney tasarım sürecini dokuz ana aşamaya ayırır:
    1.  **`context_framing`:** Deneyin amacını, arka planını ve kısıtlamalarını netleştirme.
    2.  **`hypothesis_spec`:** Test edilecek ana hipotezi (ve sıfır hipotezini) açıkça formüle etme.
    3.  **`variable_selection`:** Bağımlı, bağımsız ve kontrol edilecek değişkenleri tanımlama.
    4.  **`method_protocol_design`:** Deneyin adım adım nasıl yapılacağını, hangi araçların kullanılacağını ve verilerin nasıl toplanacağını tasarlama.
    5.  **`control_group_setup`:** Deney ve kontrol gruplarının nasıl oluşturulacağını ve yönetileceğini planlama (örneğin, rastgele atama, çift körleme).
    6.  **`outcome_modeling`:** Beklenen sonuçların ne olduğunu, verilerin nasıl analiz edileceğini ve başarının ne anlama geleceğini modelleme.
    7.  **`audit_checklist`:** Tasarımın tekrarlanabilirlik, yanlılık ve etik kurallar gibi standartlara uygunluğunu kontrol etme.
    8.  **`recursive_refinement`:** Denetim veya geri bildirimler sonucunda tasarımda iyileştirmeler yapma.
    9.  **`final_protocol_output`:** Tüm adımları içeren, uygulanmaya hazır nihai deney protokolünü oluşturma.

### 4. `[tools]` (Araçlar)
*   **Ne İşe Yarar?** Bu süreçte kullanılabilecek `hypothesis_generator` (hipotez üretici), `protocol_designer` (protokol tasarımcısı) gibi özel araçları tanımlar.

### 5. `[recursion]` (Özyineleme)
*   **Ne İşe Yarar?** Denetim listesinde (audit) bir eksiklik bulunduğunda, tasarımın ilgili aşamasına geri dönülerek iyileştirme yapılmasını sağlayan bir geri bildirim döngüsü mantığı sunar.

### 6. `[examples]` (Örnekler)
*   **Ne İşe Yarar?** Her bir iş akışı aşamasının çıktısının (örneğin, bir değişken tablosu, bir kontrol grubu planı) nasıl görünmesi gerektiğine dair somut bir örnek sunar.

## Nasıl Kullanılır?

1.  Bir araştırma fikri veya sorusu, `[context_schema]`'ya uygun olarak temel bilgilerle birlikte hazırlanır.
2.  Bu şablon ve hazırlanan bağlam, güçlü bir LLM'e sistem komutu olarak verilir.
3.  LLM, `/experiment.agent` rolünü benimseyerek, `[workflow]` adımlarını takip eder ve her adım için detaylı çıktılar (hipotezler, prosedürler, tablolar, kontrol listeleri) üretir.
4.  Süreç sonunda, bilimsel olarak sağlam, tekrarlanabilir ve denetlenmiş, uygulanmaya hazır eksiksiz bir deney tasarım protokolü ortaya çıkar.

Bu şablon, bilimsel araştırma sürecini daha titiz, yapılandırılmış ve verimli hale getirmek için tasarlanmış güçlü bir çerçevedir.