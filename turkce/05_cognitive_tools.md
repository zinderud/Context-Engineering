sorma# Bilişsel Araçlar: Bağlam Mühendisliği Çerçevesini Genişletmek (Türkçe Özet)

Bu doküman, `00_foundations/05_cognitive_tools.md` dosyasının Türkçe bir özetidir.

> "Zihin, doldurulacak bir kap değil, tutuşturulacak bir ateştir." — Plutarch

## Biyolojiden Bilişe

Bağlam mühendisliği yolculuğumuz şu ana kadar biyolojik bir metaforu takip etti: `Atomlar → Moleküller → Hücreler → Organlar`. Şimdi bu çerçeveyi, insan bilişiyle paralellikler kurarak genişletiyoruz. Tıpkı insan zihninin bilgiyi verimli bir şekilde işlemek için bilişsel araçlar kullanması gibi, LLM'ler için de benzer yapılar oluşturabiliriz.

Bu bölümde, LLM'lerin yeteneklerini artıran üç temel bilişsel araç tanıtılmaktadır:

1.  **Prompt Programları / Protokolleri (Prompt Programs / Protocols)**
2.  **Bağlam Şemaları (Context Schemas)**
3.  **Yinelemeli Prompting (Recursive Prompting)**

Bu araçlar, özellikle IBM Zürih tarafından yapılan ve "bilişsel araçların" bir dil modelinin problem çözme performansını önemli ölçüde artırdığını gösteren son araştırmalara dayanmaktadır.

## 1. Prompt Programları: LLM'ler için Algoritmik Düşünme

Bir **prompt programı**, bir LLM'in akıl yürütme sürecine rehberlik etmek için tasarlanmış, yapılandırılmış ve yeniden kullanılabilir bir prompt kalıbıdır. Tıpkı insanların karmaşık sorunları basitleştirmek için kullandığı zihinsel kısayollar (sezgisel yöntemler) gibi çalışır.

**Rastgele (Ad-hoc) Prompt Yerine Programatik Yaklaşım:**

*   **Rastgele Prompt:** `"Bu makaleyi 3 paragrafta özetle. Anlaşılması kolay olsun."`
*   **Prompt Programı:** Parametreler (paragraf sayısı, karmaşıklık seviyesi), süreç adımları (ana konuyu belirle, organize et, özetle) ve çıktı formatı gibi yapılandırılmış bileşenler içerir.

Bu yaklaşım; **yeniden kullanılabilirlik, parametreleştirme, şeffaflık ve tutarlılık** gibi avantajlar sunar.

**Protokol Kabukları (Protocol Shells):** Prompt programlarının daha yapılandırılmış bir halidir. `niyet`, `girdi`, `süreç` ve `çıktı` gibi bölümlerle hem insan hem de yapay zeka için net bir iletişim çerçevesi oluşturur.

## 2. Bağlam Şemaları: Yapılandırılmış Bilgi Kalıpları

Tıpkı insan zihninin bilgiyi düzenlemek için şemalar (örneğin, bir "restoran" şeması; menü, garson, masa gibi kavramları içerir) kullanması gibi, LLM'ler için de **bağlam şemaları** oluşturabiliriz. Bunlar, bilgiyi modelin anlamasını kolaylaştırmak için standartlaştırılmış JSON veya YAML gibi formatlardır.

Bir şema kullanarak prompt oluşturmak, modele tam olarak hangi bilginin sağlandığını ve karşılığında ne beklendiğini net bir şekilde anlatır. Bu, belirsizliği azaltır ve daha güvenilir sonuçlar üretir.

## 3. Yinelemeli Prompting: Kendi Kendini Geliştiren Döngüler

Yinelemeli prompting, modelin kendi çıktıları üzerinde düşünmesini ve onları iyileştirmesini sağlayarak bir geri bildirim döngüsü oluşturma tekniğidir. Bu, insanın kendi düşüncesini eleştirip rafine etmesine (bilişsel yansıma) benzer.

**Basit Akış:**

1.  **İlk Yanıt:** Model, soruya bir ilk yanıt üretir.
2.  **Kendi Üzerine Düşünme (Self-Reflection):** Modele, kendi yanıtını eleştirmesi için bir prompt verilir ("Bu yanıtta eksik ne var? Nasıl daha net olabilir?").
3.  **İyileştirilmiş Yanıt:** Model, bu eleştirilere dayanarak daha iyi bir yanıt üretir.

Bu basit döngü bile, modelin daha derinlemesine düşünmesini teşvik ederek yanıt kalitesini önemli ölçüde artırabilir.

## Hepsini Birleştirmek: Bilişsel Mimari

Bu bilişsel araçlar (programlar, şemalar, yineleme), insan düşünce süreçlerini taklit eden eksiksiz bir **bilişsel mimari** oluşturmak için birleştirilebilir. Böyle bir sistemde:

*   **Girdi Ayrıştırıcı:** Kullanıcının niyetini bir şema kullanarak anlar.
*   **Prompt Programı Seçici:** Göreve en uygun akıl yürütme kalıbını seçer.
*   **Yinelemeli İşlemci:** Kendi kendine yansıtma yoluyla kendini geliştirir.
*   **Çıktı Formatlayıcı:** Nihai yanıtı istenen şemaya göre biçimlendirir.

## Önemli Çıkarımlar

1.  **Prompt Programları/Protokolleri**, insan sezgileri gibi akıl yürütmeyi yapılandırır.
2.  **Bağlam Şemaları**, zihinsel bilgi yapıları gibi bilgiyi organize eder.
3.  **Yinelemeli Prompting**, bilişsel yansıma gibi kendi kendini geliştirme döngüleri oluşturur.
4.  Bu araçların birleşimi, LLM'lerle daha karmaşık ve güçlü sistemler kurmamızı sağlayan **Bilişsel Mimarileri** oluşturur.

## Sonraki Adımlar

Bir sonraki bölümlerde, bu bilişsel araçların pratik uygulamalarını inceleyeceğiz.
