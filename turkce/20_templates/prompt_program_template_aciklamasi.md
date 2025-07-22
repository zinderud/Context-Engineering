# Şablon: Prompt Programı (Prompt Program) - Türkçe Açıklama

Bu doküman, `20_templates/prompt_program_template.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, LLM'lerle etkileşimi, tıpkı bir bilgisayar programı gibi yapılandırılmış adımlarla, koşullarla ve döngülerle yönetmek için genel amaçlı bir **programlama şablonu** sunar.

## Şablonun Amacı

Bu şablon, "Prompt Mühendisliği"ni, "Prompt Programlama"ya dönüştürme fikrini temel alır. Amaç, LLM'e sadece ne yapacağını söylemek değil, aynı zamanda görevi **nasıl** yapacağını da adım adım, mantıksal bir akış içinde tarif etmektir. Bu, LLM'in akıl yürütme sürecini daha öngörülebilir, kontrol edilebilir ve güçlü hale getirir.

Bu şablon, aşağıdaki gibi programlama konseptlerini doğal dil komutlarıyla birleştiren bir yapı kurar:

1.  **Modüler Adımlar:** Bir programı, her biri belirli bir görevi olan küçük, yeniden kullanılabilir adımlara bölmek.
2.  **Kontrol Akışı:** `IF-ELSE` gibi koşullu ifadelerle veya `FOR` gibi döngülerle programın akışını yönlendirmek.
3.  **Değişken Yönetimi:** Program içinde bilgiyi depolamak ve adımlar arasında aktarmak için değişkenler kullanmak.
4.  **Hata Yönetimi:** Programın çalışması sırasında bir hata oluşursa ne yapılacağını belirleyen kurallar tanımlamak.
5.  **İleri Seviye Entegrasyon:** Programın durumunu, projenin ileri seviye kavramları olan "Nöral Alanlar" ve "Protokol Kabukları" ile entegre etmek.

## Şablonun Yapısı ve Ana Bileşenleri

### 1. `ProgramStep` (Program Adımı)
*   **Ne Yapar?** Bir programın en temel yapı taşıdır. Tek bir talimatı, bir koşulu, bir döngüyü veya bir değişken atamasını temsil eder.
*   **Türleri (`StepType`):**
    *   `INSTRUCTION`: Basit bir talimat.
    *   `CONDITION`: Bir `IF` koşulu.
    *   `LOOP`: Bir `FOR` döngüsü.
    *   `VARIABLE`: Değişken ataması (`SET x = ...`).
    *   `FUNCTION`: Harici bir fonksiyon çağrısı.
    *   `ERROR`: Hata durumunda ne yapılacağı.

### 2. `PromptProgram` (Prompt Programı - Ana Sınıf)
*   **Ne Yapar?** `ProgramStep`'lerden oluşan bir listeyi yöneten ve çalıştıran ana sınıftır.
*   **Temel Yetenekleri:**
    *   `add_step`, `add_condition`, `add_loop` gibi metotlarla programı adım adım oluşturur.
    *   `format()`: Oluşturulan programı, LLM'in anlayabileceği, numaralandırılmış bir metin formatına dönüştürür.
    *   `execute(input)`: Programı, verilen bir girdiyle çalıştırmak için LLM'e gönderilecek nihai komutu oluşturur ve LLM'i çağırır.

### 3. `NeuralFieldProgram` (Nöral Alan Programı)
*   **Ne Yapar?** Standart `PromptProgram`'ı, "Nöral Alan" konseptiyle birleştirir. Programın durumu ve adımları, alan içinde yankılanan ve birbirini etkileyen desenler olarak ele alınır.
*   **Ek Yetenekleri:**
    *   `add_attractor()`: Alana, programın düşünce sürecini yönlendirecek ana fikirler (çekiciler) ekler.
    *   `add_resonance_step()`: Belirli fikirlerle rezonansa girmesi (onları dikkate alması) için özel adımlar ekler.

### 4. `ProtocolShellProgram` (Protokol Kabuğu Programı)
*   **Ne Yapar?** `field_protocol_shells.py` şablonunda tanımlanan yüksek seviyeli protokolleri, çalıştırılabilir bir `PromptProgram`'a dönüştürür.
*   **İşleyişi:** Bir protokol tanımını alır ve `process` bölümündeki her bir adımı otomatik olarak bir `ProgramStep`'e çevirir.

## Nasıl Kullanılır?

Bu şablon, bir görevi basit bir komutla ifade etmek yerine, onu bir algoritma gibi tasarlamak istediğinizde kullanılır:

1.  Bir `PromptProgram` nesnesi oluşturun.
2.  Görevinizi tamamlamak için gereken mantıksal adımları `add_step`, `add_condition` gibi metotlarla programa ekleyin.
3.  İsteğe bağlı olarak, programın durumunu daha akışkan bir şekilde yönetmek için bir `NeuralField` entegre edin.
4.  `execute(input)` metodunu çağırarak, LLM'in bu programı adım adım çalıştırmasını ve nihai sonucu üretmesini sağlayın.

Bu şablon, LLM'lerle etkileşimi, basit talimatlar vermekten, karmaşık ve yapılandırılmış **bilişsel algoritmalar** tasarlamaya doğru bir geçişi temsil eder.
