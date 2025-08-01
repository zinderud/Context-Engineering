# Rehber 01: Minimum Prompt (En Basit Komut) - Türkçe Açıklama

Bu doküman, `10_guides_zero_to_hero/01_min_prompt.py` dosyasının amacını ve içeriğini Türkçe olarak açıklamaktadır. Bu Python betiği, Bağlam Mühendisliği'nin en temel kavramlarını uygulamalı olarak göstermek için tasarlanmıştır.

## Betiğin Amacı

Bu rehber, teorik bilgileri pratiğe dökmenin ilk adımıdır. `00_foundations` bölümünde öğrenilen "atomik prompt" (tekil komut) kavramını temel alır. Betik, gerçek bir yapay zeka modeline bağlanmak yerine, konsepti göstermek için basit bir simülasyon kullanır. Ana hedefleri şunlardır:

1.  **Atomik Prompt'ları Anlamak:** En basit, tek bir talimattan oluşan komutların nasıl oluşturulduğunu ve çalıştığını göstermek.
2.  **Kısıtlamaların Etkisini Gözlemlemek:** Bir komuta eklenen her yeni kısıtlamanın (örneğin, "4 satırda yaz") çıktıyı nasıl etkilediğini ve token maliyetini nasıl değiştirdiğini göstermek.
3.  **Token-Kalite İlişkisini Ölçmek:** Daha fazla token kullanmanın (daha ayrıntılı komut vermenin) her zaman daha kaliteli bir sonuç üretip üretmediğini keşfetmek. Bu, "yatırımın geri dönüşü" (ROI) eğrisi olarak görselleştirilir.
4.  **Stratejik Bağlamın Gücünü Göstermek:** Çok az ama stratejik olarak doğru eklenmiş bilginin (örneğin, "haiku'nun ne olduğunu açıklamak"), komutun kalitesini ve tutarlılığını nasıl önemli ölçüde artırabildiğini göstermek.

## Betikteki Deneyler

Betiğin içindeki kod, 5 ana deneye ayrılmıştır:

*   **Deney 1: Atomik Prompt:** En temel komut (`"Programlama hakkında kısa bir şiir yaz."`) ve onun token sayısı incelenir. Bu, başlangıç noktamızdır.

*   **Deney 2: Kısıtlama Ekleme:** Aynı komutun farklı versiyonları (uzunluk, format ve kelime kısıtlamaları eklenerek) test edilir. Her birinin token maliyeti ve potansiyel çıktısı karşılaştırılır.

*   **Deney 3: ROI Eğrisini Ölçme:** Komutların token maliyetleri ile varsayımsal kalite puanları karşılaştırılarak bir grafik oluşturulur. Amaç, en az token ile en yüksek kaliteyi elde ettiğimiz "tatlı noktayı" bulmaktır.

*   **Deney 4: Minimal Bağlam Geliştirmesi:** Komuta, görevi daha net hale getiren küçük bir açıklama eklenir (`"Haiku, 5-7-5 hece yapısına sahip üç satırlık bir şiirdir."`). Bu küçük eklemenin, kaliteyi nasıl artırdığı gösterilir.

*   **Deney 5: Tutarlılığı Ölçme:** Basit bir komut ile stratejik olarak geliştirilmiş bir komutun, birden çok kez çalıştırıldığında ne kadar tutarlı sonuçlar ürettiği (varsayımsal olarak) karşılaştırılır.

## Önemli Çıkarımlar

Bu basit rehber, Bağlam Mühendisliği'nin temel derslerini özetler:

*   En iyi komutlar genellikle en uzun olanlar değil, **en net ve stratejik** olanlardır.
*   Komutunuza eklediğiniz her kelimenin bir **maliyeti** (token) ve bir **getirisi** (kalite) vardır.
*   Modelin ne istediğinizi "bildiğini" varsaymak yerine, görevi netleştiren **minimal ama kritik bağlamı** sağlamak, sonuçları önemli ölçüde iyileştirir.

Bu betik, bir sonraki adım olan "moleküler" yani çok parçalı komutlara geçmeden önce sağlam bir temel oluşturur.