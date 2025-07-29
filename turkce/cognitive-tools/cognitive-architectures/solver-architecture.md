# Bilişsel Çözücü Mimarisi

Bu belge, yapay zekanın karmaşık problemleri çözme yeteneğini sistematik olarak geliştirmek için tasarlanmış bütünsel bir "Bilişsel Çözücü Mimarisi" sunar. Bu mimari, yapay zekanın sadece bir cevap üretmesini değil, aynı zamanda **nasıl düşündüğünün farkında olmasını, stratejisini duruma göre ayarlamasını ve deneyimlerinden öğrenmesini** hedefler.

## Mimarinin Temel Yapısı

Mimari, bir problemi dört temel aşamada ele alan bir iş akışı üzerine kuruludur:
1.  **Anlama:** Problemin ne olduğunu ve neyin istendiğini derinlemesine kavrama.
2.  **Analiz:** Problemi yapısal olarak inceleme ve en uygun çözüm yaklaşımını belirleme.
3.  **Çözme:** Belirlenen yaklaşımı adım adım uygulama.
4.  **Doğrulama:** Elde edilen çözümün doğruluğunu ve tüm gereksinimleri karşılayıp karşılamadığını kontrol etme.

Bu iş akışını destekleyen üç ana katman vardır:

### 1. Bilişsel Araçlar Kütüphanesi
*   **Nedir?** Her bir problem çözme aşaması için tasarlanmış, yeniden kullanılabilir "düşünme araçları" koleksiyonudur.
*   **Örnek Araçlar:** `problemi_anla`, `problemi_ayrıştır`, `adım_adım_çöz`, `çözümü_doğrula` gibi modüler fonksiyonlar.

### 2. Protokol Kabuğu Orkestrasyonu
*   **Nedir?** Belirli bir problemi çözmek için Bilişsel Araçlar Kütüphanesi'ndeki doğru araçları seçen, onları doğru sırayla çalıştıran ve aralarındaki bilgi akışını yöneten bir "orkestra şefi" gibidir.

### 3. Üst-Bilişsel (Meta-Cognitive) Katman
*   **Nedir?** Tüm problem çözme sürecini "dışarıdan" gözlemleyen, denetleyen ve ondan öğrenen en üst düzey katmandır. Bu, mimarinin "kendi kendinin farkında" olmasını sağlar.
*   **İşlevleri:**
    *   **İzleme (Monitor):** "Şu anki stratejim işe yarıyor mu? Bir engele takıldım mı?" gibi soruları sorarak süreci izler.
    *   **Düzenleme (Regulate):** Eğer bir strateji işe yaramıyorsa, "Farklı bir yaklaşım denemeliyim" diyerek planı dinamik olarak değiştirir.
    *   **Yansıtma (Reflect):** "Bu problemden ne öğrendim? Gelecekte benzer bir problemi nasıl daha iyi çözebilirim?" diyerek tamamlanan süreçten ders çıkarır ve kendini geliştirir.

## Alan Teorisi Entegrasyonu

Bu mimari, bağlamı (context) sürekli ve dinamik bir "anlamsal alan" olarak modelleyen Alan Teorisi ile daha da güçlendirilebilir. Bu sayede sistem, bir problem alanındaki "çekicileri" (yani, kararlı ve muhtemel çözüm kalıplarını) tespit edebilir ve çözümünü bu kalıplara doğru "çekerek" daha verimli ve tutarlı hale getirebilir.

## Sonuç

Bilişsel Çözücü Mimarisi, yapay zekayı basit bir "cevap makinesi" olmaktan çıkarıp, kendi düşünme sürecini yönetebilen, hatalarından öğrenebilen ve zamanla daha iyi bir problem çözücü haline gelen **dinamik ve uyarlanabilir bir sisteme** dönüştürür.
