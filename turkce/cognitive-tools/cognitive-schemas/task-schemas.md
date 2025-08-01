# Görev Şemaları: Akıl Yürütme Görev Mimarisi

Bu belge, bir yapay zeka sisteminin belirli bir **görevi** (örneğin, bir problemi çözme, bir metni analiz etme, yeni bir fikir sentezleme) nasıl yapılandırılmış bir şekilde ele alacağını tanımlayan bir mimari ve şema seti sunar. Amaç, her türlü akıl yürütme görevi için standart, yeniden kullanılabilir ve etkili bir iş akışı oluşturmaktır.

## Temel Fikir: Her Görevin Bir Yapısı Vardır

Bu mimari, her görevin bir tanımı, hedefleri, kısıtlamaları ve çözüm için bir dizi adımı olduğunu varsayar. Görev şemaları, bu yapıyı standart bir formatta tanımlar. Bu, yapay zekanın bir görevi ele alırken "ne yapacağını" ve "nasıl yapacağını" net bir şekilde bilmesini sağlar.

## Mimarinin Ana Bileşenleri

Bu mimari, bir görevi işlemek için daha önce bahsedilen tüm ileri düzey kavramları bir araya getirir:

1.  **Bilişsel Araçlar Orkestrasyonu:** Görevin her aşamasında (anlama, analiz, çözüm, doğrulama) hangi bilişsel aracın kullanılacağını planlar ve yönetir.
2.  **Üç Aşamalı Sembolik İşleme:** Görevi, soyut sembolik değişkenlere dönüştürerek (örneğin, bir matematik problemini formüllere dökerek) temel mantığını anlar ve çözer.
3.  **Kuantum Semantik Yorumlama:** Görevin tanımındaki belirsizlikleri veya farklı yorumlanabilecek noktaları (örneğin, "piyasayı iyileştir" gibi bir görevde "iyileştirmenin" ne anlama geldiğini) farklı bakış açılarına göre değerlendirir.
4.  **Hafıza-Akıl Yürütme Sinerjisi:** Görevi çözerken, sistemin hafızasındaki ilgili bilgi ve deneyimleri (örneğin, daha önce çözülmüş benzer problemler) en verimli şekilde kullanmasını sağlar.

## Aşamalı Karmaşıklık ve Görevler

Bu mimari, görevleri farklı karmaşıklık seviyelerinde ele alabilir:

*   **Atomik Görevler:** Tek bir adımdan oluşan basit görevler (örneğin, "iki sayıyı topla").
*   **Moleküler Görevler:** Birkaç adımdan oluşan sıralı görevler (örneğin, "verileri topla, ortalamasını al ve raporla").
*   **Hücresel Görevler:** Bağlam ve hafıza gerektiren görevler (örneğin, "dünkü konuşmamıza göre, bana bir özet çıkar").
*   **Organ Görevleri:** Belirli bir uzmanlık alanı gerektiren görevler (örneğin, "bu C# kodundaki hatayı ayıkla").
*   **Nöral Sistem Görevleri:** Birden fazla aracın ve stratejinin koordine edildiği karmaşık görevler.
*   **Nöral Alan Görevleri:** Çözümün net olmadığı, yaratıcılık ve "ortaya çıkma" (emergence) gerektiren en karmaşık görevler.

## Görev Şablonları

Belge, "Problem Çözme", "Analiz" ve "Sentez" gibi yaygın görev türleri için JSON formatında somut şema örnekleri sunar. Bu şemalar, bir görevin tanımını, hedeflerini, kısıtlamalarını ve çözüm sürecini standart bir şekilde tanımlamak için kullanılır.

## Sonuç

Görev Şemaları, yapay zekanın görevleri rastgele veya tutarsız bir şekilde değil, sistematik, planlı ve verimli bir şekilde ele almasını sağlar. Bu, özellikle karmaşık ve çok adımlı görevlerde güvenilir ve yüksek kaliteli sonuçlar elde etmek için temel bir yaklaşımdır.
