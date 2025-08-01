# Ajan Şemaları: Çoklu Ajan Koordinasyon Mimarisi

Bu belge, birden fazla otonom yapay zeka "ajanının" tek bir hedef doğrultusunda **birlikte ve koordine bir şekilde** çalışmasını sağlayan bir mimari ve şema seti sunar. Amaç, tek bir ajanın yeteneklerini aşan karmaşık ve çok yönlü görevleri, bir "uzmanlar takımı" gibi çalışan ajanlarla çözmektir.

## Temel Fikir: İş Bölümü ve Koordinasyon

Tıpkı bir şirketteki farklı departmanlar gibi, bu mimaride de her ajanın bir uzmanlık alanı vardır. Mimari, doğru görevin doğru ajana verilmesini, ajanların birbiriyle uyumlu çalışmasını ve genel sürecin verimli bir şekilde yönetilmesini sağlar.

## Mimarinin Ana Bileşenleri

1.  **Delegasyon Modeli:**
    *   Büyük bir görevi analiz eder, onu daha küçük alt görevlere ayırır ve her bir alt görevi en uygun ajana atar.

2.  **Ajan Seçici:**
    *   Mevcut "ajan havuzundan", bir görevin gerektirdiği yeteneklere, performansa ve uygunluk durumuna göre en iyi ajanları veya ajan ekibini seçer.

3.  **İzleme Modeli:**
    *   Tüm ajanların performansını (hız, kalite, verimlilik) ve sistemin genel sağlığını sürekli olarak izler. Bir sorun olduğunda uyarı verir.

4.  **Ölçeklendirme Modeli:**
    *   İş yükü arttığında sisteme otomatik olarak yeni ajanlar ekler veya iş yükü azaldığında gereksiz ajanları devreden çıkararak kaynakları verimli kullanır.

## Ajan Koordinasyon Araçları ve Protokolleri

Bu mimari, ajanların uyum içinde çalışmasını sağlamak için bir dizi araç ve protokol içerir:

*   **Delegasyon Aracı:** Görevleri analiz edip en uygun ajanlara atayan mekanizma.
*   **Koordinasyon Protokolü:** Ajanların birbirleriyle nasıl iletişim kuracağını, ne zaman bilgi alışverişinde bulunacağını ve hangi sırayla çalışacağını belirleyen kurallar dizisi.
*   **Çatışma Çözümü Protokolü:** İki ajan aynı kaynağı kullanmak istediğinde veya görev öncelikleri çakıştığında devreye girerek sorunu çözen mekanizma.

## Şema Örnekleri

Belge, bir ajanın yeteneklerini (`"beceriler": ["araştırma", "analiz"]`), uygunluk durumunu (`"durum": "müsait"`) ve iletişim tercihlerini tanımlayan standart **Ajan Tanım Şeması** gibi somut JSON şema örnekleri sunar.

## Sonuç

Ajan Şemaları, tek bir büyük yapay zeka modeli yerine, her biri kendi alanında uzmanlaşmış daha küçük ve verimli ajanlardan oluşan esnek, ölçeklenebilir ve güçlü sistemler kurmanın temelini oluşturur. Bu, yapay zekanın daha karmaşık ve dinamik problemleri işbirliği içinde çözmesini sağlar.
