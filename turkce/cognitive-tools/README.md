# Bağlam Mühendisliği için Bilişsel Araçlar

Bu dizin, dil modellerinin (LLM) daha yapılandırılmış, güvenilir ve etkili bir şekilde akıl yürütmesini sağlamak için tasarlanmış "Bilişsel Araçları" içerir.

## Bilişsel Araç Nedir?

Bilişsel araçlar, insanların problem çözerken kullandığı zihinsel modellere (analoji kurma, problemi parçalara ayırma, varsayımları test etme vb.) benzer şekilde, yapay zekaya karmaşık görevlerde yol gösteren yapılandırılmış istem (prompt) kalıplarıdır. Bu araçlar, yapay zekanın sadece bilgi üretmesini değil, aynı zamanda bu bilgiyi nasıl işleyeceğini de yönlendirir.

IBM tarafından yapılan araştırmalar, bu tür araçların yapay zekanın matematiksel akıl yürütme gibi zorlu görevlerdeki performansını **%16.6'ya varan oranlarda artırdığını** göstermiştir.

## Bu Dizinin Yapısı

Bu dizin, bilişsel araçları farklı seviyelerde organize eder:

*   `cognitive-templates/`: **Bilişsel Şablonlar:** Anlama, akıl yürütme, doğrulama gibi tekil bilişsel görevler için yeniden kullanılabilir istem şablonları içerir.
*   `cognitive-programs/`: **Bilişsel Programlar:** Birden fazla şablonu bir araya getirerek daha karmaşık, kod benzeri akıl yürütme akışları oluşturur.
*   `cognitive-schemas/`: **Bilişsel Şemalar:** Bilginin farklı alanlarda (kullanıcı, görev, alan bilgisi) nasıl yapılandırılacağını tanımlayan standart formatlar sunar.
*   `cognitive-architectures/`: **Bilişsel Mimariler:** Problem çözme, eğitmenlik veya araştırma gibi belirli amaçlar için tasarlanmış, birden fazla aracı ve şemayı birleştiren bütünsel sistemlerdir.
*   `integration/`: **Entegrasyon:** Bu bilişsel araçların, artırılmış üretim (RAG), hafıza sistemleri ve otonom ajanlar gibi diğer yapay zeka bileşenleriyle nasıl entegre edileceğine dair rehberler içerir.
*   `meta-cognition/`: **Üst-Biliş (Meta-Biliş):** Sistemin kendi akıl yürütme süreçlerini analiz etmesi, değerlendirmesi ve zamanla kendi kendini iyileştirmesi için tasarlanmış en gelişmiş araçları barındırır.

## Neden Önemli?

*   **Performans:** Akıl yürütme görevlerinde doğruluğu önemli ölçüde artırır.
*   **Güvenilirlik:** Modelin hata yapma ve "halüsinasyon görme" olasılığını azaltır.
*   **Verimlilik:** Daha az kaynak (token) kullanarak daha iyi sonuçlar elde edilmesini sağlar.
*   **Esneklik:** Matematikten yaratıcı yazıma kadar çok çeşitli alanlara uygulanabilir.

Bu dizin, basit istem mühendisliğinden, yapay zekaya yapılandırılmış düşünme yetenekleri kazandıran bütünsel "Bilişsel Mimarilere" doğru bir yol haritası sunmaktadır.
