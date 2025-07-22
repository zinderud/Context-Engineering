# Prompt Şablonu: Uyumluluk Ajanı (Alignment Agent) - Türkçe Açıklama

Bu doküman, `20_templates/PROMPTS/alignment.agent.md` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu dosya, basit bir komut olmaktan öte, bir yapay zeka (AI) sisteminin veya ajanının **güvenlik ve uyumluluk denetimini** baştan sona yönetmek için tasarlanmış, bütüncül bir **sistem komutudur (system prompt)**.

## Şablonun Amacı

Bu şablonun temel amacı, bir AI ajanına "uyumluluk denetçisi" rolünü vermektir. Bu denetçi ajan, kendisine sağlanan bir AI sistemi hakkındaki bilgileri (kodu, dokümanları, konfigürasyonları vb.) analiz ederek, potansiyel riskleri, güvenlik açıklarını ve insan değerleriyle uyumsuzlukları sistematik bir şekilde ortaya çıkarmakla görevlidir. Bu süreç, genellikle "Red Teaming" (kötü niyetli bir saldırgan gibi düşünerek sistemin zayıflıklarını bulma) olarak adlandırılır.

Şablon, bu denetim sürecini standartlaştırmak, şeffaf hale getirmek ve denetim sonunda somut, eyleme geçirilebilir öneriler sunmak için yapılandırılmıştır.

## Şablonun Yapısı ve Ana Bileşenleri

Bu sistem komutu, bir denetim sürecinin tüm aşamalarını kapsayan modüler bir yapıya sahiptir:

### 1. `[meta]` (Üst Veri)
*   **Ne İşe Yarar?** Bu denetim protokolünün sürümünü, hedeflenen AI modellerini ve amacını tanımlar.

### 2. `[instructions]` (Talimatlar)
*   **Ne İşe Yarar?** AI ajanına, `/alignment.agent` rolünü ve temel davranış kurallarını atar. Ajana, adım adım ilerlemesi, kanıta dayalı bulgular sunması ve belirsizlikleri raporlaması talimatını verir.

### 3. `[ascii_diagrams]` (ASCII Diyagramları)
*   **Ne İşe Yarar?** Denetim sürecinin iş akışını ve dosya yapısını görsel olarak basitçe şematize eder.

### 4. `[context_schema]` (Bağlam Şeması)
*   **Ne İşe Yarar?** Denetlenecek AI sistemi hakkında hangi bilgilerin (sistemin amacı, mimarisi, otonomi seviyesi vb.) sağlanması gerektiğini tanımlayan bir JSON şeması sunar.

### 5. `[workflow]` (İş Akışı)
*   **Ne İşe Yarar?** Denetim sürecinin hangi aşamalardan oluşacağını tanımlar. Bu, şablonun kalbidir.
*   **Aşamalar:**
    1.  **`clarify_context`:** Eksik bilgileri anlama ve netleştirme.
    2.  **`threat_modeling`:** Potansiyel tehditleri ve saldırı senaryolarını modelleme.
    3.  **`risk_failure_id`:** Olası riskleri ve başarısızlık modlarını tanımlama.
    4.  **`adversarial_testing`:** Kötü niyetli senaryolarla sistemi test etme.
    5.  **`failsafe_monitoring`:** Güvenlik önlemlerini ve izleme sistemlerini denetleme.
    6.  **`mitigation_planning`:** Bulunan riskler için azaltma planları önerme.
    7.  **`recommendation`:** Sistemin dağıtıma çıkıp çıkamayacağına dair gerekçeli bir tavsiye sunma.
    8.  **`audit_reflection`:** Tüm süreci gözden geçirme ve belgeleme.

### 6. `[tools]` (Araçlar)
*   **Ne İşe Yarar?** Denetim sırasında kullanılabilecek harici (örneğin, güvenlik açığı veritabanı) veya dahili (örneğin, düşünce zinciri analizi) araçları tanımlar.

### 7. `[recursion]` (Özyineleme)
*   **Ne İşe Yarar?** Denetim sürecinin kendi kendini nasıl iyileştirebileceğini tanımlayan bir Python benzeri psödokod sunar. Eğer denetim sonuçları yetersizse, sürecin daha derin bir analiz için kendini tekrar başlatabileceği bir mantık içerir.

### 8. `[examples]` (Örnekler)
*   **Ne İşe Yarar?** Her bir iş akışı aşamasının çıktısının nasıl görünmesi gerektiğine dair somut örnekler (Markdown tabloları, listeler vb.) sunar.

## Nasıl Kullanılır?

Bu şablon, bir AI sistemini (örneğin, yeni bir chatbot, bir otomasyon ajanı) canlıya almadan önce onun güvenliğinden ve uyumluluğundan emin olmak için kullanılır:

1.  Denetlenecek AI sistemi hakkındaki bilgiler, `[context_schema]` bölümünde belirtilen formata göre hazırlanır.
2.  Bu şablon, hazırlanan bu bağlam bilgisiyle birlikte güçlü bir LLM'e (örneğin, GPT-4o) sistem komutu olarak verilir.
3.  LLM, `/alignment.agent` rolünü benimseyerek, `[workflow]` bölümünde tanımlanan adımları sırayla takip eder.
4.  Her adımda, `[examples]` bölümündeki formatlara benzer, denetimle ilgili bulgularını, tablolarını ve analizlerini üretir.
5.  Süreç sonunda, AI sisteminin güvenliği hakkında kapsamlı bir rapor ve eyleme geçirilebilir öneriler sunar.

Bu şablon, AI güvenliği ve uyumluluğu gibi son derece karmaşık bir konuyu, yapılandırılmış, denetlenebilir ve sistematik bir sürece dönüştürmek için güçlü bir araçtır.