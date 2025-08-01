# Moleküller: Komutları Örneklerle Birleştirmek (Türkçe Özet)

Bu doküman, `00_foundations/02_molecules_context.md` dosyasının Türkçe bir özetidir.

> "Bütün, parçalarının toplamından daha büyüktür." — Aristoteles

## Atomlardan Moleküllere

Önceki bölümde, LLM etkileşiminin temel birimi olan **atomik komutları** inceledik. Şimdi bu atomları birleştirerek **moleküller** oluşturacağız: yani, modelin takip etmesi için örnekler ve kalıplar içeren yapılandırılmış bağlamlar.

`MOLEKÜL = [TALİMAT] + [ÖRNEKLER] + [BAĞLAM] + [YENİ GİRDİ]`

Bu moleküler yaklaşım, LLM'lerin güçlü bir yeteneğinden yararlanır: **Few-Shot Learning (Az Örnekle Öğrenme)**.

## Few-Shot Learning: Örneklerle Öğretme

Az örnekle öğrenme, istediğimiz girdi-çıktı kalıbına dair birkaç örnek sunarak modelin bu kalıbı tanımasını ve devam ettirmesini sağlama yöntemidir.

Örneğin:

```
Girdi: "Paris"
Çıktı: "Paris, Fransa'nın başkentidir."

Girdi: "Tokyo"
Çıktı: "Tokyo, Japonya'nın başkentidir."

Girdi: "Ottawa"
Çıktı: ?
```

Model bu kalıbı tanır ve şu şekilde tamamlar: "Ottawa, Kanada'nın başkentidir."

## Moleküler Yaklaşımın Avantajları

Aynı görev için atomik ve moleküler yaklaşımları karşılaştıralım:

| Atomik Yaklaşım | Moleküler Yaklaşım |
|---|---|
| "Bu yorumu pozitif veya negatif olarak sınıflandır: 'Servis berbattı ve yemek soğuktu.'" | "Yorumların duygu durumunu sınıflandır.<br><br>Yorum: 'Yemek harikaydı!'<br>Duygu: Pozitif<br><br>Yorum: '30 dakika bekledik ve yemek soğuktu.'<br>Duygu: Negatif<br><br>Yorum: 'Servis berbattı ve yemek soğuktu.'<br>Duygu:" |

Moleküler yaklaşım genellikle şunları sağlar:

*   **Daha Yüksek Doğruluk:** Birçok görevde %10-30 oranında iyileşme.
*   **Daha Fazla Tutarlılık:** Çıktılardaki değişkenliğin azalması.
*   **Formata Daha İyi Uyum:** İstenen çıktı formatına daha sadık kalınması.
*   **İstisnai Durumların Daha Net Ele Alınması:** Kenar durumlarla daha iyi başa çıkma.

## Etkili Moleküler Şablonlar Tasarlamak

Moleküler bağlamınızın yapısı büyük önem taşır. Yaygın kullanılan kalıplar şunlardır:

*   **Ön Ek-Son Ek (Prefix-Suffix):** En basitidir, basit görevler için iyi çalışır.
*   **Girdi-Çıktı Çiftleri (Input-Output Pairs):** Sınırları nettir, yapılandırılmış veriler için iyidir.
*   **Düşünce Zinciri (Chain-of-Thought):** Modelin akıl yürütme adımlarını görmesini sağlar, karmaşık görevler için en iyisidir.

## Örnek Seçiminin Bilimi

Her örnek eşit derecede değerli değildir. Moleküler bağlamınız için örnek seçerken:

*   **Çeşitlilik:** Farklı durumları kapsayarak modelin yelpazeyi görmesini sağlayın.
*   **Kenar Durumlar:** Sınırları netleştirmek için istisnai durumları ekleyin.
*   **Sıralama:** Mümkünse basitten karmaşığa doğru sıralayın.
*   **Yakın Hatalar:** Kesin sınırları belirlemek için hedefe çok yakın ama yanlış olan örnekler ekleyin.

## Moleküler Verimliliği Ölçme: Azalan Getiriler

Bağlamın boyutu arttıkça token sayısı da artar. Her eklenen örneğin maliyeti vardır ve getirdiği fayda bir öncekinden daha azdır. Bu duruma **azalan getiriler** denir. Çoğu görev için kalite ve token verimliliğini dengeleyen optimal bir örnek sayısı vardır (genellikle 1-5 arası).

## Dinamik Molekül Oluşturma

İleri düzey bağlam mühendisliği, her bir girdi için en alakalı örnekleri dinamik olarak seçmeyi içerir. Bu yaklaşım:

1.  Kullanıcının sorgusunu analiz eder.
2.  En alakalı örnekleri bir veritabanından çeker.
3.  Kişiye özel, optimize edilmiş bir moleküler bağlam oluşturur.
4.  Bu optimize edilmiş bağlamı LLM'e gönderir.

## Önemli Çıkarımlar

1.  **Moleküler bağlamlar**, talimatları örneklerle birleştirerek LLM performansını artırır.
2.  **Az örnekle öğrenme**, modellerin kalıpları tanımasını ve devam ettirmesini sağlar.
3.  **Şablon yapısı** ve **örnek seçimi** kritik öneme sahiptir.
4.  Eklenen her örneğin bir maliyeti vardır ve **azalan getiriler** kanununa tabidir.
5.  **Dinamik yapılandırma**, her girdi için bağlamı optimize edebilir.

## Sonraki Adımlar

Bir sonraki bölümde, birden fazla etkileşim boyunca hafızayı ve durumu koruyan bağlam yapıları olan **hücreleri (cells)** keşfedeceğiz.
