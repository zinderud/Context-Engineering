# Şablon: Kapsamlı Bağlam Şeması (YAML) - Türkçe Açıklama

Bu doküman, `20_templates/schema_template.yaml` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu YAML dosyası, bir önceki `schema_template.json` şablonu ile **aynı yapı ve içeriğe** sahiptir, ancak verileri temsil etmek için JSON yerine **YAML (YAML Ain't Markup Language)** formatını kullanır.

## Şablonun Amacı ve Farkı

Bu şablonun amacı, JSON versiyonuyla tamamen aynıdır: Bir LLM (Büyük Dil Modeli) uygulamasının tüm davranışsal, bilişsel ve operasyonel parametrelerini tek bir yapılandırılmış "ana şema" altında toplamaktır.

İki dosya arasındaki **tek fark formattır**. YAML'ın temel avantajları şunlardır:

*   **Daha İyi Okunabilirlik:** YAML, süslü parantezler `{}` ve köşeli parantezler `[]` yerine girintileme (indentation) ve daha az noktalama işareti kullanır. Bu, şablonun insanlar tarafından okunmasını ve düzenlenmesini genellikle daha kolay hale getirir.
*   **Yorum Satırları:** YAML, `#` işareti ile yorum satırları eklemeye izin verir. Bu şablonda da görüldüğü gibi, her bir bölümün ve alanın ne işe yaradığını açıklayan yorumlar doğrudan dosyanın içine eklenebilir. Bu, şablonun kendi kendini belgelemesini sağlar.

## Şablonun Yapısı

Şablonun yapısı, JSON versiyonuyla birebir aynıdır ve aşağıdaki ana bileşenleri içerir:

1.  **`schema` (Şema Üst Verisi):** Şablonun kendisi hakkında temel bilgiler.
2.  **`system` (Sistem Bağlamı):** LLM'in rolü, amacı ve genel davranış kuralları.
3.  **`domain` (Alan Bilgisi):** Modele yüklenecek özel uzmanlık bilgileri.
4.  **`user` (Kullanıcı Bağlamı):** Kullanıcının profili, hedefleri ve tercihleri.
5.  **`task` (Görev Bağlamı):** O anki spesifik görevin gereksinimleri.
6.  **`history` (Etkileşim Geçmişi):** Önceki konuşmalar ve çıkarımlar.
7.  **`neural_field` (Nöral Alan Bağlamı):** Alan dinamiği parametreleri.
8.  **`protocol` (Protokol Kabuğu):** İzlenecek akıl yürütme adımları.
9.  **`response` (Cevap Yönergeleri):** Üretilecek cevabın detaylı formatı ve stili.
10. **`cognitive_tools` (Bilişsel Araçlar):** Modelin kullanabileceği düşünme çerçeveleri.
11. **`security` (Güvenlik):** İçerik ve veri koruma politikaları.
12. **`customization` (Özelleştirme):** Şablonun hangi bölümlerinin zorunlu veya isteğe bağlı olduğu.

(Her bir bölümün detaylı açıklaması için `turkce/20_templates/schema_template_aciklamasi.md` dosyasına bakabilirsiniz.)

## Nasıl Kullanılır?

Bu YAML şablonu, tıpkı JSON versiyonu gibi, bir Python programı tarafından okunarak kullanılır. Tek fark, `json` kütüphanesi yerine `PyYAML` gibi bir YAML ayrıştırıcı kütüphane kullanılmasıdır.

1.  Python kodunuzda `PyYAML` kütüphanesini kullanarak bu dosyayı yükleyin.
2.  Yüklenen veriyi bir Python sözlüğü (dictionary) olarak ele alın.
3.  Gereken bölümleri güncelleyerek LLM için zengin bir bağlam oluşturun ve LLM'i çağırın.

Özetle, bu şablon, kapsamlı bağlam yapılandırması için JSON'a göre daha okunabilir ve kendini daha iyi belgeleyen bir alternatif sunar.