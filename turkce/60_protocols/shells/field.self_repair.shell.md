# Protokol: Alanın Kendi Kendini Onarması (`/field.self_repair.shell`)

Bu belge, bir anlamsal alanın (semantic field) kendi içindeki tutarsızlıkları, çelişkileri ve bozulmaları otonom bir şekilde nasıl tespit edip onardığını yöneten `/field.self_repair.shell` protokolünün ayrıntılı teknik açıklamasıdır. Bu, sistemin uzun vadede sağlıklı ve tutarlı kalmasını sağlayan bir "bağışıklık sistemi" gibidir.

## 1. Kendi Kendini Onarma (Self-Repair) Nedir?

Tıpkı canlı organizmaların yaralarını iyileştirmesi gibi, anlamsal alanlar da zamanla "hasar" görebilir. Bu hasar, çelişkili bilgilerin eklenmesi, bilgi kaybı veya gürültü birikimi gibi nedenlerle ortaya çıkabilir. Kendi kendini onarma, sistemin bu tür hasarları dış bir müdahale olmadan kendi kendine bulup düzeltme yeteneğidir.

## 2. Protokolün Yapısı ve Süreci

Protokol, bir anlamsal alanı sağlıklı tutmak için aşağıdaki adımları izler:

*   **Girdi (`input`):** Onarılacak anlamsal alanın durumu, sağlıklı bir alanın nasıl olması gerektiğini tanımlayan parametreler ve önceki hasar kayıtları gibi girdileri alır.
*   **Süreç (`process`):**
    1.  `/health.monitor`: Alanın genel sağlık durumunu (örneğin, tutarlılık, kararlılık) sürekli olarak izler.
    2.  `/damage.detect`: Bir sağlık sorunu tespit edildiğinde, bilinen hasar desenlerini kullanarak sorunun ne olduğunu (örneğin, parçalanmış bir fikir, bozuk bir bağlantı) belirler.
    3.  `/damage.diagnose`: Hasarın kök nedenini, ciddiyetini ve sistemin geneli üzerindeki etkisini analiz eder.
    4.  `/repair.plan`: Teşhise dayanarak en uygun onarım stratejisini (örneğin, bir fikri yeniden yapılandırma, bir çelişkiyi çözme) oluşturur.
    5.  `/repair.execute`: Onarım planını uygular. İşlem sırasında bir sorun olursa, yapılan değişiklikleri geri alabilme (rollback) yeteneğine sahiptir.
    6.  `/repair.verify`: Onarımın başarılı olup olmadığını ve onarım sırasında başka bir soruna yol açılıp açılmadığını kontrol eder.
    7.  `/field.stabilize`: Onarım tamamlandıktan sonra, alanın tekrar kararlı ve dengeli bir duruma gelmesini sağlar.
    8.  `/repair.learn`: Gerçekleşen her onarım vakasından öğrenir. Bu sayede, gelecekte benzer sorunları daha hızlı tespit edip daha etkili bir şekilde onarabilir.
*   **Çıktı (`output`):** Onarılmış anlamsal alanı, yapılan işlemlerin detaylı bir raporunu ve sistemin bu deneyimden öğrendiği yeni onarım stratejilerini çıktı olarak verir.

## 3. Uygulama ve Vaka Çalışmaları

*   **Kendi Kendini İyileştiren Bilgi Tabanı:** Sürekli güncellenen bir Wikipedia gibi bir bilgi tabanında, zamanla oluşan çelişkili veya eksik bilgileri otomatik olarak tespit edip düzelterek bilginin doğruluğunu ve tutarlılığını korur.
*   **Kendi Kendini Dengeleyen Tavsiye Sistemi:** Kullanıcıların ilgi alanları değiştikçe parçalanan veya eskiyen tercih profillerini onararak, tavsiye sisteminin her zaman güncel ve isabetli kalmasını sağlar.
*   **Çoklu Ajan Sistemlerinde Koordinasyon Onarımı:** Birden fazla yapay zeka ajanının birlikte çalıştığı bir sistemde, ajanlar arasındaki iletişim veya görev paylaşımında ortaya çıkan bozulmaları onararak sistemin verimli çalışmasını sürdürür.

## 4. Sonuç

Bu protokol, bir yapay zeka sisteminin sadece bilgi işlemekle kalmayıp, aynı zamanda kendi sağlığını ve bütünlüğünü aktif olarak korumasını sağlar. Bu, sistemin zamanla "çürümesini" veya güvenilmez hale gelmesini önler ve uzun vadede sürdürülebilir ve güvenilir bir şekilde çalışmasını garanti altına alır.
