# Rehber 03: Kontrol Döngüleri (Control Loops) - Türkçe Açıklama

Bu doküman, `10_guides_zero_to_hero/03_control_loops.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, tek adımlı komutların ötesine geçerek, bir görevi tamamlamak için yapay zeka modelinin birden çok kez ve farklı şekillerde kullanıldığı **çok adımlı kontrol mekanizmalarını** tanıtır.

## Betiğin Amacı

Önceki rehberler tek bir etkileşime odaklanırken, bu rehber LLM'i bir orkestra şefi gibi yöneterek karmaşık görevleri başarmayı hedefler. Tıpkı bir yazılımda `if-else` blokları veya `for` döngüleri gibi, bu betikteki sınıflar da LLM'in düşünce ve eylem akışını kontrol etmek için kullanılır. Amaç, daha sağlam, akıllı ve kendi kendini düzeltebilen sistemler kurmaktır.

Bu betik, aşağıdaki gibi temel kontrol akışı desenlerini uygulamak için yeniden kullanılabilir Python sınıfları sunar:

1.  **Sıralı Zincirleme (Sequential Chaining):** Bir işlemin çıktısını bir sonrakine girdi olarak bağlamak.
2.  **Yinelemeli İyileştirme (Iterative Refinement):** Bir çıktıyı, geri bildirim döngüleriyle sürekli daha iyi hale getirmek.
3.  **Koşullu Dallanma (Conditional Branching):** Gelen bir girdiyi analiz edip, türüne göre farklı bir işlem yoluna yönlendirmek.
4.  **Kendi Kendini Eleştirme (Self-Critique):** Modelin tek bir adımda hem cevap üretip hem de o cevabı eleştirip daha iyisini sunmasını sağlamak.
5.  **Harici Doğrulama (External Validation):** Modelin ürettiği bir çıktıyı (örneğin bir kod parçası), harici bir araçla (örneğin bir kod derleyici) test etmek ve hata varsa düzeltmesini istemek.

## Betikteki Ana Sınıflar (Kontrol Döngüsü Türleri)

Betiğin kalbini, her biri farklı bir kontrol deseni uygulayan 5 ana sınıf oluşturur:

### 1. `SequentialChain` (Sıralı Zincir)
*   **Ne Yapar?** Bir montaj hattı gibi çalışır. Bir başlangıç girdisi alır, onu bir dizi adımdan geçirir ve her adımın çıktısı bir sonraki adımın girdisi olur.
*   **Örnek Kullanım:** Bir metinden önce anahtar varlıkları çıkaran, sonra bu varlıklar arasındaki ilişkileri analiz eden ve son olarak bu analizden bir rapor oluşturan üç adımlı bir sistem.

### 2. `IterativeRefiner` (Yinelemeli İyileştirici)
*   **Ne Yapar?** Bir ilk taslak oluşturur ve ardından "bunu nasıl daha iyi yapabilirim?" sorusunu tekrar tekrar sorarak kendini geliştirir. Her döngüde, ya kendi kendine ya da bir insandan geri bildirim alarak çıktıyı iyileştirir.
*   **Örnek Kullanım:** Bir makale taslağı yazmak, ardından bu taslağı "daha akıcı yap", "bir örnek ekle" gibi geri bildirimlerle birkaç turda mükemmelleştirmek.

### 3. `ConditionalBrancher` (Koşullu Dallandırıcı)
*   **Ne Yapar?** Gelen bir soruyu veya görevi önce sınıflandırır, sonra bu sınıflandırmaya göre en uygun uzmana yönlendirir. Bir santral operatörü gibi davranır.
*   **Örnek Kullanım:** "Kuantum bilgisayarları nasıl çalışır?" gibi bir soruyu "teknik açıklama" dalına, "İklim değişikliği nedir?" sorusunu ise "basit açıklama" dalına yönlendirerek her soruya en uygun cevabın verilmesini sağlamak.

### 4. `SelfCritique` (Kendi Kendini Eleştirme)
*   **Ne Yapar?** Modelden tek bir seferde üç adımlı bir cevap istenir: 1) İlk cevabı yaz. 2) Kendi cevabını eleştir (hataları, eksikleri bul). 3) Eleştirine göre nihai ve düzeltilmiş cevabı yaz. Bu, daha düşünülmüş ve doğru cevaplar üretir.
*   **Örnek Kullanım:** Tarihi bir olay hakkında bilgi istenirken, modelin hem bilgiyi sunması hem de sunduğu bilgideki olası eksiklikleri veya yanlılıkları kontrol edip daha dengeli bir nihai cevap vermesi.

### 5. `ExternalValidation` (Harici Doğrulama)
*   **Ne Yapar?** Modelin ürettiği bir çıktının doğruluğunu, modelin kendisi dışında bir kaynağa veya araca sorarak teyit eder. Eğer çıktı testi geçemezse, neden geçemediği bilgisiyle birlikte modele geri gönderilir ve düzeltmesi istenir.
*   **Örnek Kullanım:** Modelden bir Python fonksiyonu yazmasını istemek, ardından bu kodun gerçekten çalışıp çalışmadığını bir Python derleyicisi ile test etmek. Eğer kodda bir `SyntaxError` (yazım hatası) varsa, bu hatayı modele bildirerek kodu düzeltmesini sağlamak.

## Önemli Çıkarımlar

Bu rehber, LLM'leri basit birer "cevap makinesi" olarak görmekten, onları karmaşık iş akışlarının bir parçası olarak yönetmeye geçişi temsil eder. Temel dersler şunlardır:

*   **Görevleri Ayrıştırma:** Karmaşık bir görevi daha küçük, yönetilebilir adımlara bölmek, daha güvenilir sonuçlar üretir.
*   **Geri Bildirim Döngüleri:** Kendi kendini düzelten ve iyileştiren sistemler, statik sistemlerden çok daha güçlüdür.
*   **Doğrulama:** Modelin cevaplarının doğruluğunu varsaymak yerine, hem modelin kendi içinde hem de harici araçlarla doğrulamak kritik öneme sahiptir.
*   **Orkestrasyon:** Farklı kontrol döngülerini birleştirerek, son derece sofistike ve akıllı otomasyon sistemleri oluşturmak mümkündür.