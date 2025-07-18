# Şablon: Alan Rezonans Ölçümü (Field Resonance Measure) - Türkçe Açıklama

Bu doküman, `20_templates/field_resonance_measure.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, "Nöral Alanlar" gibi soyut bir kavramı, somut ve ölçülebilir metriklere dönüştürmek için bir araç seti ve şablon sunar.

## Şablonun Amacı

`00_foundations` bölümünde, bağlamın (context) birbiriyle etkileşen, yankılanan (rezonans) ve zamanla kararlı yapılar (çekiciler) oluşturan bir "alan" gibi davrandığı teorisini inceledik. Bu şablon, bu teorik fikirleri pratiğe döker ve şu soruları yanıtlamamızı sağlar:

*   İki fikir veya metin parçası birbiriyle ne kadar **uyumlu (rezonans)**?
*   Bir bağlamdaki tüm fikirler birbiriyle ne kadar **tutarlı (coherence)**?
*   Oluşturduğumuz bağlam ne kadar **kararlı (stability)** ve değişime ne kadar açık?
*   Bağlamımızdaki bilgi ne kadar **düzenli veya dağınık (entropy)**?

Bu şablon, bu metrikleri hesaplamak için yeniden kullanılabilir Python sınıfları sunarak, tasarladığımız bağlam sistemlerinin kalitesini ve davranışını nicel olarak analiz etmemize olanak tanır.

## Şablonun Yapısı ve Ana Bileşenleri

### 1. `ResonanceMeasurer` (Rezonans Ölçer)
*   **Ne Yapar?** İki metin parçasının (desenin) anlamsal olarak ne kadar benzer veya uyumlu olduğunu ölçer. Bu, "rezonans" olarak adlandırılır.
*   **Ölçüm Yöntemleri:**
    *   **`cosine`:** Kelime frekanslarına dayalı klasik kosinüs benzerliği.
    *   **`overlap`:** Ortak kelime oranına dayalı (Jaccard benzerliği) daha basit bir ölçüm.
    *   **`embedding`:** Metinleri anlamsal vektörlere dönüştürüp bu vektörler arasındaki benzerliği ölçen en gelişmiş yöntem.

### 2. `CoherenceMeasurer` (Tutarlılık Ölçer)
*   **Ne Yapar?** Bir "alanın" (yani bir bağlamdaki tüm metin parçalarının) kendi içindeki genel tutarlılığını ölçer.
*   **Ölçüm Yöntemleri:**
    *   **`pairwise_coherence`:** Alandaki tüm metinlerin ikili rezonanslarının ortalamasını alır. Yüksek bir skor, alandaki her şeyin birbiriyle ilişkili olduğunu gösterir.
    *   **`attractor_alignment`:** Alandaki metinlerin, ana fikirleri temsil eden "çekicilere" ne kadar uyumlu olduğunu ölçer. Yüksek bir skor, alanın belirli ana temalar etrafında iyi organize olduğunu gösterir.
    *   **`entropy_coherence`:** Alanın ne kadar düzenli veya dağınık olduğunu ölçer. Düşük entropi (yüksek tutarlılık), alanın iyi organize olduğunu gösterir.

### 3. `StabilityMeasurer` (Kararlılık Ölçer)
*   **Ne Yapar?** Bir alanın zaman içinde değişime ne kadar dirençli olduğunu ölçer. Kararlı bir alan, yeni bilgilere rağmen ana temalarını korur.
*   **Nasıl Çalışır?** Alanın kararlılığını, içindeki "çekicilerin" gücü ve alandaki diğer metinlerin bu çekicilere ne kadar uyumlu olduğunun ağırlıklı bir ortalaması olarak hesaplar.

### 4. `FieldResonanceMeasurer` (Kapsamlı Alan Ölçer)
*   **Ne Yapar?** Yukarıdaki tüm ölçüm araçlarını tek bir sınıfta birleştirir ve bir alanın kapsamlı bir analizini sunar.
*   **Sağladığı Metrikler:** `coherence`, `stability`, `entropy`, `attractor_count` (çekici sayısı), `pattern_count` (desen sayısı) gibi birçok metriği tek seferde hesaplar.
*   **Görselleştirme:** Alanın durumunu özetleyen metin tabanlı, ASCII veya JSON formatında görselleştirmeler üretebilir.

### 5. `FieldAnalyzer` (Alan Analizörü)
*   **Ne Yapar?** `FieldResonanceMeasurer` tarafından üretilen metrikleri yorumlayarak, alanın durumu hakkında daha üst düzey analizler ve iyileştirme önerileri sunar.
*   **Örnek Analizler:**
    *   "Bu alan çok katı (rijit), yeni fikirlerin girmesi için zayıflatılması gerekiyor."
    *   "Bu alan çok dağınık (kaotik), ana fikirleri (çekicileri) güçlendirerek daha tutarlı hale getirilmeli."
    *   "Alandaki fikir çeşitliliği az, daha farklı kavramlar eklenmeli."

## Nasıl Kullanılır?

Bu şablon, tasarladığınız bir bağlam sisteminin (örneğin, bir RAG sistemi veya çok adımlı bir ajan) davranışını anlamak ve optimize etmek için kullanılır:

1.  Sisteminizin ürettiği bağlamı veya ara çıktıları bir "alan" olarak temsil edin.
2.  Bir `FieldResonanceMeasurer` nesnesi oluşturun.
3.  `get_field_metrics(field)` metodunu kullanarak alanınızın metriklerini hesaplayın.
4.  `FieldAnalyzer` kullanarak bu metrikleri yorumlayın ve sisteminizi nasıl daha iyi hale getirebileceğinize dair öneriler alın.

Bu şablon, bağlam mühendisliğini sezgisel bir sanattan, ölçülebilir ve optimize edilebilir bir mühendislik disiplinine dönüştürmek için temel bir araç seti sağlar.
