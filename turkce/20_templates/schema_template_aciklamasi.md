# Şablon: Kapsamlı Bağlam Şeması (JSON) - Türkçe Açıklama

Bu doküman, `20_templates/schema_template.json` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu JSON dosyası, bu projede tanıtılan neredeyse tüm bağlam mühendisliği kavramlarını tek bir **kapsamlı ana şema** altında birleştiren, son derece detaylı ve yapılandırılmış bir şablondur.

## Şablonun Amacı

Bu şablon, bir LLM (Büyük Dil Modeli) ile kurulabilecek en karmaşık ve kontrol edilebilir etkileşimler için bir "beyin haritası" veya "yapılandırma dosyası" görevi görür. Amacı, bir LLM ajanının veya uygulamasının davranışını, bilgisini, hafızasını, görevlerini, güvenlik protokollerini ve hatta düşünce süreçlerini tek bir yerden yönetmek için standart bir yapı sunmaktır.

`minimal_context.yaml` şablonu basit etkileşimler için bir başlangıç noktası sunarken, bu JSON şablonu, projenin tüm felsefesini yansıtan, gelişmiş ve bütünleşik bir sistem kurmak için bir plan sunar.

## Şablonun Yapısı ve Ana Bileşenleri

Bu JSON şablonu, bir LLM sisteminin farklı katmanlarını temsil eden çok sayıda anahtar içerir:

### 1. `systemContext` (Sistem Bağlamı)
*   **Ne İşe Yarar?** Modelin temel kimliğini, amacını, kısıtlamalarını ve genel iletişim stilini (örneğin, profesyonel, samimi) tanımlar.

### 2. `domainKnowledge` (Alan Bilgisi)
*   **Ne İşe Yarar?** Modele, belirli bir konu alanı hakkında özel bilgi yükler. Bu, modelin genel bilgisinin ötesinde, belirli bir alanda uzmanlaşmasını sağlar. Kavramlar, önemli gerçekler ve kaynaklar gibi bilgiler içerir.

### 3. `userContext` (Kullanıcı Bağlamı)
*   **Ne İşe Yarar?** Etkileşimde bulunulan kullanıcının profilini, tercihlerini, hedeflerini ve konu hakkındaki ön bilgisini tanımlar. Bu, modelin cevabını kullanıcıya özel olarak uyarlamasına olanak tanır.

### 4. `taskContext` (Görev Bağlamı)
*   **Ne İşe Yarar?** O anki spesifik görevi tanımlar. Görevin türü, konusu, gereksinimleri (örneğin, uzunluk, format) ve başarı kriterleri gibi detayları içerir.

### 5. `interactionHistory` (Etkileşim Geçmişi)
*   **Ne İşe Yarar?** Sadece geçmiş konuşmaları değil, aynı zamanda bu konuşmalardan çıkarılan önemli içgörüleri ve çözülmemiş konuları da saklayarak daha akıllı bir hafıza yönetimi sağlar.

### 6. `neuralFieldContext` (Nöral Alan Bağlamı)
*   **Ne İşe Yarar?** Projenin ileri düzey "Nöral Alan" teorisini yapılandırır. Alanın ana fikirlerini (`attractors`), o anki metriklerini (`stability`, `coherence`) ve işleme sırasında ortaya çıkan yan ürünleri (`residue`) içerir.

### 7. `protocolShell` (Protokol Kabuğu)
*   **Ne İşe Yarar?** Görevi tamamlamak için izlenecek adımları (`process`) tanımlayan bir akıl yürütme protokolü içerir. Bu, modelin düşünce sürecini yapılandırır.

### 8. `responseGuidelines` (Cevap Yönergeleri)
*   **Ne İşe Yarar?** Üretilecek cevabın yapısını, formatını ve tonunu çok detaylı bir şekilde belirler. Hangi bölümlerin dahil edileceği, madde imlerinin nerede kullanılacağı gibi kuralları içerir.

### 9. `cognitiveTools` (Bilişsel Araçlar)
*   **Ne İşe Yarar?** Modelin kullanabileceği düşünme araçlarını tanımlar. Örneğin, bir problemi çözerken "adım adım düşünme" aracını veya bir karar verirken "artı-eksi analizi" aracını kullanmasını sağlar.

### 10. `security` (Güvenlik)
*   **Ne İşe Yarar?** Modelin içerik politikalarını, veri koruma kurallarını ve genel güvenlik yönergelerini tanımlar. Bu, sistemin sorumlu ve güvenli bir şekilde çalışmasını sağlar.

### 11. `fieldExtensions` ve `recursivePatterns` (Alan ve Özyineli Uzantılar)
*   **Ne İşe Yarar?** Nöral alanların ve özyineli kendi kendini iyileştirme mekanizmalarının daha detaylı teknik parametrelerini yapılandırır.

## Nasıl Kullanılır?

Bu JSON şablonu, bir LLM uygulamasının beyni olarak tasarlanmıştır. Bir Python programı:

1.  Bu JSON dosyasını yükleyerek sistemin tüm yapılandırmasını alır.
2.  Kullanıcıdan bir istek geldiğinde, bu şablonun ilgili bölümlerini (örneğin, `userContext`, `taskContext`) günceller.
3.  Şablondaki tüm bu bilgileri bir araya getirerek LLM için son derece zengin ve yapılandırılmış bir bağlam (komut) oluşturur.
4.  LLM'den gelen cevabı, yine bu şablondaki `responseGuidelines` ve `security` gibi kurallara göre değerlendirir ve işler.

Bu şablon, basit bir komut göndermekten, bir LLM'in tüm davranışsal, bilişsel ve operasyonel parametrelerini tasarlamaya ve yönetmeye geçişi temsil eder.