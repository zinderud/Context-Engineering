# NOCODE.md: Protokol-Güdümlü Bağlam Yönetimi ve Token Bütçelemesi

> *"Harita bölge değildir, ama iyi bir harita karmaşık araziyi geçmeye yardımcı olabilir."*
>
>
> **— Alfred Korzybski (uyarlanmış)**

## 1. Giriş: Token Optimizasyonu Altyapısı Olarak Protokoller

Protokol-güdümlü token bütçelemesi dünyasına hoş geldiniz - programlama bilgisi olmadan sofistike bağlam yönetimi tekniklerini nasıl kullanacağınızı göstereceğimiz yer. Bu rehber, protokol kabukları, pareto-lang ve fractal.json desenlerini kullanarak programlama bilgisi olmadan token kullanımını nasıl optimize edeceğinizi gösterecek.

**Sokratik Soru**: Hiç bağlam alanınız tükendiği ve kritik bilgilerin tam ihtiyacınız olduğu anda kesildiği durumlarda bulundunuz mu? Yapılandırılmış bir bağlam yaklaşımı bunu nasıl önlemeye yardımcı olabilir?

Dalışa geçmeden önce, neyi başarmaya çalıştığımızı görselleştirelim:

```
Protokol Optimizasyonu Öncesi:
┌─────────────────────────────────────────────────┐
│                                                 │
│  Yapılandırılmamış Bağlam (16K token)          │
│                                                 │
│  ███████████████████████████████████████████    │
│  ███████████████████████████████████████████    │
│  ███████████████████████████████████████████    │
│  ███████████████████████████████████████████    │
│                                                 │
└─────────────────────────────────────────────────┘
  ↓ Genellikle kesintiye, kayıp bilgiye yol açar ↓

Protokol Optimizasyonu Sonrası:
┌─────────────────────────────────────────────────┐
│                                                 │
│  Protokol-Yapılandırılmış Bağlam (16K token)   │
│                                                 │
│  Sistem    Geçmiş   Güncel    Alan       │
│  ████      ████████ ██████    ███        │
│  1.5K      8K       5K        1.5K       │
│                                                 │
└─────────────────────────────────────────────────┘
  ↓ Kasıtlı tahsisat, dinamik optimizasyon ↓
```

Bu rehberde, üç tamamlayıcı yaklaşımı keşfedeceğiz:

1. **Protokol Kabukları**: Bağlamı organize eden yapılandırılmış şablonlar
2. **Pareto-lang**: Bağlam işlemleri için basit, bildirimsel dil
3. **Fractal.json**: Token yönetimi için özyinelemeli, kendi kendine benzer desenler

Her yaklaşım bağımsız olarak kullanılabilir veya güçlü bağlam yönetimi için birleştirilebilir.

## 2. Protokol Kabukları: Temel

### 2.1. Protokol Kabukları Nedir?

Protokol kabukları, bağlam için net bir organizasyonel çerçeve oluşturan yapılandırılmış şablonlardır. Hem insanların hem de AI modellerinin kolayca anlayabileceği tutarlı bir desen izlerler.

```
/protokol.adi{
    niyet="Amacın net ifadesi",
    girdi={...},
    islem=[...],
    cikti={...}
}
```

**Sokratik Soru**: İstemlerinizi bir protokol gibi yapılandırmak, modelin bilginizi nasıl işlemesini nasıl değiştirebilir? Tipik istemlerinizin hangi yönleri daha net yapıdan faydalanabilir?

### 2.2. Temel Protokol Kabuğu Anatomisi

Bileşenleri parçalayalım:

```
┌─────────────────────────────────────────────────────────┐
│                    PROTOKOL KABUĞU                      │
├─────────────────────────────────────────────────────────┤
│ /protokol.adi{                                          │
│                                                         │
│   niyet="Bu protokolün neden var olduğu",               │
│                  ▲                                      │
│                  └── Amaç ifadesi, modeli yönlendirir   │
│                                                         │
│   girdi={                                               │
│     param1="deger1",                                    │
│     param2="deger2"    ◄── Girdi parametreleri/bağlam   │
│   },                                                    │
│                                                         │
│   islem=[                                               │
│     /adim1{eylem="X yap"},   ◄── İşleme adımları        │
│     /adim2{eylem="Y yap"}                               │
│   ],                                                    │
│                                                         │
│   cikti={                                               │
│     sonuc1="beklenen X",    ◄── Çıktı spesifikasyonu    │
│     sonuc2="beklenen Y"                                 │
│   }                                                     │
│ }                                                       │
└─────────────────────────────────────────────────────────┘
```

Bu yapı, etkileşim için token-verimli bir şema oluşturur.

### 2.3. Pratik Örnek: Metin Özetleme Protokolü

İşte basit ama etkili bir metin özetleme protokolü:

```
/ozet.analiz{
    niyet="Uzun metni ana fikirlerini koruyarak özetlemek",
    
    girdi={
        metin="[Özetlenecek metin buraya]",
        uzunluk="orta",        // kısa, orta, uzun
        stil="akademik",       // akademik, günlük, teknik
        hedef_kitle="genel"    // uzman, genel, başlangıç
    },
    
    islem=[
        /okuma{
            eylem="metni ana temalar için tara",
            odak="anahtar argümanlar ve kanıtlar"
        },
        /yapilandirma{
            eylem="bilgiyi hiyerarşik olarak organize et",
            oncelik="kritik noktalar > destekleyici detaylar"
        },
        /sentez{
            eylem="özet oluştur",
            kriter="tutarlılık + bütünlük"
        }
    ],
    
    cikti={
        ozet="yapılandırılmış özet",
        anahtar_noktalar="madde işaretli liste",
        kaybedilen_detaylar="önemli eksik bilgiler"
    }
}
```

