# Hücreler: Hafıza ve Durum Eklemek (Türkçe Özet)

Bu doküman, `00_foundations/03_cells_memory.md` dosyasının Türkçe bir özetidir.

> "Biz hafızamızız, o değişken şekillerden oluşan hayali müzeyiz, o kırık aynalar yığınıyız." — Jorge Luis Borges

## Moleküllerden Hücrelere

**Atomları** (tekil talimatlar) ve **molekülleri** (örnekli talimatlar) keşfettik. Şimdi bir üst seviyeye, **hücrelere** çıkıyoruz. Hücreler, birden fazla etkileşim boyunca bilgiyi koruyan, yani **hafızaya** sahip bağlam yapılarıdır.

`HÜCRE = [TALİMATLAR] + [ÖRNEKLER] + [HAFIZA/DURUM] + [MEVCUT GİRDİ]`

Tıpkı çevresiyle etkileşime girerken kendi iç durumunu koruyan biyolojik bir hücre gibi, bizim bağlam "hücrelerimiz" de LLM ile yapılan çoklu alışverişler boyunca bilgiyi muhafaza eder.

## Hafıza Problemi

Varsayılan olarak, LLM'ler hafızasızdır. Her istek bağımsız olarak işlenir. Bu durum, modelin önceki konuşmaları unutmasına ve kopuk bir kullanıcı deneyimine yol açar.

## Hücre Çözümü: Konuşma Hafızası

En basit hücre yapısı, konuşma geçmişini bağlama ekler. Bu sayede LLM, önceki konuşmalara erişebilir ve sürekliliği sağlayabilir.

Örnek:

```
SİSTEM PROMPT'U: "Sen yardımcı bir asistansın..."

KONUŞMA GEÇMİŞİ:
Kullanıcı: "Benim adım Alex."
Asistan: "Merhaba Alex, tanıştığımıza memnun oldum."

Mevcut Girdi: "Benim adım neydi?"
```

Bu bağlamla, model doğru cevabı verebilir: "Adınız Alex."

## Hafıza Token Bütçesi Problemi

Konuşmalar uzadıkça, bağlam penceresi (context window) dolar. Bu nedenle hafıza yönetimi stratejilerine ihtiyaç duyarız. Aksi takdirde, eski bilgileri pencereden atmak zorunda kalırız.

## Hafıza Yönetimi Stratejileri

Sınırlı bağlam pencerelerini optimize etmeye yardımcı olan birkaç strateji vardır:

*   **Pencereleme (Windowing):** Sadece en son N konuşma turunu tutar. Basittir ama eski bilgileri unutur.
*   **Özetleme (Summarization):** Eski konuşmaları özetleyerek sıkıştırır. Ana bilgiyi korurken token sayısını azaltır.
*   **Anahtar-Değer Depolama (Key-Value Storage):** Önemli gerçekleri (kullanıcı adı, tercihler vb.) ayrı bir yapıda saklar. Hassas kontrol sağlar.
*   **Harici Depolama (External Memory):** Gerçekten kalıcı hafıza için bilgiyi harici bir veritabanında (örn: Vector DB) saklar. Bu, potansiyel olarak sınırsız hafıza sağlar.

## Konuşmanın Ötesinde: Durum Bilgisine Sahip Uygulamalar

Hücreler, sadece tutarlı sohbetlerden çok daha fazlasını mümkün kılar. LLM'in şunları yapabildiği **durum bilgisine sahip (stateful)** uygulamalara olanak tanır:

1.  Önceki etkileşimleri hatırlama.
2.  Değişkenleri güncelleme ve sürdürme.
3.  Çok adımlı süreçlerdeki ilerlemeyi izleme.
4.  Önceki çıktıların üzerine inşa etme.

Örneğin, durumu koruyan bir hesap makinesi asistanı, her adımda ara toplamı hafızasında tutarak sürekli hesaplamalar yapabilir.

## Kendi Kendini Geliştiren Hafıza

Gelişmiş hücreler, LLM'in kendi hafızasını yönetmesine yardımcı olduğu geri bildirim döngüleri oluşturur. LLM, konuşmadan önemli gerçekleri çıkarır, bunları hafızasına ekler ve gerektiğinde günceller. Bu, kendi kendini geliştiren bir hafıza sistemi yaratır.

## Önemli Çıkarımlar

1.  **Hafıza hücreleri**, birden fazla etkileşim boyunca durumu korur.
2.  Konuşmalar uzadıkça **token bütçesi yönetimi** kritik hale gelir.
3.  **Hafıza stratejileri** (pencereleme, özetleme, anahtar-değer) farklı ihtiyaçlar için farklı avantajlar sunar.
4.  **Harici hafıza**, bağlam penceresinin sınırlarının ötesinde kalıcı depolama sağlar.
5.  **Yapılandırılmış durum (structured state)**, basit sohbetlerin ötesinde karmaşık uygulamalara olanak tanır.

## Sonraki Adımlar

Bir sonraki bölümde, birden fazla bağlam hücresinin karmaşık sorunları çözmek için birlikte çalıştığı çoklu ajan sistemleri olan **organları (organs)** keşfedeceğiz.
