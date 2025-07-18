# Prompt Şablonu: Düşünce Zinciri (Chain of Thought) - Türkçe Açıklama

Bu doküman, `20_templates/PROMPTS/chain_of_thought.md` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu şablon, bir yapay zeka (AI) modelinin karmaşık problemleri çözerken daha doğru ve güvenilir sonuçlar üretmesini sağlamak için en yaygın ve etkili tekniklerden biri olan **Düşünce Zinciri (Chain of Thought - CoT)** yöntemini uygulamak için tasarlanmıştır.

## Şablonun Amacı

Bir LLM'den zor bir soruyu doğrudan cevaplamasını istediğimizde, model bazen aceleci davranıp mantık hataları yapabilir. Düşünce Zinciri tekniği bu sorunu çözer. Modelden, cevabı vermeden önce problemi nasıl çözdüğünü **adım adım açıklaması** istenir. Bu süreç, modeli daha yavaş, daha metodik ve daha mantıklı düşünmeye zorlar. Sonuç olarak, hem cevabın doğruluğu artar hem de modelin cevaba nasıl ulaştığı şeffaf bir şekilde görülebilir hale gelir.

Bu şablon, aşağıdaki gibi durumlar için idealdir:

*   Matematiksel veya mantıksal akıl yürütme gerektiren problemler.
*   Çok adımlı analiz veya hesaplama gerektiren görevler.
*   Bir kararın arkasındaki "neden"in, kararın kendisi kadar önemli olduğu durumlar.
*   Zorlu problemlerde hata yapma olasılığını azaltmak.

## Şablonun Yapısı

Şablon, oldukça basit ve etkili bir yapıya sahiptir:

1.  **`Task` (Görev):** Çözülmesi gereken problem veya cevaplanması gereken soru net bir şekilde tanımlanır.
2.  **`Approach` (Yaklaşım):** Şablonun en kritik kısmıdır. Modele, "**Bunu adım adım düşün:**" talimatı verilir ve ardından izlemesi gereken mantıksal adımlar listelenir. Bu adımlar, problemin türüne göre özelleştirilir.
3.  **`Expected Output` (Beklenen Çıktı):** Modelden, hem tüm akıl yürütme sürecini hem de en sondaki nihai cevabını sunması istenir.

### Örnek Kullanım: Matematik Problemi

*   **Görev:** Bir kelime problemi verilir.
*   **Yaklaşım (Adımlar):
    1.  Değişkenleri tanımla.
    2.  Verilen bilgilere göre denklemleri kur.
    3.  Denklemleri çöz.
    4.  Cevabın mantıklı olup olmadığını kontrol et.

Bu yapı, modeli problemi rastgele çözmek yerine, bir matematikçinin izleyeceği yapısal bir yola sokar.

## Varyasyonlar

*   **`Self-Prompted Chain of Thought` (Kendi Kendine Yönlendirilen Düşünce Zinciri):** Modele hazır adımlar vermek yerine, ondan problemi önce kendi mantıksal adımlarına ayırmasını ve sonra bu adımları takip etmesini istemek. Bu, modelin problem çözme yeteneğini daha da geliştirir.
*   **`Guided Problem Decomposition` (Yönlendirilmiş Problem Ayrıştırma):** Çok karmaşık problemler için, problemi daha küçük alt problemlere ayırarak her birini ayrı ayrı çözmesini istemek ve en sonunda sonuçları birleştirmesini sağlamak.
*   **`Scenario Analysis Chain of Thought` (Senaryo Analizi Düşünce Zinciri):** Farklı senaryoların (örneğin, "Eğer A olursa ne olur?", "Eğer B olursa ne olur?") analizini gerektiren karar verme problemleri için kullanılır.

## En İyi Uygulamalar

*   **Adımları Probleme Göre Ayarla:** Her problem türü (matematik, etik, mantık) farklı düşünce adımları gerektirir.
*   **Doğrulama Adımı Ekle:** Modelin kendi cevabını kontrol etmesini sağlayacak bir adım eklemek (örneğin, "Cevabının mantıklı olduğundan emin ol") hataları azaltır.
*   **Adım Sayısını Optimize Et:** Genellikle 3 ila 7 adım idealdir. Çok az adım yetersiz yönlendirme sağlar, çok fazla adım ise kafa karıştırıcı olabilir.

Bu şablon, LLM'lerin "kara kutu" doğasını daha şeffaf, güvenilir ve denetlenebilir bir hale getirmek için en temel ve güçlü araçlardan biridir.
