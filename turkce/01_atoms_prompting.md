# Atomlar: Prompting'in Temel Birimi (Türkçe Özet)

Bu doküman, `00_foundations/01_atoms_prompting.md` dosyasının Türkçe bir özetidir.

> "Eğer sıfırdan bir elmalı turta yapmak istiyorsanız, önce evreni icat etmelisiniz." — Carl Sagan

## Atom: Tek Bir Talimat

Bağlam mühendisliği yolculuğumuza en temel birimle başlıyoruz: **atom**. Atom, bir Yapay Zeka Dil Modeli'ne (LLM) verilen tek ve bağımsız bir talimattır.

```
┌───────────────────────────────────────────────┐
│                                               │
│  "Okyanus hakkında 4 satırlık bir şiir yaz."   │
│                                               │
└───────────────────────────────────────────────┘
```

Bu, en saf haliyle prompt mühendisliğidir: bir insan, bir talimat, bir model yanıtı. Basit, doğrudan ve atomik.

## Atomik Bir Prompt'un Anatomisi

Etkili bir atomik prompt'u oluşturan temel bileşenler şunlardır:

`ATOMİK PROMPT = [GÖREV] + [KISITLAMALAR] + [ÇIKTI FORMATI]`

Örneğin:

| GÖREV | KISITLAMALAR | ÇIKTI FORMATI |
|---|---|---|
| "Bir şiir yaz" | "okyanus hakkında" | "4 satırda." |

## Atomların Sınırlılıkları

Atomik prompt'lar, LLM etkileşimlerinin yapı taşları olsalar da, hızla temel sınırlılıklarını ortaya çıkarırlar:

*   **Etkileşimler arasında hafıza yoktur:** Her prompt bir öncekinden bağımsızdır.
*   **Sınırlı gösterim yeteneği:** Örneklerle öğretmek zordur.
*   **Karmaşık akıl yürütme iskeleleri yoktur:** Adım adım düşünmeyi teşvik etmez.
*   **Belirsizliğe yatkındır:** Model, niyeti yanlış anlayabilir.
*   **Çıktılarda yüksek değişkenlik:** Aynı prompt'a her seferinde farklı yanıtlar alınabilir.

Bu değişkenlik, aynı prompt'u birden çok kez çalıştırdığınızda bile modelin tutarlı sonuçlar üretmekte zorlandığını gösterir. Minimal bağlam, tutarsızlığa yol açar.

## Tek Atomlu Temel Çizgi: Faydalı Ama Sınırlı

Sınırlılıklarına rağmen, atomik prompt'lar bizim için bir **başlangıç noktası** oluşturur. Bu sayede şunları yapabiliriz:

1.  Token verimliliğini ölçebiliriz (en az ek maliyet).
2.  Yanıt kalitesini kıyaslayabiliriz.
3.  Deneyler için bir kontrol grubu oluşturabiliriz.

## Söylenmemiş Bağlam: Modellerin Zaten "Bildiği" Şeyler

Atomik bir prompt'ta bile, LLM'ler eğitim verilerinden gelen devasa bir **örtük bağlamdan** yararlanır (dil kuralları, genel kültür bilgisi, formatlama gelenekleri vb.). Ancak bu örtük bilgi güvenilir değildir ve modelden modele değişir.

## Güç Yasası: Token-Kalite Eğrisi

Çoğu görevde, bağlama eklenen token sayısı ile çıktının kalitesi arasında bir **güç yasası ilişkisi** gözlemlenir. Kritik nokta şudur: Az sayıda token eklemenin kaliteyi önemli ölçüde artırdığı bir "maksimum yatırım getirisi (ROI) bölgesi" vardır. Bu bölgeyi bulmak, bağlam mühendisliğinin hedeflerindendir.

## Atomlardan Moleküllere: Daha Fazla Bağlama Duyulan İhtiyaç

Atomların sınırlılıkları bizi doğal olarak bir sonraki adıma götürür: **moleküller**. Moleküller, talimatları örnekler, ek bağlam ve yapılandırılmış formatlarla birleştiren çok parçalı prompt'lardır.

İşte temel geçiş:

**Atomik Prompt:** `"Bir programcı hakkında bir limerik (kısa, esprili şiir) yaz."`

**Moleküler Prompt:** `"İşte bir örnek: Bir zamanlar bir... Şimdi bir programcı hakkında bir limerik yaz."`

Örnekler ve yapı ekleyerek, bağlam penceresini kasıtlı olarak şekillendirmeye başlarız. Bu, bağlam mühendisliğine atılan ilk adımdır.

## Önemli Çıkarımlar

1.  **Atomik prompt'lar**, LLM etkileşiminin temel birimidir.
2.  Temel bir yapıları vardır: görev + kısıtlamalar + çıktı formatı.
3.  Hafıza, örnekler ve akıl yürütme iskeleleri gibi doğal sınırlılıkları vardır.
4.  Atomların ötesine geçmek, bağlam mühendisliğine doğru atılan ilk adımdır.

## Sonraki Adımlar

Bir sonraki bölümde, atomları birleştirerek **molekülleri** nasıl oluşturacağımızı keşfedeceğiz. Bu moleküller, güvenilirliği ve kontrolü önemli ölçüde artıran "few-shot learning" (az örnekle öğrenme) kalıplarıdır.
