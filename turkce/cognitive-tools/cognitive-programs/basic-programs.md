# Temel Bilişsel Programlar

Bu belge, "Bilişsel Programların" temellerini ve basit uygulamalarını açıklar. Bilişsel programlar, dil modellerini (LLM) yönlendirmek için kullanılan, yeniden kullanılabilir ve yapılandırılmış istem (prompt) kalıplarıdır. Ancak bunlar statik şablonlardan daha fazlasıdır; daha esnek ve güçlü akıl yürütme çerçeveleri oluşturmak için programlama dillerindeki temel kavramları (fonksiyonlar, koşullar, döngüler) kullanırlar.

## Bilişsel Programların Temel Kavramları

1.  **Fonksiyonlar ve Parametreler:**
    *   Her bilişsel program, `analiz_et(konu, derinlik)` gibi bir "fonksiyon" olarak düşünülebilir.
    *   Bu fonksiyonlar, görevi özelleştirmek için `konu` ve `derinlik` gibi "parametreler" alır. Bu, aynı programın farklı girdilerle farklı sonuçlar üretmesini sağlar.

2.  **Koşullu Mantık (If/Else):**
    *   Programın, gelen girdinin özelliğine göre farklı davranmasını sağlar.
    *   Örneğin, bir problem çözücü program, problemin "matematiksel" olduğuna karar verirse farklı, "mantıksal" olduğuna karar verirse farklı bir çözüm yolu izleyebilir.

3.  **Döngüler ve Yineleme (Loops):**
    *   Bir işlemin birden çok kez tekrarlanmasını sağlar.
    *   Örneğin, bir konuyu "ekonomik", "sosyal" ve "politik" gibi birden fazla perspektiften analiz etmek için bir döngü kullanılabilir.

4.  **Fonksiyon Kompozisyonu:**
    *   Basit bilişsel programları birleştirerek daha karmaşık iş akışları oluşturmaktır.
    *   Örneğin, bir `araştırma_yap` programı ile bir `analiz_et` programını birleştirerek, önce araştırma yapan sonra da bulgularını analiz eden bir `araştır_ve_analiz_et` programı oluşturulabilir.

## Temel Bilişsel Program Şablonları

Bu belgede, yukarıdaki kavramları kullanan üç temel program sunulmaktadır:

1.  **Problem Çözücü Programı:**
    *   **Amaç:** Herhangi bir yapılandırılmış problemi çözmek için genel bir çerçeve sunar.
    *   **Özellikler:** Problemin türünü (matematiksel, mantıksal vb.) otomatik olarak algılayabilir ve çözüm yaklaşımını buna göre uyarlayabilir. Çözüm adımlarını gösterme veya gizleme, detay seviyesini ayarlama gibi seçenekler sunar.

2.  **Adım Adım Akıl Yürütme Programı:**
    *   **Amaç:** Bir problemi, önceden tanımlanmış veya dinamik olarak oluşturulmuş adımlarla çözmek için modeli yönlendirir.
    *   **Özellikler:** Standart adımlar (Anla, Planla, Uygula, Doğrula) sunar ancak bu adımlar göreve özel olarak değiştirilebilir.

3.  **Karşılaştırmalı Analiz Programı:**
    *   **Amaç:** İki veya daha fazla öğeyi, belirli kriterlere göre sistematik olarak karşılaştırmak.
    *   **Özellikler:** Analizin çıktısını tablo, anlatı veya artı/eksi listesi gibi farklı formatlarda üretebilir. Karşılaştırma kriterleri özelleştirilebilir.

Bu temel programlar, bilişsel şablonları bir sonraki seviyeye taşıyarak, yapay zekaya daha dinamik, uyarlanabilir ve güçlü akıl yürütme yetenekleri kazandırmanın ilk adımını oluşturur.