**Türkçe Yorum**: Bu protokol, AI'ya sadece "özetle" demek yerine, nasıl özetlemesi gerektiğini detaylı olarak açıklar. Böylece daha tutarlı ve kullanışlı sonuçlar alırız.

### 2.4. Token Verimliliği Faydaları

Protokol kabukları aşağıdaki şekillerde token tasarrufu sağlar:

```
Geleneksel İstem (150+ token):
"Bu metni özetler misin? Ama çok kısa olmasın, ana fikirleri 
kaydetmek istiyorum. Ayrıca önemli detayları da atlama. 
Ve eğer bir şey eksik kalırsa bana söyle. Oh, ve formal 
bir dil kullan çünkü bu akademik bir metin..."

Protokol Kabuğu (95 token):
/ozet.akademik{
    girdi={metin="...", stil="formal"},
    cikti={ozet="ana_fikirler", eksikler="liste"}
}
```

**Verimllik Analizi**:
- %37 token tasarrufu
- Daha net yapı
- Tekrarlanabilir sonuçlar
- Kolay modifikasyon

### 2.5. Gelişmiş Protokol Desenleri

#### 2.5.1. Zincirleme Protokoller

Karmaşık görevler için protokolleri zincirleme yapabilirsiniz:

```
/analiz.belgesi{
    niyet="Çok aşamalı belge analizi",
    
    asamalar=[
        /on_islem{protokol="temizlik.metni"},
        /yapisal_analiz{protokol="icerik.haritasi"},
        /sentment_analiz{protokol="duygu.cikarimi"},
        /ozet{protokol="sonuc.sentezi"}
    ]
}
```

#### 2.5.2. Koşullu Protokoller

Farklı durumlar için farklı işlem yolları:

```
/analiz.uyarlanabilir{
    girdi={
        metin_tipi="otomatik_tespit",
        karmasiklik="dinamik"
    },
    
    kosullar={
        EĞER: metin_tipi=="akademik" 
        O_ZAMAN: /protokol.akademik_analiz{},
        
        EĞER: metin_tipi=="yaratici"
        O_ZAMAN: /protokol.yaratici_analiz{},
        
        VARSAYILAN: /protokol.genel_analiz{}
    }
}
```

**Türkçe Yorum**: Bu yaklaşım, AI'nın farklı metin türlerine uygun stratejiler uygulamasını sağlar, tıpkı deneyimli bir editörün farklı belge türleri için farklı yaklaşımlar benimsemesi gibi.

## 3. Pareto-lang: Basit Ama Güçlü Bağlam Dili

### 3.1. Pareto-lang Nedir?

Pareto-lang, bağlam manipülasyonu için minimalist bir dildir. 80/20 kuralından ilham alır - az sözcükle çok iş yapmak.

**Temel Sözdizimi**:
```
/islem.duzenleyici{parametreler}
```

**Örnek İşlemler**:
```
/kaydet.on_plan{konu="proje_yonetimi"}         // Bilgiyi öne çıkar
/gizle.detay{seviye="teknik"}                  // Gereksiz detayları gizle  
/genislet.ornekler{alan="pazarlama"}           // Örnekleri genişlet
/sıkıştır.gecmis{oran=0.3}                     // Geçmişi %30'a sıkıştır
```

### 3.2. Pratik Pareto-lang Kullanımı

#### Örnek 1: Bellek Yönetimi
```
// Konuşmanın başında
/ayarla.bellek{
    ana_konu="web_tasarimi",
    priori_bilgiler=["html", "css", "kullanici_deneyimi"],
    goz_ardi_et=["sunucu_yonetimi", "veritabani"]
}

// Konuşma sırasında  
/vurgula.kavram{ad="responsive_design", bag="mobil_cihazlar"}
/bagla.ornekler{kavram="responsive_design", tip="kod_parcaciklari"}
```

#### Örnek 2: Dinamik Bağlam Ayarlama
```
// İhtiyaç duyduğunuzda bağlamı ayarlayın
/duzenle.odak{
    onceki="genel_konseptler",
    yeni="spesifik_uygulama",
    gecis="yumusak"
}

/yenile.ornekler{
    eski_alan="teorik",
    yeni_alan="pratik",
    miktar=3
}
```

**Türkçe Yorum**: Pareto-lang, tıpkı bir müze rehberinin galeride hangi eserleri vurgulayıp hangilerini gözardı edeceğini söylemesi gibi, AI'ya bağlamda neye odaklanması gerektiğini net şekilde iletir.

### 3.3. Gelişmiş Pareto-lang Desenleri

#### 3.3.1. Bağlam Temizliği
```
/temizle.gereksiz{
    tur=["tekrar", "alakasiz_detay", "eski_ornekler"],
    koruma_seviyesi="onemli_baglanti"
}

/optimize.token{
    hedef_oran=0.8,           // %20 azaltma hedefi
    oncelik=["ana_fikirler", "ornekler", "arka_plan"]
}
```

#### 3.3.2. Bilgi Katmanlama  
```
/katmanla.bilgi{
    temel_seviye="kavramlar",
    orta_seviye="uygulamalar", 
    ileri_seviye="optimizasyonlar",
    aktif_seviye="orta"
}

// Daha sonra seviye değiştirme
/degistir.seviye{hedef="ileri", gecis="adimli"}
```

Bu yaklaşım tıpkı iyi bir ders kitabının temel, orta ve ileri bölümlerine ayrılması gibi, bilgiyi kullanıcının seviyesine göre düzenler.

## Devam Edecek...

Bu, NOCODE.md dosyasının ilk büyük bölümünün Türkçe çevirisidir. Devam edelim mi?
