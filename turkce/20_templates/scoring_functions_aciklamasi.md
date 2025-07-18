# Şablon: Puanlama Fonksiyonları (Scoring Functions) - Türkçe Açıklama

Bu doküman, `20_templates/scoring_functions.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, bir LLM (Büyük Dil Modeli) tarafından üretilen cevapların veya bir bağlamın kalitesini **nicel olarak ölçmek** için bir dizi yeniden kullanılabilir **puanlama fonksiyonu** sunar.

## Şablonun Amacı

Bağlam mühendisliğinde farklı yaklaşımları (örneğin, farklı komutlar, farklı RAG stratejileri) denerken, hangisinin daha iyi olduğunu öznel bir şekilde değerlendirmek zordur. Bu şablon, bu değerlendirmeyi nesnel ve tekrarlanabilir hale getirmeyi amaçlar. "İyi bir cevap" veya "iyi bir bağlam" kavramlarını, aşağıdakiler gibi ölçülebilir metriklere ayırır:

1.  **İlgililik (Relevance):** Cevap, sorulan soruyla ne kadar ilgili?
2.  **Tutarlılık (Coherence):** Cevap, kendi içinde mantıksal olarak ne kadar tutarlı ve akıcı?
3.  **Kapsamlılık (Comprehensiveness):** Cevap, konuyu ne kadar eksiksiz bir şekilde ele alıyor?
4.  **Özlülük (Conciseness):** Cevap, bilgiyi gereksiz kelimeler kullanmadan ne kadar verimli bir şekilde sunuyor?
5.  **Doğruluk (Accuracy):** Cevaptaki bilgiler, referans bir kaynağa göre ne kadar doğru?
6.  **Token Verimliliği (Token Efficiency):** Cevap, ayrılan token bütçesini ne kadar verimli kullanıyor?
7.  **Alan Rezonansı (Field Resonance):** Cevap, projenin ileri düzey kavramı olan "Nöral Alan"ın genel yapısıyla ne kadar uyumlu?

Bu fonksiyonlar, farklı bağlam mühendisliği stratejilerini A/B testi gibi yöntemlerle karşılaştırmak ve en iyi yaklaşımı bilimsel bir temele dayanarak seçmek için kritik öneme sahiptir.

## Şablonun Yapısı ve Ana Fonksiyonlar

Betiğin içindeki fonksiyonlar, farklı kalite boyutlarını ölçmek üzere gruplandırılmıştır:

### 1. Metin İşleme Yardımcıları (`tokenize`, `jaccard_similarity` vb.)
*   **Ne Yapar?** Puanlama fonksiyonlarının ihtiyaç duyduğu temel metin işleme görevlerini (metni kelimelere ayırma, iki metin arasındaki benzerliği hesaplama vb.) yerine getiren yardımcı fonksiyonlardır.

### 2. Temel Puanlama Fonksiyonları
*   **`score_relevance(response, query)`:** Bir cevabın, sorulan soruyla kelime bazında ne kadar örtüştüğünü ölçer.
*   **`score_coherence(text)`:** Bir metnin cümleleri arasındaki anlamsal bağlantıyı ve geçiş kelimelerinin kullanımını analiz ederek metnin akıcılığını puanlar.
*   **`score_comprehensiveness(response, reference)`:** Bir cevabın, referans (doğru kabul edilen) bir metindeki anahtar noktaları ne kadar kapsadığını ölçer.
*   **`score_conciseness(response, reference)`:** Bir cevabın, aynı bilgiyi referans metne göre daha az veya daha çok kelimeyle mi anlattığını ölçer.
*   **`score_accuracy(response, reference)`:** Bir cevabın, referans metindeki olgusal bilgileri ne kadar doğru bir şekilde içerdiğini kontrol eder.
*   **`score_token_efficiency(response, max_tokens)`:** Bir cevabın, verilen token bütçesini ne kadar verimli kullandığını (ne çok kısa ne de çok uzun) ve bilgi yoğunluğunu ölçer.

### 3. Nöral Alan Puanlama Fonksiyonları
*   **`score_field_resonance(response, field)`:** Bir cevabın, bir "nöral alanın" ana fikirleriyle (çekicileriyle) ne kadar uyumlu olduğunu puanlar.
*   **`score_field_coherence(response, field)`:** Bir cevabın, alanın genel yapısına ve tutarlılığına ne kadar katkıda bulunduğunu ölçer.

### 4. Protokol Puanlama Fonksiyonları
*   **`score_protocol_adherence(response, protocol)`:** Bir cevabın, önceden tanımlanmış bir protokolün (akıl yürütme adımları) adımlarını ne kadar iyi takip ettiğini ölçer.
*   **`score_protocol_output_match(response, protocol)`:** Cevap içinde üretilen yapılandırılmış çıktının (örneğin, JSON), protokolün beklediği çıktı şemasına ne kadar uyduğunu kontrol eder.

### 5. `score_response` (Kapsamlı Puanlama Fonksiyonu)
*   **Ne Yapar?** Yukarıdaki tüm bireysel puanlama fonksiyonlarını tek bir seferde çalıştırır ve bir cevap için her bir kalite boyutunu içeren kapsamlı bir **puan kartı** oluşturur. Ayrıca, bu metriklerin ağırlıklı bir ortalamasını alarak genel bir kalite puanı (`overall`) hesaplar.

## Nasıl Kullanılır?

Bu şablondaki fonksiyonlar, bir LLM uygulamasının test ve değerlendirme aşamasında kullanılır:

1.  Farklı bağlam stratejileriyle aynı soruya birkaç farklı cevap üretin.
2.  Bu cevapları, bir referans metin veya bir dizi anahtar nokta ile birlikte `score_response` fonksiyonuna verin.
3.  Fonksiyonun döndürdüğü puan kartlarını karşılaştırarak, hangi bağlam stratejisinin daha ilgili, daha doğru, daha tutarlı veya daha verimli sonuçlar ürettiğini nesnel olarak belirleyin.

Bu şablon, bağlam mühendisliği sürecine bilimsel bir titizlik katarak, en iyi sonuçları veren yaklaşımları sistematik olarak bulmanıza yardımcı olur.
