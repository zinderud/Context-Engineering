# Prompt Şablonu: Çekici Tasarımı (Attractor Design) - Türkçe Açıklama

Bu doküman, `20_templates/PROMPTS/attractor_design.md` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu şablon, bir LLM'in (Büyük Dil Modeli) akıl yürütme sürecini, ona ne yapacağını doğrudan söylemek yerine, onu belirli düşünce tarzlarına veya kavramsal çerçevelere doğru **dolaylı olarak yönlendirmek** için tasarlanmıştır.

## Şablonun Amacı

Bu şablonun temel fikri, projenin ileri düzey kavramlarından olan "Nöral Alanlar" teorisindeki **Çekici (Attractor)** kavramını kullanmaktır. Bir çekici, anlamsal uzayda bir "kütle çekim merkezi" gibi davranır; LLM'in düşüncelerini doğal olarak o yöne doğru çeker.

Doğrudan talimat vermek yerine (örneğin, "Sistem düşüncesi yaklaşımını kullan"), bu şablon, LLM'e "dikkate alınması faydalı olabilecek kavramlar" başlığı altında bir dizi ilgili fikir sunar. Bu, modelin bu fikirleri benimsemesini teşvik eder, ancak bunu bir zorunluluk olarak sunmaz. Bu yaklaşım, daha esnek, yaratıcı ve doğal hissettiren bir yönlendirme sağlar.

Bu şablon şu durumlar için idealdir:

*   Belirli bir düşünce stilini (örneğin, eleştirel düşünme, yaratıcı düşünme) teşvik etmek.
*   Cevabın belirli temalar etrafında şekillenmesini sağlamak.
*   Modele katı kurallar koymadan, onu nazikçe doğru yöne itmek.

## Şablonun Yapısı

Şablon, birkaç ana bölümden oluşur:

1.  **`Task` (Görev):** LLM'den yapması istenen ana görev. Bu bölümde, çekici kavramlardan **bahsedilmez**.
2.  **`Context` (Bağlam):** Görevle ilgili tarafsız arka plan bilgisi.
3.  **`Conceptual Framework` (Kavramsal Çerçeve):** Şablonun kalbidir. Burada, LLM'in düşünmesini istediğimiz ana fikirler (çekiciler) ve bu fikirleri güçlendiren alt maddeler sunulur. Genellikle "*Aşağıdaki kavramları dikkate almak faydalı olabilir:*" gibi bir ifadeyle sunulur.
4.  **`Approach` (Yaklaşım):** Modele, yukarıdaki kavramları analizine uygun şekilde dahil etmesini öneren kısa bir talimat.
5.  **`Expected Output` (Beklenen Çıktı):** Cevabın formatı ve yapısıyla ilgili beklentiler.

### Örnek Kullanım: Sistem Düşüncesi Çekicisi

*   **Görev:** Şehir içi ulaşımın zorluklarını analiz et.
*   **Kavramsal Çerçeve (Çekiciler):**
    *   **`Interconnectedness` (Birbiriyle Bağlantılı Olma):** Ulaşımın arazi kullanımı ve ekonomiyle ilişkisi.
    *   **`Feedback Loops` (Geri Besleme Döngüleri):** Altyapı yatırımlarının davranışları nasıl şekillendirdiği.
    *   **`Emergence` (Kendiliğinden Belirme):** Bireysel kararlardan doğan beklenmedik trafik desenleri.

Bu yapı, LLM'i problemi sadece "yollar ve arabalar" olarak değil, birbiriyle ilişkili parçalardan oluşan karmaşık bir **sistem** olarak düşünmeye teşvik eder.

## Varyasyonlar

*   **`Multi-Attractor Field` (Çoklu Çekici Alanı):** Farklı güçlerde birden fazla çekici sunarak, bazı fikirlerin daha baskın olmasını sağlamak.
*   **`Attractor-Repeller Dynamics` (Çekici-İtici Dinamikleri):** Modele sadece benimsemesi gereken yaklaşımları (`attractors`) değil, aynı zamanda kaçınması gereken yaklaşımları da (`repellers`) sunmak.
*   **`Resonant Field Attractor` (Rezonans Alanı Çekicisi):** Birbirini güçlendiren ve yankılayan (rezonans) bir dizi bağlantılı kavram sunarak daha karmaşık ve bütüncül bir düşünce alanı yaratmak.

## En İyi Uygulamalar

*   **Zorlama, Yönlendir:** Çekicileri birer gereklilik gibi değil, birer "tavsiye" gibi sunun.
*   **Tutarlı Ol:** Birbiriyle uyumlu ve birbirini destekleyen çekici kavramlar seçin.
*   **Dengeyi Bul:** Çok belirsiz kavramlar yeterli çekim gücü oluşturmaz, çok spesifik kavramlar ise yaratıcılığı kısıtlar.

Bu şablon, LLM ile etkileşimde ince ayar yapmanın ve onun düşünce süreçlerini bir heykeltıraş gibi şekillendirmenin güçlü bir yoludur.