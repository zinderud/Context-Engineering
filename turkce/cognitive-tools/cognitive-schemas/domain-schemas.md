# Alan Şemaları: Bilgi Alanı Modelleme Mimarisi

Bu belge, bir yapay zeka sisteminin belirli bir **uzmanlık alanındaki** (örneğin, tıp, hukuk, mühendislik, sanat) bilgiyi derinlemesine anlaması, yapılandırması ve o alana özgü kurallarla akıl yürütmesi için tasarlanmış bir mimari ve araç seti sunar. Amaç, yapay zekayı genel bir bilgi deposu olmaktan çıkarıp, belirli bir alanda "uzman" gibi davranan bir varlığa dönüştürmektir.

## Temel Fikir: Her Bilgi Alanının Kendi Yapısı Vardır

Her uzmanlık alanının kendine özgü bir terminolojisi, kavramları, ilişkileri ve kuralları vardır. Bu mimari, bu yapıyı modellemek için tasarlanmıştır.

## Mimarinin Ana Bileşenleri

1.  **Kavram Modeli:**
    *   Bir alandaki temel "nesneleri" ve terminolojiyi tanımlar. Örneğin, yazılım mühendisliği için "sınıf", "fonksiyon", "tasarım deseni" gibi.

2.  **İlişki Modeli:**
    *   Bu kavramların birbirleriyle nasıl bir ilişki içinde olduğunu haritalar. Örneğin, "kalıtım" (inheritance) bir "sınıf" ile diğer bir "sınıf" arasındaki bir ilişkidir.

3.  **Kısıtlama Modeli:**
    *   Alanın "kurallarını" ve "yasalarını" tanımlar. Örneğin, fizikte "enerjinin korunumu yasası" bir kısıtlamadır. Bir çözüm bu kuralı ihlal edemez.

4.  **Doğrulama Modeli:**
    *   Üretilen bir çözümün veya bilginin, o alanın standartlarına ve kurallarına uygun olup olmadığını kontrol eder.

## Bilişsel Alan Araçları

Bu mimari, alan bilgisini işlemek için özel bilişsel araçlar sunar:

*   **Kavram Çıkarıcı (`concept_extractor`):** Bir metinden o alana özgü anahtar kavramları otomatik olarak çıkarır.
*   **İlişki Haritalayıcı (`relation_mapper`):** Bu kavramlar arasındaki (neden-sonuç, alt-üst, parça-bütün gibi) ilişkileri belirler.
*   **Kısıtlama Doğrulayıcı (`constraint_validator`):** Bir önerinin veya çözümün, alanın kurallarını (örneğin, bir mühendislik tasarımının güvenlik standartlarını) ihlal edip etmediğini kontrol eder.
*   **Alan Odaklı Akıl Yürütücü (`domain_reasoner`):** Problemleri, o alana özgü mantık ve çıkarım kurallarını kullanarak çözer.
*   **Disiplinlerarası Köprü (`cross_domain_bridge`):** Bir alandaki bir kavramı, başka bir ilgili alandaki bir kavrama benzeterek (analoji kurarak) bilgi transferi sağlar.

## Uygulama Örnekleri

Belge, **Yazılım Mühendisliği**, **Veri Bilimi**, **Fizik** ve **Pazarlama** gibi farklı alanlar için bu yapının nasıl somut şemalarla (JSON formatında) temsil edilebileceğini gösteren detaylı örnekler içerir.

## Sonuç

Alan Şemaları, yapay zekanın yüzeysel bilgi tekrarı yapmasının önüne geçerek, belirli bir konuda derinlemesine uzmanlık geliştirmesini sağlar. Bu, yapay zekanın daha doğru, güvenilir ve bağlama uygun çözümler üretmesi için temel bir gerekliliktir.
