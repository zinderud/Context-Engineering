# Şablon: Kontrol Döngüsü (Control Loop) - Türkçe Açıklama

Bu doküman, `20_templates/control_loop.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, LLM'lerle yapılan etkileşimleri yönetmek için genel amaçlı, modüler ve genişletilebilir bir **kontrol döngüsü şablonu** sunar.

## Şablonun Amacı

Tek seferlik LLM çağrıları basit görevler için yeterli olabilir, ancak karmaşık problemler genellikle çok adımlı bir süreç gerektirir. Bu şablon, bu tür karmaşık iş akışlarını yönetmek için bir iskelet sağlar. Bir görevi tamamlamak için LLM'in tekrar tekrar çağrıldığı, her adımda durumun (state) güncellendiği ve sonuçların değerlendirildiği bir yapı kurar.

Bu şablonun temel amacı, aşağıdaki gibi yeteneklere sahip sistemler kurmak için yeniden kullanılabilir bir temel sağlamaktır:

1.  **Çok Adımlı Akıl Yürütme:** Bir problemi daha küçük, yönetilebilir adımlara bölerek çözmek.
2.  **Durum Takibi:** Etkileşimler boyunca önemli bilgileri (hafıza, ara sonuçlar vb.) korumak ve bir sonraki adıma taşımak.
3.  **Dinamik Bağlam Yönetimi:** Her adımda LLM'e gönderilecek bağlamı, o anki duruma göre dinamik olarak oluşturmak.
4.  **Otomatik Değerlendirme ve İyileştirme:** LLM'in ürettiği çıktıları önceden tanımlanmış kriterlere göre otomatik olarak değerlendirmek ve gerekirse iyileştirme için döngüyü devam ettirmek.

## Şablonun Yapısı ve Ana Bileşenleri

Bu şablon, birkaç temel ve birbiriyle değiştirilebilir bileşenden oluşur:

### 1. `ModelInterface` (Model Arayüzü)
*   **Ne Yapar?** Farklı LLM sağlayıcıları (OpenAI, Anthropic vb.) ile iletişim kurmak için standart bir arayüz tanımlar. Bu, kodun geri kalanını değiştirmeden farklı bir LLM kullanmanıza olanak tanır.
*   **Örnekler:** `OpenAIInterface`, `AnthropicInterface`.

### 2. `ContextManager` (Bağlam Yöneticisi)
*   **Ne Yapar?** LLM'e gönderilecek olan bağlamı yönetir. Durumu (state) tutar, etkileşim geçmişini kaydeder ve bağlamın token limitini aşmasını önlemek için basit budama stratejileri uygular.
*   **Temel Yetenekleri:**
    *   `update(key, value)`: Bağlamdaki bir bilgiyi günceller.
    *   `get_context_str()`: Bağlamı, LLM'in anlayacağı bir metin formatına dönüştürür.
    *   `add_to_history()`: Bir etkileşimi geçmişe ekler.

### 3. `EvaluationFunction` (Değerlendirme Fonksiyonu)
*   **Ne Yapar?** LLM'in ürettiği bir cevabın kalitesini veya doğruluğunu ölçmek için bir standart tanımlar. Bu, sistemin kendi kendini denetlemesini sağlar.
*   **Örnekler:**
    *   **`SimpleKeywordEvaluator`:** Cevabın belirli anahtar kelimeleri içerip içermediğini kontrol eder.
    *   **`PatternMatchEvaluator`:** Cevabın belirli bir regex deseniyle eşleşip eşleşmediğini kontrol eder.
    *   **`ModelEvaluator`:** Bir cevabı değerlendirmek için başka bir LLM'i kullanır (örneğin, "Bu cevap soruyu ne kadar iyi yanıtlıyor?").

### 4. `ControlLoop` (Kontrol Döngüsü)
*   **Ne Yapar?** Tüm bu parçaları bir araya getiren ana orkestratördür. Belirlenen sayıda iterasyon boyunca çalışır, her adımda:
    1.  `ContextManager`'dan güncel bağlamı alır.
    2.  `ModelInterface` aracılığıyla LLM'i çağırır.
    3.  Gelen cevabı `EvaluationFunction`'lar ile değerlendirir.
    4.  Değerlendirme sonucuna göre döngüye devam edip etmeyeceğine veya duracağına karar verir.

### 5. `NeuralField` Uzantıları (İleri Seviye)
*   Şablon ayrıca, bağlamı ayrık metinler yerine sürekli bir "alan" olarak ele alan `NeuralField` ve `NeuralFieldControlLoop` gibi daha gelişmiş ve teorik sınıflar da içerir. Bu, projenin ileri seviye kavramlarını denemek için bir başlangıç noktası sunar.

## Nasıl Kullanılır?

Bu şablonu kendi projenizde kullanmak için:

1.  Kullanmak istediğiniz LLM için bir `ModelInterface` seçin (veya kendinizinkini oluşturun).
2.  Görevinizin gerektirdiği başlangıç bilgilerini içeren bir `initial_context` tanımlayın.
3.  LLM'in çıktılarını nasıl değerlendireceğinizi belirleyen bir veya daha fazla `EvaluationFunction` oluşturun.
4.  Bu bileşenleri bir `ControlLoop` nesnesi içinde birleştirin.
5.  `run(input_data)` metodunu çağırarak döngüyü başlatın.

Bu şablon, basit bir soru-cevap botundan, karmaşık bir araştırma ajanına kadar birçok farklı uygulamayı hayata geçirmek için sağlam ve esnek bir temel sunar.