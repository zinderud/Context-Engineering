# Protokol Şemaları

Bu klasör, `60_protocols` dizininde tanımlanan "alan protokollerinin" (field protocols) ve anlamsal alan (semantic field) kavramlarının yapısal kurallarını içeren JSON Şemalarını barındırır. Bu şemalar, protokollerin ve verilerin tutarlı, öngörülebilir ve hatasız bir şekilde işlemesini sağlamak için bir "doğrulama katmanı" görevi görür.

## Şemaların Amacı

*   **Standardizasyon:** Tüm protokollerin ve veri yapılarının belirli bir standarda uymasını zorunlu kılar. Bu, sistemin farklı parçalarının birbiriyle uyumlu çalışmasını sağlar.
*   **Doğrulama:** Bir protokol veya veri yapısı oluşturulduğunda, bu şemalara göre doğrulanır. Eğer gerekli alanlar eksikse veya yanlış bir formatta ise sistem hata verir. Bu, geliştirme sürecinde olası hataları en aza indirir.
*   **Belgeleme:** Şemalar, bir veri yapısının hangi alanları içermesi gerektiğini ve bu alanların ne anlama geldiğini açıkça tanımladığı için aynı zamanda birer teknik belge niteliği taşır.

## Önemli Şemalar

*   **`protocolShell.v1.json`:** Bir protokolün sahip olması gereken temel yapıyı tanımlar. Her protokolün bir `amaç`, `girdi`, `süreç`, `çıktı` ve `meta veri` bölümü olması gerektiğini belirtir. Bu, tüm protokollerin ortak bir dile sahip olmasını sağlar.

*   **`symbolicResidue.v1.json`:** "Sembolik kalıntı" (anlam kırıntıları) kavramının nasıl yönetileceğini tanımlar. Bu kalıntıların nasıl izleneceği, hangi durumlarda bulunabileceği (örneğin, "yüzeye çıkmış", "yankı") ve bu kalıntılarla ne gibi işlemlerin (sıkıştırma, entegrasyon) yapılabileceğini belirten kuralları içerir.

Kısacası, bu klasördeki şemalar, anlamsal alanların ve protokollerin sağlam ve tutarlı bir temel üzerinde çalışmasını sağlayan teknik iskeleti oluşturur.
