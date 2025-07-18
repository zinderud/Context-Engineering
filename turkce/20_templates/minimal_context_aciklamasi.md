# Şablon: Minimal Bağlam (Minimal Context) - Türkçe Açıklama

Bu doküman, `20_templates/minimal_context.yaml` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu YAML dosyası, bir LLM (Büyük Dil Modeli) ile etkileşim kurmak için gereken temel bağlam bileşenlerini tanımlayan, yeniden kullanılabilir ve yapılandırılmış bir **başlangıç şablonudur**.

## Şablonun Amacı

Bir LLM'e komut gönderirken, sadece o anki soruyu değil, aynı zamanda modelin kim olacağını, hangi kurallara uyması gerektiğini, geçmiş konuşmaları ve hatta örnek cevapları da içeren bir bağlam sunmak, çok daha kaliteli ve tutarlı sonuçlar üretir. Bu YAML şablonu, bu bağlamı oluşturan tüm bu parçaları organize etmek için standart bir yapı sunar.

Bu şablonun temel amacı, yeni bir LLM projesine başlarken sıfırdan bir bağlam yapısı düşünmek yerine, doğrudan kullanılabilecek veya projenin ihtiyacına göre kolayca özelleştirilebilecek sağlam bir temel sağlamaktır.

## Şablonun Yapısı ve Ana Bileşenleri

YAML dosyası, bir bağlamın farklı yönlerini tanımlayan birkaç ana bölümden oluşur:

### 1. `metadata` (Üst Veri)
*   **Ne İşe Yarar?** Şablonun kendisi hakkında bilgi verir.
*   **Alanlar:**
    *   `version`: Şablonun sürüm numarası.
    *   `description`: Şablonun ne işe yaradığının kısa bir açıklaması.
    *   `author`: Şablonu oluşturan kişi veya grup.
    *   `token_budget`: Bu bağlamın hedeflenen maksimum token sayısı. Bu, maliyet ve performans kontrolü için önemlidir.

### 2. `system` (Sistem Talimatları)
*   **Ne İşe Yarar?** LLM'in temel kimliğini ve davranış kurallarını belirler. Bu, tüm etkileşim boyunca sabit kalır.
*   **Alanlar:**
    *   `role`: Modelin benimsemesi gereken rol (örneğin, "yardımcı asistan", "matematik öğretmeni").
    *   `capabilities`: Modelin neler yapabileceği (örneğin, "soru cevaplama", "kod yazma").
    *   `constraints`: Modelin uyması gereken kısıtlamalar (örneğin, "doğru bilgi ver", "gereksiz uzun konuşma").

### 3. `memory` (Hafıza)
*   **Ne İşe Yarar?** Konuşma geçmişini yönetir, böylece model önceki konuşmaları "hatırlayabilir".
*   **Alanlar:**
    *   `enabled`: Hafıza özelliğinin açık olup olmadığını belirtir.
    *   `max_turns`: Kaç adet geçmiş konuşmanın (kullanıcı-asistan diyaloğu) bağlama ekleneceğini belirler.
    *   `pruning_strategy`: Konuşma geçmişi token bütçesini aştığında hangi stratejinin uygulanacağını belirtir (örneğin, `drop_oldest` - en eski konuşmayı sil).

### 4. `examples` (Az Sayıda Örnek - Few-Shot)
*   **Ne İşe Yarar?** Modele, istediğiniz cevap stilini veya formatını göstermek için birkaç örnek soru-cevap çifti sunar.
*   **Alanlar:**
    *   `enabled`: Örneklerin bağlama eklenip eklenmeyeceğini belirtir.
    *   `exchanges`: Örnek diyalogları içerir.

### 5. `evaluation` (Değerlendirme)
*   **Ne İşe Yarar?** Modelin ürettiği cevapların kalitesini ölçmek için kullanılacak metrikleri tanımlar. Bu bölüm programatik olarak kullanılmak üzere bir rehber niteliğindedir.
*   **Alanlar:**
    *   `metrics`: `relevance` (ilgililik), `conciseness` (özlülük), `accuracy` (doğruluk) gibi ölçülecek kalite kriterlerini listeler.

### 6. `token_management` (Token Yönetimi)
*   **Ne İşe Yarar?** Bağlamın, belirlenen `token_budget`'ı aşmasını önlemek için uygulanacak stratejileri tanımlar.
*   **Alanlar:**
    *   `reduction_strategies`: Token sayısını azaltmak için yapılacaklar listesi (örneğin, "en eski konuşmaları sil").
    *   `priority`: Token bütçesi dolduğunda, hangi bağlam parçasının daha önemli olduğunu ve hangisinin önce silinebileceğini belirten bir öncelik sırası.

### 7. `assembly` (Birleştirme)
*   **Ne İşe Yarar?** Yukarıdaki tüm parçaların hangi sırayla birleştirilerek nihai komutu (prompt) oluşturacağını tanımlar.
*   **Alanlar:**
    *   `order`: `system`, `examples`, `memory` gibi bileşenlerin sıralaması.
    *   `template`: Tüm bu parçaları bir araya getiren nihai komut şablonu.

## Nasıl Kullanılır?

Bu YAML dosyası doğrudan çalıştırılmaz. Bunun yerine, bir Python betiği içinden okunur ve bir LLM çağrısı yapmadan önce bağlamı dinamik olarak oluşturmak için kullanılır:

1.  Python kodunuzda `PyYAML` kütüphanesini kullanarak bu dosyayı yükleyin.
2.  Projenizin ihtiyacına göre şablondaki değerleri (örneğin, `role` veya `token_budget`) güncelleyin.
3.  `assembly` bölümündeki şablonu kullanarak, o anki kullanıcı sorusu, konuşma geçmişi ve diğer bileşenlerle birlikte nihai komutu oluşturun.
4.  Oluşturulan bu tam bağlamı LLM'e gönderin.

Bu şablon, LLM etkileşimlerinizi daha yapılandırılmış, yönetilebilir ve tutarlı hale getirmek için mükemmel bir başlangıç noktasıdır.
