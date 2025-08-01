# Bağlam Mühendisliği (Context Engineering) - Türkçe Özet

Bu doküman, `Context-Engineering` projesinin ana `README.md` dosyasının Türkçe bir özetidir.

## Ana Fikir: Bağlam Mühendisliği Nedir?

**Bağlam Mühendisliği**, Andrej Karpathy'nin tanımıyla, "bir sonraki adım için bağlam penceresini (context window) tam olarak doğru bilgiyle doldurma sanatı ve bilimidir."

Bu alan, "Prompt Mühendisliği"nin (Prompt Engineering) bir adım ötesine geçer:

*   **Prompt Mühendisliği**: Modele ne söylediğinizdir (tek bir talimat).
*   **Bağlam Mühendisliği**: Modelin gördüğü diğer her şeydir (örnekler, hafıza, araçlar, durum bilgisi, kontrol akışı vb.).

Bu proje, bağlam tasarımı, düzenlemesi ve optimizasyonu için temel prensiplere dayanan bir el kitabı sunar.

## Projenin Yapısı ve Felsefesi

Proje, öğrenme sürecini biyolojik bir metafor üzerinden yapılandırır:

`atomlar → moleküller → hücreler → organlar → sinir sistemleri → sinirsel & anlamsal alan teorisi`

Bu yapı, en temel birim olan tekil komutlardan (atomlar) başlayarak, giderek daha karmaşık ve bütünleşik sistemlere (sinirsel alanlar) doğru ilerleyen bir öğrenme yolu sunar.

### Öğrenme Yolu

Proje, aşağıdaki gibi numaralandırılmış klasörlerle yapılandırılmıştır:

*   `00_foundations`: Temel teoriler ve ilk prensipler.
*   `10_guides_zero_to_hero`: Adım adım pratik rehberler.
*   `20_templates`: Kendi projelerinizde kullanabileceğiniz hazır şablonlar.
*   `30_examples`: Pratik uygulama örnekleri.
*   `40_reference`: Derinlemesine teknik dokümanlar.
*   `60_protocols`: Yapılandırılmış protokoller ve kabuklar (shells).
*   `70_agents`: Örnek ajan (agent) uygulamaları.
*   `cognitive-tools`: Gelişmiş bilişsel çerçeveler.

## Dayandığı Temel Araştırmalar

Bu proje, dil modellerinin yeteneklerini en üst düzeye çıkarmak için yapılan en son bilimsel araştırmalara dayanmaktadır. Öne çıkan bazı temel bulgular şunlardır:

1.  **Bilişsel Araçlar (Cognitive Tools - IBM Zürih):** Karmaşık görevleri, insan uzmanların akıl yürütme şeklini taklit eden daha küçük, yönetilebilir adımlara (araçlara) bölmek, yapay zekanın problem çözme yeteneğini önemli ölçüde artırır. Bu "araçlar", aslında yapılandırılmış prompt şablonlarıdır.

2.  **Beliren Sembolik Mekanizmalar (Emergent Symbolic Mechanisms - ICML Princeton):** Büyük dil modelleri, sadece kelime kalıplarını ezberlemekle kalmaz, aynı zamanda soyut akıl yürütmeyi sağlayan kendi iç "sembolik mantık devrelerini" geliştirirler. Bu, modellerin neden Markdown ve JSON gibi yapılandırılmış verileri daha iyi işlediğini açıklar.

3.  **Hafıza ve Akıl Yürütme Sinerjisi (MEM1 - Singapur-MIT):** Yapay zeka ajanlarına, her adımda hafıza ve akıl yürütmeyi birleştirerek yalnızca önemli olanı saklamayı öğretmek, onları daha verimli ve performanslı hale getirir. Sürekli yeni bağlam eklemek yerine, mevcut durumu özetleyerek günceller.

## Hızlı Başlangıç

1.  **Teoriyi Anlayın:** `00_foundations/01_atoms_prompting.md` dosyasını okuyarak başlayın.
2.  **Deney Yapın:** `10_guides_zero_to_one/01_min_prompt.py` dosyasını çalıştırarak en basit örneği test edin.
3.  **Şablonları İnceleyin:** `20_templates/minimal_context.yaml` dosyasını kendi projeniz için bir başlangıç noktası olarak kullanın.
4.  **Örneği Görün:** `30_examples/00_toy_chatbot/` klasöründeki tam bir uygulamayı inceleyin.

Bu özet, projenin genel bir resmini sunmaktadır. Daha fazla ayrıntı için ana depodaki orijinal dosyalara başvurmanız önerilir.
