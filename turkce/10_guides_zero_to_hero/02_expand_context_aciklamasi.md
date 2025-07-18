# Rehber 02: Bağlamı Genişletme (Expand Context) - Türkçe Açıklama

Bu doküman, `10_guides_zero_to_hero/02_expand_context.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, bir önceki rehberde incelenen basit "atomik" komutların üzerine nasıl katman katman yeni bilgiler eklenerek daha güçlü ve etkili "moleküler" bağlamlar oluşturulacağını gösterir.

## Betiğin Amacı

Bu rehber, bağlam mühendisliğinin temel sanatını öğretir: Bir yapay zeka modeline sadece ne yapacağını söylemek değil, aynı zamanda görevi en iyi şekilde yerine getirmesi için gerekli olan zenginleştirilmiş bilgiyi sağlamak. Betik, bu genişletme işleminin etkilerini hem nicel (token sayısı, gecikme süresi) hem de nitel (cevap kalitesi) olarak ölçmek için pratik yöntemler sunar.

Ana hedefleri şunlardır:

1.  **Bağlam Katmanlarını Tanıtmak:** Basit bir komuta nasıl farklı bilgi katmanları (rol, örnekler, kısıtlamalar, hedef kitle) ekleneceğini göstermek.
2.  **Etkiyi Ölçmek:** Eklenen her katmanın token maliyetini, cevap hızını ve cevap kalitesini nasıl etkilediğini somut metriklerle analiz etmek.
3.  **Kalıpları Formalleştirmek:** Etkili bağlam genişletme tekniklerini (örneğin, rol atama, az sayıda örnekle öğrenme) yeniden kullanılabilir bir şablon haline getirmek.
4.  **Optimizasyon Tekniklerini Keşfetmek:** Bağlamı zenginleştirirken token maliyetini düşürmek için bağlamı sıkıştırma (özetleme, anahtar kelime çıkarma) ve gereksiz bilgiyi budama gibi ileri düzey teknikleri tanıtmak.
5.  **Harici Bilgiyle Zenginleştirme (RAG):** Bağlamı, harici bir bilgi kaynağından (örneğin bir doküman arşivi) ilgili bilgileri çekerek dinamik olarak nasıl genişleteceğimizi (Retrieval-Augmented Generation) göstermek.

## Betikteki Deneyler ve Kavramlar

Betiğin içindeki kod, birkaç ana bölümden oluşur:

*   **Bağlam Genişletme Teknikleri:** Temel bir komut (`"İklim değişikliği hakkında bir paragraf yaz."`) alınır ve bu komuta farklı katmanlar eklenerek çeşitli versiyonları oluşturulur:
    *   **Rol Ekleme:** `"Sen bir çevre bilimcisisin..."`
    *   **Örnek Ekleme:** `"İşte bir örnek paragraf..."`
    *   **Kısıtlama Ekleme:** `"Şu kurallara uy..."`
    *   **Hedef Kitle Belirleme:** `"Bu paragrafı lise öğrencileri için yaz..."`
    *   **Kapsamlı Birleştirme:** Yukarıdakilerin hepsinin stratejik bir birleşimi.

*   **Görsel Analiz:** Bu farklı komut versiyonlarının token maliyetleri, cevaplama süreleri ve verimlilikleri (harcanan token başına alınan cevap token'ı) grafiklerle görselleştirilir.

*   **Nitel Analiz:** Üretilen cevapların içerikleri karşılaştırılarak, hangi bağlam katmanının kaliteyi ne yönde etkilediği incelenir.

*   **Bağlam Şablonu:** Öğrenilenleri bir araya getiren, farklı bağlam katmanlarını programatik olarak birleştiren yeniden kullanılabilir bir Python fonksiyonu (`create_expanded_context`) oluşturulur.

*   **İleri Düzey Optimizasyon:**
    *   **Bağlam Sıkıştırma:** Uzun bir bağlamın, LLM kullanılarak nasıl daha az token kaplayan bir özete, anahtar kelime listesine veya madde imli listeye dönüştürülebileceği gösterilir.
    *   **Bağlam Budama:** Bir bağlamdaki hangi katmanların kaliteye katkı sağlamadığını sistematik olarak test edip, gereksiz olanları ayıklayan bir yöntem sunulur.

*   **Retrieval-Augmented Generation (RAG):** Basit bir bilgi tabanından, kullanıcının sorusuyla ilgili dokümanları bulan ve bunları komuta otomatik olarak ekleyen bir sistem simüle edilir.

## Önemli Çıkarımlar

Bu rehber, "daha fazla bağlam her zaman daha iyidir" yanılgısını yıkar ve şu temel dersleri verir:

*   **Stratejik Katmanlama:** Bağlamı rastgele eklemek yerine, rol, örnek, kural gibi modüler katmanlar halinde eklemek ve her birinin etkisini ayrı ayrı test etmek en iyisidir.
*   **Ölç ve Optimize Et:** En iyi bağlam, kalite, maliyet ve hız arasında optimum dengeyi kuran bağlamdır. Bu dengeyi bulmak için sürekli ölçüm yapmak şarttır.
*   **Budamaktan Korkma:** Eğer bir bilgi katmanı (örneğin, bir konunun gereksiz tarihçesi) cevabın kalitesini artırmıyorsa, token maliyetini düşürmek için onu kaldırmak daha iyidir.
*   **Dinamik Ol:** Her soru için aynı genel bağlamı kullanmak yerine, RAG gibi tekniklerle o anki soruya en uygun bilgiyi dinamik olarak bağlama eklemek, çok daha verimli ve etkilidir.

Bu rehber, statik komutlardan, göreve özel olarak tasarlanmış, optimize edilmiş ve dinamik olarak zenginleştirilmiş bağlamlar oluşturmaya geçişi öğretir.
