# Rehber 04: RAG Tarifleri (Retrieval-Augmented Generation) - Türkçe Açıklama

Bu doküman, `10_guides_zero_to_hero/04_rag_recipes.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, yapay zeka modellerine harici bir "beyin" veya "kütüphane" vererek, onların sadece kendi eğitim verileriyle değil, sizin sağladığınız belgelerle de soruları yanıtlamasını sağlayan **Retrieval-Augmented Generation (RAG)** sistemlerinin nasıl kurulacağını öğretir.

## Betiğin Amacı

Önceki rehberler, LLM'e tek seferde verilen komutlara odaklanıyordu. Bu rehber ise LLM'i, kendi belirlediğimiz bir bilgi tabanından (örneğin, bir dizi PDF, metin dosyası veya web sayfası) aktif olarak bilgi alıp kullanabilen bir sisteme dönüştürür.

Bu betik, RAG sistemleri kurmak için farklı karmaşıklık seviyelerinde, yeniden kullanılabilir ve pratik "yemek tarifleri" sunar. Ana hedefleri şunlardır:

1.  **Temel RAG İş Akışını Göstermek:** Bir RAG sisteminin üç temel adımını (Hazırlık, Arama, Üretim) somut kodlarla göstermek.
2.  **Doküman İşleme Tekniklerini Öğretmek:** Uzun belgelerin nasıl yönetilebilir parçalara (`chunks`) ayrılacağını ve bu parçaların nasıl endeksleneceğini öğretmek.
3.  **Vektör Arama Sanatını Tanıtmak:** Metinlerin anlamsal "parmak izlerini" (embeddings) kullanarak, bir soruya en alakalı bilgi parçacıklarını nasıl bulacağımızı göstermek.
4.  **Farklı RAG Stratejilerini Karşılaştırmak:** Basit bir RAG'dan, daha verimli ve hibrit arama yapan gelişmiş RAG'lara kadar farklı yaklaşımları uygulamak ve aralarındaki farkları göstermek.
5.  **Performansı Ölçülebilir Kılmak:** Kurulan RAG sisteminin ne kadar hızlı, ne kadar maliyetli ve ne kadar verimli çalıştığını ölçmek için metrikler ve görselleştirmeler sunmak.

## Betikteki Ana Kavramlar ve "Tarifler"

Betiğin içindeki kod, bir RAG sisteminin temel bileşenlerini ve bu bileşenleri birleştiren farklı "tarifleri" (Python sınıfları) içerir.

### Temel RAG İş Akışı

Her RAG sistemi şu üç adımı takip eder:

1.  **Hazırlık (Indexing):** Bilgi tabanınızdaki belgeler okunur, daha küçük ve yönetilebilir parçalara (`chunks`) bölünür. Ardından her bir parçanın anlamsal bir vektör temsili (`embedding`) oluşturulur ve bir veritabanına kaydedilir. Bu işlem bir kere yapılır.
2.  **Arama (Retrieval):** Kullanıcı bir soru sorduğunda, önce sorunun `embedding`'i oluşturulur. Bu `embedding`, veritabanındaki en alakalı belge parçacıklarını bulmak için kullanılır (vektör benzerlik araması).
3.  **Üretim (Generation):** Arama adımında bulunan en alakalı belge parçaları, kullanıcının orijinal sorusuyla birleştirilerek LLM'e gönderilecek nihai bir komut (`prompt`) oluşturulur. LLM, bu zenginleştirilmiş bağlamı kullanarak soruyu yanıtlar.

### Betikteki RAG Tarifleri (Sınıflar)

*   **`SimpleRAG` (Basit RAG):** En temel tariftir. Az sayıda ve kısa dokümanlar için uygundur. Tüm dokümanları tek tek ele alır ve basit bir benzerlik araması yapar.
*   **`ChunkedRAG` (Parçalanmış RAG):** En yaygın ve pratik tariftir. Uzun dokümanları daha küçük parçalara ayırarak işler. Bu, hem arama kalitesini artırır hem de büyük bilgi tabanlarıyla çalışmayı mümkün kılar. Ayrıca, aramayı hızlandırmak için verimli bir kütüphane olan `FAISS`'i kullanır.
*   **`HybridRAG` (Hibrit RAG):** Gelişmiş bir tariftir. Anlamsal (embedding tabanlı) aramanın gücünü, geleneksel anahtar kelime (`keyword`) aramasıyla birleştirir. Bu, özellikle ürün kodları, özel isimler veya teknik terimler gibi belirli kelimelerin önemli olduğu durumlarda çok daha isabetli sonuçlar verir.

## Önemli Çıkarımlar

Bu rehber, LLM'lere harici bilgiyle akıl yürütme yeteneği kazandırmanın pratik yollarını sunar:

*   **RAG, Tek Bir Şey Değildir:** RAG, farklı ihtiyaçlara göre uyarlanabilen bir dizi teknik ve "tariftir".
*   **"Çöp Girdi, Çöp Çıktı":** Bir RAG sisteminin kalitesi, büyük ölçüde dokümanları ne kadar iyi parçaladığınıza ve arama mekanizmanızın ne kadar isabetli olduğuna bağlıdır.
*   **Ölçmek Her Şeydir:** Bir RAG sisteminin yavaş çalışması veya alakasız bilgi getirmesi, onu işe yaramaz hale getirir. Bu yüzden maliyet, hız ve verimlilik gibi metrikleri sürekli izlemek kritik öneme sahiptir.
*   **Hibrit Yaklaşımlar Güçlüdür:** Anlamsal arama ile anahtar kelime aramasını birleştirmek, genellikle tek bir yönteme göre daha sağlam ve güvenilir sonuçlar üretir.
*   **Bu Betik Bir Şablondur:** Buradaki kod, kendi RAG sistemlerinizi kurmak için doğrudan kullanabileceğiniz veya ilham alabileceğiniz eksiksiz bir başlangıç noktasıdır.
