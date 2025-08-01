# Bütçe Modeli: Bağlam Kaynaklarını Yönetme

> *“Küçük harcamalara dikkat edin; küçük bir sızıntı büyük bir gemiyi batırır.”*
>
>
> **— Benjamin Franklin**

## 1. Giriş: Bağlam Olarak Ekonomi

Bahçe Modeli bize bağlama organik bir bakış açısı sunarken, Bütçe Modeli tamamlayıcı bir ekonomik mercek sunar. Bu çerçeve, bağlamı, maksimum değer üretmek için dikkatlice tahsis edilmesi, yatırım yapılması ve optimize edilmesi gereken sınırlı kaynaklar sistemi olarak görür.

Bağlam mühendisliği dünyasında, her etkileşimin sınırlı kaynakları vardır:
- **Jetonlar**: Sert sınırlara sahip temel para birimi
- **Dikkat**: Hem insanın hem de yapay zekanın bilişsel bant genişliği
- **İlgililik**: İçeriğin hedeflerle uyumu
- **Tutarlılık**: Bilginin bağlantılılığı ve tutarlılığı
- **Etki**: İstenen sonuçları yaratma gücü

Bütçe Modeli, optimum sonuçlar için bu kaynakları nasıl yöneteceğimizi sistematik olarak düşünmemize yardımcı olur.

**Sokratik Soru**: Kişisel veya kurumsal bütçelemenizi düşünün. Hangi ilkeler en değerli olduğunu kanıtladı? Bu aynı ilkeler yapay zeka etkileşimlerinde bağlamı yönetmeye nasıl uygulanabilir?

```
┌─────────────────────────────────────────────────────────┐
│                BÜTÇE MODELİ                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Kaynaklar        Tahsis        Yatırım Getirisi│
│  ─────────        ──────────        ───────────────────│
│                                                         │
│  Çalışmak için    Nasıl kullandığınız    Yatırımınız için   │
│  sahip olduklarınız     ve önceliklendirdiğiniz    geri aldıklarınız │
│                                                         │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐       │
│  │ Jetonlar    │    │ Stratejik │    │ Kalite    │       │
│  │ Dikkat    │    │ Taktiksel │    │ Verimlilik│       │
│  │ İlgililik │    │ Acil Durum│    │ Etki      │       │
│  │ Tutarlılık│    │ Rezerv    │    │ Öğrenme   │       │
│  └───────────┘    └───────────┘    └───────────┘       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 2. Bütçe Bileşenleri ve Bağlam Paralellikleri

Bütçe Modeli, finansal kavramları doğrudan bağlam mühendisliği öğelerine eşler:

### 2.1. Para Birimi (Jetonlar)

Finansal bütçelemede para birimi temel kaynaktır. Bağlamda:

- **Jeton Sınırları**: Toplam mevcut bütçe
- **Jeton Tüketimi**: Giderler
- **Jeton Verimliliği**: Dolar başına daha fazla değer elde etme
- **Jeton Rezervleri**: Beklenmedik ihtiyaçlar için acil durum fonları

```
/jeton_bütçesi.değerlendir{
    toplam_mevcut=8000,
    mevcut_tüketim=6200,
    verimlilik_puanı=0.85,
    rezerv_politikası="%10 tamponu koru",
    mevcut_rezerv=800,
    durum="parametreler_içinde"
}
```

### 2.2. Gelir ve Giderler (Bilgi Akışı)

Bütçeler gelen ve giden parayı izler. Bağlamda:

- **Bilgi Girdileri**: Gelir kaynakları
- **Çıktı Gereksinimleri**: Sabit giderler
- **İşlem Maliyetleri**: Değişken giderler
- **Kapsam Genişlemesi**: Yaşam tarzı enflasyonu

```
/bilgi_akışı.izle{
    girdiler=[
        {kaynak="kullanıcı sorgusu", boyut="orta", kalite="yüksek", sıklık="aralıklı"},
        {kaynak="sistem talimatları", boyut="büyük", kalite="çok yüksek", sıklık="sabit"},
        {kaynak="geri çağırma", boyut="değişken", kalite="orta", sıklık="gerektiğinde"},
        {kaynak="önceki etkileşimler", boyut="büyüyen", kalite="karışık", sıklık="sürekli"}
    ],
    
    çıktılar=[
        {gereksinim="sorguyu yanıtla", öncelik="yüksek", jeton_tahmini=500},
        {gereksinim="tutarlılığı koru", öncelik="orta", jeton_tahmini=300},
        {gereksinim="örnekler sağla", öncelik="düşük", jeton_tahmini=400}
    ],
    
    işlem_maliyetleri=[
        {işlem="akıl yürütme", yoğunluk="yüksek", jeton_etkisi="dolaylı"},
        {işlem="geri çağırma işleme", yoğunluk="orta", jeton_etkisi="orta"},
        {işlem="bağlam entegrasyonu", yoğunluk="değişken", jeton_etkisi="yüksek"}
    ]
}
```

### 2.3. Varlıklar ve Yükümlülükler (İçerik Değeri)

Finansal sağlık, sahip olduklarınızı borçlu olduklarınıza karşı değerlendirir. Bağlamda:

- **Yüksek Değerli İçerik**: Getiri sağlayan varlıklar
- **Gerekli Ek Yük**: İpotek/temel yükümlülükler
- **Düşük Değerli İçerik**: Kaynakları tüketen borç
- **İçerik Yatırımları**: Gelecekteki getiriler için edinilen varlıklar

```
/içerik_değeri.denetle{
    varlıklar=[
        {tür="çekirdek tanımlar", değer="yüksek", dayanıklılık="uzun vadeli", getiri="anlama temeli"},
        {tür="açıklayıcı örnekler", değer="orta-yüksek", dayanıklılık="orta vadeli", getiri="gelişmiş anlama"},
        {tür="organize yapı", değer="yüksek", dayanıklılık="uzun vadeli", getiri="gelişmiş gezinme ve saklama"}
    ],
    
    yükümlülükler=[
        {tür="gereksiz bilgi", etki="orta düzeyde tüketim", gereklilik="yok", öneri="ortadan kaldır"},
        {tür="konu dışı içerik", etki="hafif tüketim", gereklilik="düşük", öneri="en aza indir"},
        {tür="aşırı detay", etki="önemli tüketim", gereklilik="durumsal", öneri="optimize et"}
    ],
    
    yatırımlar=[
        {tür="temel kavramlar", mevcut_maliyet="orta", beklenen_getiri="yüksek", zaman_çerçevesi="anında ve sürekli"},
        {tür="ilişki kurma", mevcut_maliyet="düşük", beklenen_getiri="yüksek", zaman_çerçevesi="kümülatif"},
        {tür="bağlamsal farkındalık", mevcut_maliyet="orta", beklenen_getiri="yüksek", zaman_çerçevesi="aşamalı"}
    ]
}
```

### 2.4. Finansal Oranlar (Verimlilik Metrikleri)

Oranlar finansal sağlığı değerlendirmeye yardımcı olur. Bağlamda:

- **Bilgi Yoğunluğu**: Jeton başına değer (Yatırım Getirisi)
- **İlgililik Oranı**: Konuyla ilgili yüzde (Kar marjı)
- **Tutarlılık Puanı**: Bağlantılılık (Finansal istikrar)
- **Ek Yük Oranı**: Gerekli ancak dolaylı içerik (İşletme gider oranı)

```
/verimlilik_metrikleri.hesapla{
    bilgi_yoğunluğu={
        formül="sağlanan_değer / kullanılan_jetonlar",
        mevcut_değer=0.82,
        kıyaslama=0.75,
        durum="hedefin_üzerinde"
    },
    
    ilgililik_oranı={
        formül="konuyla_ilgili_jetonlar / toplam_jetonlar",
        mevcut_değer=0.88,
        kıyaslama=0.85,
        durum="hedefin_üzerinde"
    },
    
    tutarlılık_puanı={
        formül="bağlantılılık_ölçümü(tüm_içerik)",
        mevcut_değer=0.79,
        kıyaslama=0.80,
        durum="hedefin_biraz_altında"
    },
    
    ek_yük_oranı={
        formül="destek_içeriği / doğrudan_değer_içeriği",
        mevcut_değer=0.30,
        kıyaslama=0.35,
        durum="hedeften_daha_iyi"
    }
}
```

### 2.5. Bütçe Kategorileri (İçerik Türleri)

Bütçeler harcamaları kategorilere ayırır. Bağlamda:

- **Sistem Talimatları**: Sabit giderler (kira/ipotek)
- **Çekirdek İçerik**: Temel değişken giderler (market/faturalar)
- **Örnekler/Detaylar**: İsteğe bağlı harcamalar (eğlence/dışarıda yeme)
- **Meta-İçerik**: İdari maliyetler (banka ücretleri/sigorta)
- **Rezerv Kapasitesi**: Tasarruflar (acil durum fonu)

```
/bütçe_kategorileri.organize_et{
    sistem_talimatları={
        doğa="sabit temel",
        mevcut_tahsis="%18",
        optimizasyon_potansiyeli="düşük",
        değer_değerlendirmesi="temel"
    },
    
    çekirdek_içerik={
        doğa="değişken temel",
        mevcut_tahsis="%42",
        optimizasyon_potansiyeli="orta",
        değer_değerlendirmesi="doğrudan etki"
    },
    
    örnekler_detaylar={
        doğa="isteğe bağlı",
        mevcut_tahsis="%25",
        optimizasyon_potansiyeli="yüksek",
        değer_değerlendirmesi="geliştirici"
    },
    
    meta_içerik={
        doğa="ek yük",
        mevcut_tahsis="%7",
        optimizasyon_potansiyeli="orta",
        değer_değerlendirmesi="destekleyici"
    },
    
    rezerv_kapasitesi={
        doğa="acil durum fonu",
        mevcut_tahsis="%8",
        optimizasyon_potansiyeli="durumsal",
        değer_değerlendirmesi="risk yönetimi"
    }
}
```

**Düşünme Egzersizi**: Yakın zamandaki bir yapay zeka etkileşimini düşünün. "Bütçesini" nasıl kategorize edersiniz? Hangi kategoriler en çok "harcamayı" aldı? Daha iyi sonuçlar için kaynakları nereye yeniden tahsis edebilirdiniz?

## 3. Bütçeleme Stratejileri

Finansal yönetimde olduğu gibi, bağlam bütçelemesine yönelik farklı yaklaşımlar çeşitli faydalar ve ödünleşimler sunar.

### 3.1. Sıfır Tabanlı Bütçeleme

Sıfırdan başlayın ve her jetonu gerekçelendirin:

```
/sıfır_tabanlı_bütçeleme.uygula{
    yaklaşım={
        felsefe="Her jetonu sıfırdan gerekçelendir",
        sıklık="Her yeni etkileşim",
        titizlik="Tüm öğelerin yüksek düzeyde incelenmesi"
    },
    
    süreç=[
        {adım="Çekirdek sonuçları belirle", açıklama="Tam olarak neyin başarılması gerektiğini tanımla"},
        {adım="Gerekli öğeleri listele", açıklama="Her sonuç için neyin gerekli olduğunu sırala"},
        {adım="Jeton tahsislerini ata", açıklama="Geçmişe değil, gerekçelendirilmiş ihtiyaca göre bütçele"},
        {adım="Her öğeyi incele", açıklama="Gerekliliği ve tahsis boyutunu sorgula"},
        {adım="Optimize et ve sonlandır", açıklama="İncelemeye göre son tahsisleri belirle"}
    ],
    
    faydalar=[
        "Tarihsel israfı ortadan kaldırır",
        "Tüm öğeler hakkında bilinçli kararlar vermeye zorlar",
        "Gerekli olmayan içeriğin otomatik olarak dahil edilmesini önler",
        "Öncelikleri düzenli olarak yeniler"
    ],
    
    zorluklar=[
        "Zaman alıcı süreç",
        "Gereksinimlerin derinlemesine anlaşılmasını gerektirir",
        "İnce karşılıklı bağımlılıkları kaçırabilir",
        "Aşırı kullanılırsa yorucu olabilir"
    ],
    
    en_iyi_kullanım_alanları=[
        "Yeni etkileşim türleri",
        "Maksimum verimlilik gerektiren durumlar",
        "Etkisiz desenlerden çıkma",
        "Yüksek riskli, jeton kısıtlı senaryolar"
    ]
}
```

### 3.2. Zarf Bütçelemesi

Belirli kategorilere önceden jeton tahsis edin:

```
/zarf_bütçelemesi.uygula{
    yaklaşım={
        felsefe="Katı sınırlara sahip kategorilere önceden tahsis et",
        sıklık="Başlangıçta kurulur, boyunca sürdürülür",
        titizlik="Kategoriler arasında sağlam sınırlar"
    },
    
    süreç=[
        {adım="Kategorileri tanımla", açıklama="Açık içerik/işlev kategorileri oluştur"},
        {adım="Jeton bütçelerini tahsis et", açıklama="Her kategoriye belirli jeton miktarları ata"},
        {adım="Tüketimi izle", açıklama="Her kategorideki kullanımı izle"},
        {adım="Sınırları uygula", açıklama="Kategoriler arasında borçlanmayı önle"},
        {adım="Gerektiğinde ayarla", açıklama="Yalnızca kasıtlı kararla yeniden tahsis et"}
    ],
    
    kategoriler=[
        {ad="Sistem talimatları", tahsis="%15", esneklik="Düşük"},
        {ad="Çekirdek açıklama", tahsis="%30", esneklik="Orta"},
        {ad="Örnekler", tahsis="%20", esneklik="Yüksek"},
        {ad="Keşif", tahsis="%25", esneklik="Yüksek"},
        {ad="Meta/Gezinme", tahsis="%5", esneklik="Düşük"},
        {ad="Rezerv", tahsis="%5", esneklik="Sadece acil durum"}
    ],
    
    faydalar=[
        "Kategori kaymasını önler",
        "Açık sorumluluk yaratır",
        "İzlemeyi basitleştirir",
        "Tüm işlevlerin tahsis almasını sağlar"
    ],
    
    zorluklar=[
        "Dinamik durumlar için çok katı olabilir",
        "İyi başlangıç tahsis tahminleri gerektirir",
        "Yapay kısıtlamalar yaratabilir",
        "Düzenli inceleme ve ayarlama gerektirir"
    ],
    
    en_iyi_kullanım_alanları=[
        "Öngörülebilir ihtiyaçlara sahip yapılandırılmış etkileşimler",
        "Birden çok rakip önceliği yönetme",
        "Bağlam disiplinini öğretme",
        "Açık kategori gereksinimleri olan senaryolar"
    ]
}
```

### 3.3. Değer Tabanlı Bütçeleme

Etki ve öneme göre tahsis edin:

```
/değer_tabanlı_bütçeleme.uygula{
    yaklaşım={
        felsefe="Değer katkısına göre tahsis et",
        sıklık="Sürekli önceliklendirme süreci",
        titizlik="Sürekli değer değerlendirmesi"
    },
    
    süreç=[
        {adım="Değer metriklerini tanımla", açıklama="Etkinin nasıl ölçüleceğini belirle"},
        {adım="Öğe katkılarını değerlendir", açıklama="Her öğenin nasıl değer sağladığını değerlendir"},
        {adım="Yatırım Getirisine göre sırala", açıklama="Öğeleri jeton başına getiriye göre sırala"},
        {adım="Aşamalı olarak tahsis et", açıklama="Jetonları önce en yüksek değere ata"},
        {adım="İncele ve optimize et", açıklama="Değer sunumunu düzenli olarak yeniden değerlendir"}
    ],
    
    değer_metrikleri=[
        {metrik="Hedef ilerlemesi", ağırlık=0.4, ölçüm="Birincil hedefe doğru ilerleme"},
        {metrik="Anlama derinliği", ağırlık=0.3, ölçüm="Sağlanan anlama derinliği"},
        {metrik="Çok yönlülük", ağırlık=0.2, ölçüm="Bağlamlar arasında uygulanabilirlik"},
        {metrik="Hatırlanabilirlik", ağırlık=0.1, ölçüm="Hatırlanma olasılığı"}
    ],
    
    faydalar=[
        "Jeton yatırım getirisini en üst düzeye çıkarır",
        "Doğal olarak en önemli olanı önceliklendirir",
        "Düşük değerli öğelerdeki israfı azaltır",
        "Girdi yerine sonuçlara odaklanma yaratır"
    ],
    
    zorluklar=[
        "Açık değer tanımları gerektirir",
        "Değer öznel veya ölçmesi zor olabilir",
        "Temel veya destek öğelerine yetersiz yatırım yapabilir",
        "Değer metriklerinin düzenli olarak yeniden kalibre edilmesini gerektirir"
    ],
    
    en_iyi_kullanım_alanları=[
        "Sonuç odaklı etkileşimler",
        "Açık başarı metrikleri olan durumlar",
        "Kısıtlı jeton ortamları",
        "Etkinin öncelikli olduğu uygulamalar"
    ]
}
```

### 3.4. Artımlı Bütçeleme

Ayarlamalarla önceki tahsislerin üzerine inşa edin:

```
/artımlı_bütçeleme.uygula{
    yaklaşım={
        felsefe="Hedefli ayarlamalarla önceki başarılı tahsislere dayan",
        sıklık="Her yineleme veya benzer etkileşim",
        titizlik="Değişikliklere ve iyileştirmelere odaklanmış"
    },
    
    süreç=[
        {adım="Önceki modelle başla", açıklama="Başarılı geçmiş etkileşimden tahsis kullan"},
        {adım="İyileştirme alanlarını belirle", açıklama="Neyin ayarlanması gerektiğini belirle"},
        {adım="Hedefli değişiklikler yap", açıklama="Belirli artışlar veya azalmalar uygula"},
        {adım="Ayarlamaları test et", açıklama="Değişikliklerin etkisini değerlendir"},
        {adım="Gelecek yineleme için belgele", açıklama="Gelecekteki referans için sonuçları kaydet"}
    ],
    
    ayarlama_türleri=[
        {tür="Genişletme", tetikleyici="Anahtar alanda yetersiz derinlik", yaklaşım="Hedefli artış"},
        {tür="Azaltma", tetikleyici="Düşük değerli aşırı detay", yaklaşım="Hedefli azalış"},
        {tür="Yeniden Tahsis", tetikleyici="Değişen öncelikler", yaklaşım="Kategoriler arasında kaydırma"},
        {tür="Optimizasyon", tetikleyici="Daha azıyla aynı sonuç mümkün", yaklaşım="Verimlilik iyileştirmesi"}
    ],
    
    faydalar=[
        "Kanıtlanmış başarıların üzerine inşa eder",
        "Verimli planlama süreci",
        "Etkileşimler arasında tutarlılığı korur",
        "Kademeli optimizasyona izin verir"
    ],
    
    zorluklar=[
        "Tarihsel verimsizlikleri sürdürebilir",
        "Daha büyük gerekli değişikliklere direnebilir",
        "Değişen ortamlara daha az duyarlı",
        "Zamanla kayıtsız kalabilir"
    ],
    
    en_iyi_kullanım_alanları=[
        "Tekrarlanan etkileşim türleri",
        "Kurulmuş desenleri iyileştirme",
        "Tutarlılık gerektiren durumlar",
        "Yinelemeli iyileştirme süreçleri"
    ]
}
```

**Sokratik Soru**: Mevcut bağlam yönetimi yaklaşımınıza en çok hangi bütçeleme stratejisi uyuyor? Bir sonraki etkileşiminiz için farklı bir strateji denemekten ne kazanabilirsiniz?

## 4. Bağlam Yönetimi için Finansal Disiplinler

Birçok finansal disiplin, güçlü sonuçlar için bağlam mühendisliğine uyarlanabilir.

### 4.1. Yatırım Getirisi Analizi (ROI)

Jeton yatırımınız için ne elde ettiğinizi değerlendirin:

```
/roi_analizi.yap{
    formül="sağlanan_değer / yatırılan_jetonlar",
    
    uygulamalar=[
        {öğe="Ayrıntılı örnek", jetonlar=500, değer_puanı=450, roi=0.9, yorum="İyi yatırım"},
        {öğe="Teknik açıklama", jetonlar=300, değer_puanı=360, roi=1.2, yorum="Mükemmel yatırım"},
        {öğe="Tarihsel bağlam", jetonlar=400, değer_puanı=200, roi=0.5, yorum="Kötü yatırım"},
        {öğe="Adım adım kılavuz", jetonlar=600, değer_puanı=660, roi=1.1, yorum="Güçlü yatırım"}
    ],
    
    değerlendirme_kriterleri=[
        {kriter="Netlik geliştirme", ağırlık=0.3},
        {kriter="Problem çözme katkısı", ağırlık=0.4},
        {kriter="Etkileşim oluşturma", ağırlık=0.1},
        {kriter="Saklamayı kolaylaştırma", ağırlık=0.2}
    ],
    
    karar_kuralları=[
        {kural="roi > 1.0", eylem="Yatırımı sürdür veya artır"},
        {kural="0.7 < roi < 1.0", eylem="Verimlilik için optimize et"},
        {kural="roi < 0.7", eylem="Yatırımı azalt veya yeniden yapılandır"},
        {kural="roi > 1.5", eylem="Stratejik genişlemeyi düşün"}
    ]
}
```

### 4.2. Maliyet-Fayda Analizi

Bağlam yatırımlarının artılarını ve eksilerini tartın:

```
/maliyet_fayda_analizi.yap{
    karar="Kapsamlı teknik arka planı dahil et",
    
    maliyetler=[
        {tür="Jeton tüketimi", etki=700, önem="Yüksek"},
        {tür="Karmaşıklık artışı", etki="Orta", önem="Orta"},
        {tür="Odak seyreltmesi", etki="Düşük", önem="Düşük"},
        {tür="Erişilebilirlik azaltma", etki="Orta", önem="Orta"}
    ],
    
    faydalar=[
        {tür="Anlama derinliği", etki="Yüksek", önem="Yüksek"},
        {tür="Karar kalitesi", etki="Önemli", önem="Yüksek"},
        {tür="Kendi kendine yeterliliği sağlama", etki="Orta", önem="Orta"},
        {tür="Gelecek temeli", etki="Yüksek", önem="Orta"}
    ],
    
    nicel_değerlendirme={
        maliyet_puanı=3.2,
        fayda_puanı=4.1,
        net_fayda=0.9,
        yorum="Olumlu ama çok güçlü değil"
    },
    
    hassas_faktörler=[
        {faktör="Kullanıcı uzmanlık seviyesi", etki="Teknik detayın değerini değiştirir"},
        {faktör="Problem karmaşıklığı", etki="Arka plan gerekliliğini etkiler"},
        {faktör="Mevcut jeton bütçesi", etki="Karşılanabilirliği belirler"}
    ],
    
    öneri="Teknik arka planı dahil et ancak verimlilik ve erişilebilirlik için optimize et; aşamalı açıklama yaklaşımını düşün"
}
```

### 4.3. Fırsat Maliyeti Değerlendirmesi

Her tahsis seçimiyle neyden vazgeçtiğinizi değerlendirin:

```
/fırsat_maliyeti.değerlendir{
    jeton_bütçesi=8000,
    
    tahsis_senaryosu={
        sistem_talimatları=1500,
        çekirdek_içerik=3000,
        örnekler=2000,
        keşif=1000,
        rezerv=500
    },
    
    vazgeçilen_alternatifler=[
        {seçenek="Ek örnekler", potansiyel_değer="Çeşitlilik yoluyla gelişmiş netlik", jeton_gerekli=1000},
        {seçenek="Tarihsel bağlam", potansiyel_değer="Evrimin daha derin anlaşılması", jeton_gerekli=1200},
        {seçenek="Karşı argümanlar", potansiyel_değer="Daha dengeli perspektif", jeton_gerekli=800},
        {seçenek="Uygulama detayları", potansiyel_değer="Pratik uygulama rehberliği", jeton_gerekli=1500}
    ],
    
    en_yüksek_fırsat_maliyetleri=[
        {vazgeçilen="Uygulama detayları", maliyet_derecelendirmesi="Yüksek", gerekçe="Doğrudan pratik değer kaybı"},
        {vazgeçilen="Karşı argümanlar", maliyet_derecelendirmesi="Orta", gerekçe="Perspektif genişliği feda edildi"}
    ],
    
    azaltma_stratejileri=[
        {strateji="Aşamalı açıklama", uygulama="Gerektiğinde detayları ertele"},
        {strateji="Referans verme", uygulama="Tam olarak geliştirmeden kabul et"},
        {strateji="Özetleme", uygulama="Özü sıkıştırılmış biçimde sağla"},
        {strateji="Önceliklendirme", uygulama="En yüksek kaldıraçlı öğelere odaklan"}
    ]
}
```

### 4.4. Risk Yönetimi

Potansiyel bağlam bütçesi sorunlarını belirleyin ve azaltın:

```
/bağlam_riskleri.yönet{
    risk_değerlendirmesi=[
        {
            risk="Jeton sınırı aşıldı",
            olasılık="Orta",
            etki="Yüksek",
            risk_puanı="Yüksek",
            göstergeler=["Genişleyen kapsam", "Büyüyen karmaşıklık", "%80 kapasiteye yaklaşma"]
        },
        {
            risk="Kritik bilgi atlandı",
            olasılık="Düşük",
            etki="Şiddetli",
            risk_puanı="Orta-Yüksek",
            göstergeler=["Agresif özetleme", "Hızlı konu değişimleri", "Karmaşıklık sıkıştırması"]
        },
        {
            risk="Tutarlılık bozulması",
            olasılık="Orta",
            etki="Yüksek",
            risk_puanı="Yüksek",
            göstergeler=["Parçalanmış referanslar", "Bağlam çelişkileri", "Gezinme sorunları"]
        },
        {
            risk="Değer uyumsuzluğu",
            olasılık="Orta",
            etki="Orta",
            risk_puanı="Orta",
            göstergeler=["Kullanıcı yönlendirmesi", "Etkileşim düşüşü", "Açıklama talepleri"]
        }
    ],
    
    azaltma_stratejileri=[
        {
            risk="Jeton sınırı aşıldı",
            stratejiler=[
                {eylem="Aşamalı özetleme", uygulama="Eski içeriği kademeli olarak sıkıştır"},
                {eylem="Kapsam sınırı uygulaması", uygulama="Açık konu sınırlamalarını koru"},
                {eylem="Rezerv yönetimi", uygulama="Her zaman %10 jeton rezervi koru"}
            ]
        },
        {
            risk="Kritik bilgi atlandı",
            stratejiler=[
                {eylem="Kritiklik etiketlemesi", uygulama="Koruma için temel öğeleri işaretle"},
                {eylem="Referans bakımı", uygulama="Detaylar sıkıştırıldığında bile işaretçileri koru"},
                {eylem="Doğrulama kontrol noktaları", uygulama="Periyodik olarak kritik öğelerin mevcut olduğunu doğrula"}
            ]
        },
        {
            risk="Tutarlılık bozulması",
            stratejiler=[
                {eylem="Yapısal güçlendirme", uygulama="Açık organizasyon işaretçilerini koru"},
                {eylem="Bağlantı izleme", uygulama="Referans bütünlüğünü düzenli olarak kontrol et"},
                {eylem="Tutarlılık kurtarma", uygulama="Kayma tespit edildiğinde çerçeveyi yeniden kur"}
            ]
        },
        {
            risk="Değer uyumsuzluğu",
            stratejiler=[
                {eylem="Değer doğrulaması", uygulama="Hedeflerle uyumu düzenli olarak kontrol et"},
                {eylem="Geri bildirim entegrasyonu", uygulama="Kullanıcı sinyallerine göre ayarla"},
                {eylem="Öncelik yeniden kalibrasyonu", uygulama="Kaynak tahsisini değerle yeniden hizala"}
            ]
        }
    ],
    
    acil_durum_planları=[
        {tetikleyici="%90 jeton kapasitesine ulaşıldı", plan="Acil durum özetleme protokolünü başlat"},
        {tetikleyici="Tutarlılık puanı 0.7'nin altına düştü", plan="Yapısal kurtarma prosedürünü yürüt"},
        {tetikleyici="Birden çok açıklama talebi", plan="Değer hizalama kontrolü ve ayarlaması yap"},
        {tetikleyici="Kritik öğe kaybı tespit edildi", plan="Temel içeriğin hedeflenmiş yeniden oluşturulmasını uygula"}
    ]
}
```

**Düşünme Egzersizi**: En önemli veya zorlu bağlam mühendisliği senaryolarınızı düşünün. Hangi finansal disiplin bu durumlar için en değerli içgörüleri sunabilir? Bu yaklaşımı özel olarak nasıl uygulardınız?

## 5. Bütçe Döngüleri ve Planlama

Finansal planlama gibi, bağlam bütçelemesi de farklı zaman ölçeklerinde çalışır.

### 5.1. Stratejik Bütçe Planlaması

Uzun vadeli bağlam mimarisi planlaması:

```
/stratejik_bütçe.planla{
    zaman_çerçevesi="Uzatılmış etkileşim veya ilişki",
    
    vizyon={
        hedef="Makine öğrenmesi temellerinin kapsamlı bir şekilde anlaşılmasını geliştir",
        kapsam="Temel kavramlardan ileri uygulamalara kadar",
        değer_önerisi="Bağımsız uygulama ve problem çözmeyi sağla"
    },
    
    çekirdek_stratejiler=[
        {
            strateji="Aşamalı bilgi oluşturma",
            yaklaşım="Kavramları temelden ileriye doğru katmanla",
            kaynak_çıkarımları="Tanımsal içeriği öne yükle, aşamalı olarak uygulamaya kaydır"
        },
        {
            strateji="Pratik uygulama vurgusu",
            yaklaşım="Teoriyi uygulama boyunca bağla",
            kaynak_çıkarımları="Örneklere ve alıştırmalara tutarlı bir şekilde tahsis et"
        },
        {
            strateji="Kavramsal çerçeve güçlendirmesi",
            yaklaşım="Çekirdek zihinsel modelleri düzenli olarak yeniden ziyaret et ve güçlendir",
            kaynak_çıkarımları="Özyinelemeli güçlendirme için kapasite ayır"
        },
        {
            strateji="Uyarlanabilir hız ve derinlik",
            yaklaşım="Gösterilen anlamaya göre karmaşıklığı ayarla",
            kaynak_çıkarımları="Ayarlamalar için esneklik rezervlerini koru"
        }
    ],
    
    anahtar_performans_göstergeleri=[
        {metrik="Kavram saklama", ölçüm="Referans olmadan uygulama", hedef="%80 hatırlama"},
        {metrik="Uygulama yeteneği", ölçüm="Başarılı problem çözme", hedef="%70 başarı oranı"},
        {metrik="Kavramsal entegrasyon", ölçüm="Bağlantı kurma", hedef="Gösterilen sentez"},
        {metrik="İlerleme verimliliği", ölçüm="Öğrenme oranı", hedef="Yeniden çalışma olmadan optimum hız"}
    ],
    
    kaynak_tahsis_stratejisi={
        erken_aşama={
            temeller="%40",
            örnekler="%30",
            pratik="%20",
            keşif="%10"
        },
        orta_aşama={
            temeller="%20",
            örnekler="%30",
            pratik="%35",
            keşif="%15"
        },
        ileri_aşama={
            temeller="%10",
            örnekler="%25",
            pratik="%40",
            keşif="%25"
        }
    }
}
```

### 5.2. Taktiksel Bütçe Planlaması

Orta vadeli bağlam planlaması:

```
/taktiksel_bütçe.planla{
    zaman_çerçevesi="Tek oturum veya belirli konu keşfi",
    
    hedefler=[
        {hedef="Doğal dil işleme temellerini açıkla", öncelik="Yüksek"},
        {hedef="Anahtar NLP yaklaşımlarını karşılaştır", öncelik="Orta"},
        {hedef="Basit bir uygulama örneği göster", öncelik="Yüksek"},
        {hedef="Daha geniş ML manzarasına bağla", öncelik="Düşük"}
    ],
    
    kaynak_kısıtlamaları={
        mevcut_jetonlar=6000,
        mevcut_zaman="30 dakikalık etkileşim",
        karmaşıklık_eşiği="Teknik ama yarı teknik kitleye erişilebilir",
        önkoşul_bilgisi="Temel ML anlayışı, NLP özellikleri yok"
    },
    
    tahsis_planı={
        giriş_çerçevelemesi=600,
        çekirdek_nlp_kavramları=1500,
        yaklaşım_karşılaştırması=1200,
        pratik_örnek=1800,
        daha_geniş_bağlam=400,
        esneklik_rezervi=500
    },
    
    kritik_yol=[
        {kilometretaşı="Temel anlayışı oluştur", jeton_tahsisi=1200},
        {kilometretaşı="Anahtar yaklaşımları keşfet", jeton_tahsisi=1200},
        {kilometretaşı="Pratik uygulamayı göster", jeton_tahsisi=1800},
        {kilometretaşı="Sentezle ve bağla", jeton_tahsisi=800}
    ],
    
    acil_durum_planlaması=[
        {tetikleyici="Kavram karışıklığı", yanıt="Açıklama için rezervden tahsis et"},
        {tetikleyici="Beklenmedik derinlik ihtiyacı", yanıt="Çekirdek netliği korumak için karşılaştırma kapsamını azalt"},
        {tetikleyici="Zaman kısıtlaması baskısı", yanıt="Daha geniş bağlam bölümünü sıkıştır"},
        {tetikleyici="Hızlı anlama", yanıt="Pratik örneği karmaşıklıkla genişlet"}
    ]
}
```

### 5.3. Operasyonel Bütçe Planlaması

Anlık bağlam yönetimi:

```
/operasyonel_bütçe.planla{
    zaman_çerçevesi="Mevcut alışveriş veya anlık görev",
    
    anlık_ihtiyaçlar=[
        {ihtiyaç="Transformatörler hakkında belirli bir soruyu yanıtla", öncelik="Acil"},
        {ihtiyaç="Önceki modellerle ilişkiyi netleştir", öncelik="Yüksek"},
        {ihtiyaç="Uygulama değerlendirmesi sağla", öncelik="Orta"}
    ],
    
    mevcut_kaynaklar={
        kalan_jetonlar=2500,
        kullanıcı_dikkati="Odaklanmış ama sınırlı",
        önceki_bağlam="Dikkat mekanizmalarının temelleri kuruldu",
        referans_malzemesi="Gömülü model bilgisi"
    },
    
    tahsis_kararı={
        doğrudan_yanıt=900,
        bağlamsal_bağlantı=600,
        uygulama_notları=700,
        netliği_sağlama=200,
        beklenmedik_ihtiyaçlar_rezervi=100
    },
    
    yürütme_öncelikleri=[
        "Çekirdek sorunun tamamen ele alındığından emin ol",
        "Kurulmuş bilgiye bağlan",
        "Eyleme geçirilebilir uygulama rehberliği sağla",
        "Netliği ve tutarlılığı koru"
    ],
    
    başarı_kriterleri=[
        "Soru tamamen yanıtlandı",
        "Önceki tartışmayla net bir bağlantı kuruldu",
        "Pratik sonraki adımlar özetlendi",
        "Açıklama gerektiren karışıklık yok"
    ]
}
```

### 5.4. Bütçe İncelemesi ve Ayarlaması

Düzenli değerlendirme ve optimizasyon:

```
/bütçe.incele_ve_ayarla{
    inceleme_süreci=[
        {
            yön="Tahsis etkinliği",
            değerlendirme_yöntemi="Değer sunumu değerlendirmesi",
            bulgular="Örnekler etkiye göre aşırı tahsis aldı",
            ayarlama="Örnek tahsisini %15 azalt, kavram açıklamasına yönlendir"
        },
        {
            yön="Bilgi yoğunluğu",
            değerlendirme_yöntemi="Jeton başına değer analizi",
            bulgular="Giriş bölümü düşük yoğunluğa sahip (0.6 vs. hedef 0.8)",
            ayarlama="Girişi %25 sıkıştır, tüm anahtar noktaları koru"
        },
        {
            yön="Anlama etkisi",
            değerlendirme_yöntemi="Anlama kontrol soruları",
            bulgular="Karmaşık kavram açıklamaları güçlendirme gerektiriyor",
            ayarlama="Çekirdek kavram netliğine %10 daha fazla tahsis et, çevresel detayları azalt"
        },
        {
            yön="Etkileşim kalitesi",
            değerlendirme_yöntemi="Etkileşim deseni analizi",
            bulgular="Pratik uygulamalarla en yüksek etkileşim",
            ayarlama="Pratik içeriği %20 artır, sıraya daha erken entegre et"
        }
    ],
    
    ayarlama_uygulaması={
        zaman_çerçevesi="Sonraki etkileşim döngüsü",
        yaklaşım="Ölçümle artımlı ayarlama",
        iletişim="İyileştirmenin açıkça kabul edilmesi",
        doğrulama="Uygulamadan sonra etkinlik kontrolü"
    },
    
    sürekli_iyileştirme_sistemi={
        izleme="Sürekli değer sunumu takibi",
        geri_bildirim_döngüsü="Sonuçlara göre düzenli ayarlama",
        deney="Alternatiflerin kontrollü testi",
        belgeleme="Değişikliklerin ve etkilerin kaydı"
    }
}
```

**Sokratik Soru**: Stratejik, taktiksel ve operasyonel planlama açısından açıkça düşünmek bağlam mühendisliği yaklaşımınızı nasıl değiştirebilir? Şu anda en çok hangi planlama ufkuna odaklanıyorsunuz ve zaman çerçevenizi genişletmekten ne kazanabilirsiniz?

## 6. Bütçe Krizleri ve Yönetimi

İyi planlanmış bütçeler bile krizlerle karşılaşabilir. İşte bağlam bütçesi acil durumlarının nasıl ele alınacağı:

### 6.1. Jeton Tükenmesi

Sınırınızı aşmak üzereyken:

```
/jeton_tükenmesi.yönet{
    uyarı_işaretleri=[
        "Bağlam penceresinin %90'ına yaklaşma",
        "Hızla artan jeton tüketim oranı",
        "Kapsanacak önemli bir zemin kalan karmaşık konu",
        "Çözüm gerektiren birden çok açık konu"
    ],
    
    acil_eylemler=[
        {
            eylem="Acil durum sıkıştırması",
            uygulama="Kritik olmayan geçmişi agresif bir şekilde özetle",
            etki="Kullanılan jetonların %10-30'unu geri kazanır",
            ödünleşim="Nüans ve detayı kaybedebilir"
        },
        {
            eylem="Kapsam triyajı",
            uygulama="Yalnızca en yüksek öncelikli öğeleri belirle ve odaklan",
            etki="Kalan jetonları temel unsurlara yoğunlaştırır",
            ödünleşim="İkincil hedefleri erteler veya terk eder"
        },
        {
            eylem="Yapı düzenlemesi",
            uygulama="Biçimlendirme ve organizasyonel ek yükü azalt",
            etki="Ek yük jetonlarının %5-15'ini geri kazanır",
            ödünleşim="Gezinilebilirliği ve netliği azaltabilir"
        },
        {
            eylem="Tamamlama bölme",
            uygulama="Birden çok küçük etkileşime böl",
            etki="Sınırsız etkili jeton bütçesi yaratır",
            ödünleşim="Geçiş ek yükü ve potansiyel süreksizlik getirir"
        }
    ],
    
    kurtarma_planı=[
        {aşama="Stabilize et", eylemler=["Acil durum önlemlerini uygula", "Kritik bağlamı koru", "Tutarlılığı koru"]},
        {aşama="Yeniden yapılandır", eylemler=["Verimlilik için yeniden düzenle", "Sürdürülebilir jeton deseni uygula", "Temel öğeleri yeniden oluştur"]},
        {aşama="Önle", eylemler=["Erken uyarı sistemi kur", "Önleyici sıkıştırma uygula", "Jeton verimliliği protokolleri oluştur"]}
    ],
    
    önleme_stratejileri=[
        {
            strateji="Aşamalı özetleme",
            uygulama="Eski içeriği düzenli olarak sıkıştır",
            etkinlik="Uzun etkileşimler için yüksek"
        },
        {
            strateji="Yapılandırılmış jeton bütçelemesi",
            uygulama="Kategori sınırlarını belirle ve uygula",
            etkinlik="Disiplinli yaklaşım için yüksek"
        },
        {
            strateji="Jeton izleme sistemi",
            uygulama="Uyarı eşikleriyle tüketimi izle",
            etkinlik="İyi uyumla orta-yüksek"
        },
        {
            strateji="Verimlilik optimizasyonu",
            uygulama="Jeton israfını ortadan kaldırmak için düzenli inceleme",
            etkinlik="Yüksek ancak tutarlı dikkat gerektirir"
        }
    ]
}
```

### 6.2. Değer Uyumsuzluğu

Kaynaklar istenen sonuçları üretmediğinde:

```
/değer_uyumsuzluğu.ele_al{
    tanımlama=[
        {sinyal="Kullanıcı hedefleri yeniden yönlendiriyor veya yeniden belirtiyor", önem="Yüksek"},
        {sinyal="Sağlanan içerikle düşük etkileşim", önem="Orta"},
        {sinyal="Farklı ihtiyaçların açıkça ifade edilmesi", önem="Yüksek"},
        {sinyal="Farklı beklentileri gösteren sorular", önem="Orta"}
    ],
    
    tanı_süreci=[
        {adım="Hedef netleştirmesi", eylem="Amaçlanan sonuçları açıkça doğrula"},
        {adım="Değer değerlendirmesi", eylem="Kullanıcı için en önemli olanı belirle"},
        {adım="Hizalama analizi", eylem="Mevcut tahsisi önceliklerle karşılaştır"},
        {adım="Boşluk tanımlaması", eylem="Belirli uyumsuzlukları belirle"}
    ],
    
    düzeltme_stratejileri=[
        {
            strateji="Değer sıfırlaması",
            uygulama="Açıklanmış hedefler etrafında açıkça yeniden yönlendir",
            yaklaşım="'Sizin için en önemli olana odaklandığımdan emin olayım...'"
        },
        {
            strateji="Yeniden Tahsis",
            uygulama="Kaynakları yüksek değerli alanlara kaydır",
            yaklaşım="Düşük etkili içeriği azalt, yüksek öncelikli alanları genişlet"
        },
        {
            strateji="Format uyarlaması",
            uygulama="İçeriğin sunulma şeklini değiştir",
            yaklaşım="Daha değerliyse ayrıntılı açıklamalardan örneklere geç"
        },
        {
            strateji="Kapsam ayarlaması",
            uygulama="Değere göre kapsamı genişlet veya daralt",
            yaklaşım="Derinlik için odağı daralt veya kapsamlı görünüm için genişlet"
        }
    ],
    
    önleme_mekanizmaları=[
        {
            mekanizma="Erken değer doğrulaması",
            uygulama="Başlangıçta hedefleri ve öncelikleri onayla",
            etkinlik="Açık beklentiler için yüksek"
        },
        {
            mekanizma="Değer kontrol kilometretaşları",
            uygulama="Devam eden hizalamayı periyodik olarak doğrula",
            etkinlik="Gelişen etkileşimler için orta-yüksek"
        },
        {
            mekanizma="Geri bildirim döngüleri",
            uygulama="Yön ayarlaması için açık kanallar oluştur",
            etkinlik="Duyarlı adaptasyonla yüksek"
        },
        {
            mekanizma="Değer şeffaflığı",
            uygulama="Tahsis seçimlerini ve gerekçelerini görünür kıl",
            etkinlik="İşbirlikçi bağlamlar için orta-yüksek"
        }
    ]
}
```

### 6.3. Kaynak Tükenmesi

Jetonlardan ziyade dikkat veya tutarlılık tükendiğinde:

```
/kaynak_tükenmesi.yönet{
    jeton_olmayan_kaynaklar=[
        {
            kaynak="Dikkat kapasitesi",
            tükenme_sinyalleri=["Etkileşim düşüşü", "Anlama sorunları", "Saklama sorunları"],
            etki="Azaltılmış emilim ve uygulama"
        },
        {
            kaynak="Tutarlılık rezervi",
            tükenme_sinyalleri=["Bağlantı zorluğu", "Entegrasyon zorlukları", "Yapı bozulması"],
            etki="Parçalanmış anlama ve uygulama"
        },
        {
            kaynak="Kavramsal çalışma belleği",
            tükenme_sinyalleri=["Unutulan öğeler", "Daha önce kapsanan materyal hakkında karışıklık", "Tekrarlayan sorular"],
            etki="Verimsiz öğrenme ve ilerleme"
        },
        {
            kaynak="Etkileşim enerjisi",
            tükenme_sinyalleri=["Pasif yanıtlar", "Daha kısa yanıtlar", "Azalan etkileşim kalitesi"],
            etki="Azaltılmış işbirliği ve keşif"
        }
    ],
    
    müdahale_stratejileri=[
        {
            kaynak="Dikkat kapasitesi",
            stratejiler=[
                {yaklaşım="Parçalara ayırma", uygulama="Daha küçük, sindirilebilir parçalara ayır"},
                {yaklaşım="Odak daraltma", uygulama="Derinliği korumak için kapsamı azalt"},
                {yaklaşım="Desen oluşturma", uygulama="Unutulmaz çerçeveler oluştur"},
                {yaklaşım="Çok modlu güçlendirme", uygulama="Çeşitli sunum yöntemleri kullan"}
            ]
        },
        {
            kaynak="Tutarlılık rezervi",
            stratejiler=[
                {yaklaşım="Yapısal güçlendirme", uygulama="Organizasyonel çerçeveyi güçlendir"},
                {yaklaşım="Bağlantı haritalama", uygulama="İlişkileri açıkça göster"},
                {yaklaşım="Aşamalı entegrasyon", uygulama="Sistematik olarak yeniyi kurulmuşa bağla"},
                {yaklaşım="Tutarlılık kontrol noktaları", uygulama="Anlama bağlantılarını düzenli olarak doğrula"}
            ]
        },
        {
            kaynak="Kavramsal çalışma belleği",
            stratejiler=[
                {yaklaşım="Aktif özetleme", uygulama="Anahtar noktaları düzenli olarak özetle"},
                {yaklaşım="Referans demirleme", uygulama="Kararlı referans noktaları oluştur"},
                {yaklaşım="Bellek iskelesi", uygulama="Saklama için destekleyici yapılar oluştur"},
                {yaklaşım="Stratejik tekrar", uygulama="Önemli öğeleri güçlendir"}
            ]
        },
        {
            kaynak="Etkileşim enerjisi",
            stratejiler=[
                {yaklaşım="Değer vurgulama", uygulama="İlgililiği ve etkiyi vurgula"},
                {yaklaşım="Varyasyon tanıtımı", uygulama="Hızı, formatı veya yaklaşımı değiştir"},
                {yaklaşım="İlgi hedefleme", uygulama="Bilinen motivasyon alanlarına bağlan"},
                {yaklaşım="Etkileşimli öğeler", uygulama="Aktif katılım fırsatlarını artır"}
            ]
        }
    ],
    
    uzun_vadeli_sürdürülebilirlik=[
        {
            ilke="Kaynak döngüsü",
            uygulama="Farklı talep türleri arasında geçiş yap",
            fayda="İlerlemeyi korurken iyileşmeye izin verir"
        },
        {
            ilke="Aşamalı zorluk",
            uygulama="Kapasite arttıkça karmaşıklığı kademeli olarak artır",
            fayda="Zamanla kaynak kapasitesi oluşturur"
        },
        {
            ilke="Stratejik konsolidasyon",
            uygulama="Öğrenmeyi düzenli olarak güçlendir ve entegre et",
            fayda="Sürekli kaynak taleplerini azaltır"
        },
        {
            ilke="Verimlilik iyileştirmesi",
            uygulama="İletişim ve öğrenme yaklaşımlarını sürekli olarak iyileştir",
            fayda="Benzer sonuçlar için kaynak maliyetini azaltır"
        }
    ]
}
```

### 6.4. Bütçe Yeniden Dengelemesi

Tahsisleriniz önemli bir ayarlama gerektirdiğinde:

```
/bağlam_bütçesi.yeniden_dengele{
    yeniden_dengeleme_tetikleyicileri=[
        {tetikleyici="Hedef evrimi", gösterge="Değişen hedefler veya öncelikler", eşik="Yönünde önemli değişiklik"},
        {tetikleyici="Etkinlik verileri", gösterge="Kategoriye göre yatırım getirisi metrikleri", eşik="Beklenenden %20+ sapma"},
        {tetikleyici="Kaynak kısıtlamaları", gösterge="Jeton limiti değişiklikleri", eşik="Mevcut bütçede %15+ değişiklik"},
        {tetikleyici="İçerik değerlendirmesi", gösterge="Değer değerlendirmesi", eşik="Önemli değer dağılımı kayması"}
    ],
    
    yeniden_dengeleme_süreci=[
        {
            adım="Mevcut durum değerlendirmesi",
            eylemler=[
                "Tüm tahsis kategorilerini değerlendir",
                "Etkinliği ve değer sunumunu ölç",
                "Dengesizlikleri ve verimsizlikleri belirle",
                "Uyumsuzluğun temel nedenlerini belirle"
            ]
        },
        {
            adım="Değer tabanlı önceliklendirme",
            eylemler=[
                "Çekirdek hedefleri ve sonuçları yeniden onayla",
                "Öğeleri etki ve gerekliliğe göre sırala",
                "Yüksek yatırım getirisi fırsatlarını belirle",
                "Azaltma için düşük değerli alanları işaretle"
            ]
        },
        {
            adım="Tahsis yeniden tasarımı",
            eylemler=[
                "Yeni kategori tahsisleri taslağı hazırla",
                "Mevcuttan hedefe geçiş yaklaşımı oluştur",
                "Korkulukları ve izleme metriklerini belirle",
                "Acil durum uyarlamaları oluştur"
            ]
        },
        {
            adım="Uygulama ve izleme",
            eylemler=[
                "Yeniden dengelenmiş tahsis yaklaşımını yürüt",
                "Anahtar metrikler üzerindeki etkiyi izle",
                "Gerektiğinde gerçek zamanlı ayarlamalar yap",
                "Gelecekteki referans için etkinliği belgele"
            ]
        }
    ],
    
    yaygın_yeniden_dengeleme_desenleri=[
        {
            desen="Değer yoğunlaşması",
            senaryo="Birçok alanda çok dağınık",
            yaklaşım="Genişliği azalt, yüksek değerli alanlarda derinliği artır",
            tipik_sonuçlar="Öncelikli alanlarda daha büyük etki"
        },
        {
            desen="Temel güçlendirmesi",
            senaryo="Sallantılı anlayış sürekli sorunlara neden oluyor",
            yaklaşım="Temellere geçici olarak tahsisi artır",
            tipik_sonuçlar="Başlangıç yatırımından sonra daha verimli ilerleme"
        },
        {
            desen="Pratik vurgu",
            senaryo="Mevcut ihtiyaçlar için çok teorik",
            yaklaşım="Kavram açıklamasından uygulamaya kaydır",
            tipik_sonuçlar="Gelişmiş pratik yetenek ve etkileşim"
        },
        {
            desen="Ek yük azaltma",
            senaryo="Çok fazla yapı, süreç, meta-içerik",
            yaklaşım="Organizasyonu ve açıklamayı düzenle",
            tipik_sonuçlar="Kısıtlamalar dahilinde daha doğrudan değer sunumu"
        }
    ]
}
```

**Düşünme Egzersizi**: Uyumsuzluk, tükenme veya yeniden dengeleme ihtiyacı yaşadığınız bir bağlam mühendisliği senaryosunu düşünün. Bunu nasıl ele aldınız? Yukarıda açıklanan stratejilerden hangisi daha etkili olabilirdi?

## 7. Bütçe Modeli Zihinsel Çerçeveleri

Bütçe Modeli içindeki farklı metaforlar, bağlam yönetimine tamamlayıcı bakış açıları sunar.

### 7.1. Yatırım Portföyü Çerçevesi

Bağlamınızı çeşitlendirilmiş bir yatırım portföyü olarak görün:

```
/yatırım_portföyü.çerçevele{
    çekirdek_kavram="Bağlamı farklı özelliklere ve getirilere sahip bir yatırım portföyü olarak yönet",
    
    öğeler=[
        {
            öğe="Çekirdek varlıklar (Sistem talimatları, temel kavramlar)",
            özellikler=[
                "Daha düşük oynaklık",
                "Genel performans için temel",
                "Uzun vadeli değer"
            ],
            tahsis_yaklaşımı="Kalite odaklı önemli temel tahsis",
            optimizasyon="Sağlamlığı ve netliği sağla"
        },
        {
            öğe="Büyüme yatırımları (Anahtar örnekler, uygulamalar, keşifler)",
            özellikler=[
                "Daha yüksek potansiyel getiriler",
                "Daha değişken sonuçlar",
                "Önemli etki fırsatı"
            ],
            tahsis_yaklaşımı="Yüksek potansiyelli alanlara stratejik yatırım",
            optimizasyon="Risk/ödül dengesi, yaklaşımları çeşitlendir"
        },
        {
            öğe="Gelir üretenler (Pratik uygulamalar, anında değer)",
            özellikler=[
                "Güvenilir getiriler",
                "Doğrudan, ölçülebilir faydalar",
                "Tutarlı değer üretimi"
            ],
            tahsis_yaklaşımı="Sürekli sonuçlar için yeterli tahsis sağla",
            optimizasyon="Verimliliği ve güvenilirliği en üst düzeye çıkar"
        },
        {
            öğe="Spekülatif pozisyonlar (Yeni bağlantılar, yaratıcı keşifler)",
            özellikler=[
                "Yüksek risk/yüksek ödül",
                "Potansiyel atılım değeri",
                "Asimetrik getiri profili"
            ],
            tahsis_yaklaşımı="Küçük, stratejik tahsisler",
            optimizasyon="Keşfi sağlarken riski yönet"
        }
    ],
    
    portföy_yönetimi_ilkeleri=[
        {
            ilke="Çeşitlendirme",
            uygulama="Tahsisi farklı içerik türleri ve yaklaşımları arasında yay",
            fayda="Tam başarısızlık riskini azaltır, değere birden çok yol sağlar"
        },
        {
            ilke="Risk ayarlı getiriler",
            uygulama="Öğeleri belirsizliğe göre değere göre değerlendir",
            fayda="Genel portföy performansını optimize eder"
        },
        {
            ilke="Yeniden Dengeleme",
            uygulama="Performansa göre tahsisleri periyodik olarak ayarla",
            fayda="Koşullar değiştikçe optimum dağılımı korur"
        },
        {
            ilke="Maliyet yönetimi",
            uygulama="Jeton ek yükünü ve verimsizlikleri en aza indir",
            fayda="Portföy genelinde net getirileri iyileştirir"
        }
    ],
    
    uygulama_senaryoları=[
        {
            senaryo="Uzun vadeli öğrenme ilişkisi",
            portföy_stratejisi="Büyümeye vurgu yaparak dengeli",
            anahtar_odak="Temel istikrarla zamanla değer oluşturma"
        },
        {
            senaryo="Tek seferlik problem çözme",
            portföy_stratejisi="Bazı spekülasyonlarla gelir odaklı",
            anahtar_odak="Potansiyel atılım içgörüleriyle güvenilir sonuçlar"
        },
        {
            senaryo="Keşifsel araştırma",
            portföy_stratejisi="Büyüme ve spekülasyon odaklı",
            anahtar_odak="Değerli yeni perspektifler ve bağlantılar keşfetme"
        },
        {
            senaryo="Prosedürel rehberlik",
            portföy_stratejisi="Güçlü çekirdekle gelir ağırlıklı",
            anahtar_odak="Sağlam temelle güvenilir, pratik değer"
        }
    ]
}
```

### 7.2. Kaynak Ekonomisi Çerçevesi

Bağlamı bir üretim ve tüketim ekonomik sistemi olarak kavramsallaştırın:

```
/kaynak_ekonomisi.çerçevele{
    çekirdek_kavram="Bağlamı kaynaklar, üretim, tüketim ve değer yaratımı olan bir ekonomik sistem olarak gör",
    
    öğeler=[
        {
            öğe="Kaynaklar (Jetonlar, dikkat, bilgi tabanı)",
            özellikler=[
                "Sınırlı kullanılabilirlik",
                "Değişken kalite ve erişilebilirlik",
                "Kıtlık kısıtlamalarına tabi"
            ],
            yönetim_yaklaşımı="En yüksek değerli kullanıma göre dikkatli tahsis",
            optimizasyon="Kaynak kullanım verimliliğini artır"
        },
        {
            öğe="Üretim (İçerik oluşturma, akıl yürütme, sentez)",
            özellikler=[
                "Kaynakları değere dönüştürür",
                "Değişken verimlilik ve etkinlik",
                "Üretim yöntemlerine ve kısıtlamalarına tabi"
            ],
            yönetim_yaklaşımı="Üretim yöntemlerini ve süreçlerini optimize et",
            optimizasyon="Çıktı kalitesini ve üretim verimliliğini artır"
        },
        {
            öğe="Tüketim (Anlama, uygulama, karar verme)",
            özellikler=[
                "Değerin nihayetinde nasıl gerçekleştirildiği",
                "Değişken kapasite ve tercihler",
                "Tüketim kısıtlamalarına tabi"
            ],
            yönetim_yaklaşımı="Üretimi tüketim ihtiyaçlarıyla hizala",
            optimizasyon="Erişilebilirliği ve kullanılabilirliği artır"
        },
        {
            öğe="Piyasa dinamikleri (Değişen ihtiyaçlar, geri bildirim döngüleri)",
            özellikler=[
                "Gelişen talep ve tercihler",
                "Dikkat için rekabetçi alternatifler",
                "Değer algısı ve memnuniyeti"
            ],
            yönetim_yaklaşımı="Değişen koşullara duyarlılığı koru",
            optimizasyon="Piyasa araştırmasını ve uyarlanabilirliği artır"
        }
    ],
    
    ekonomik_ilkeler=[
        {
            ilke="Karşılaştırmalı üstünlük",
            uygulama="Yaklaşımınızın en büyük göreceli güce sahip olduğu alanlara odaklan",
            fayda="Uzmanlaşma yoluyla değeri en üst düzeye çıkarır"
        },
        {
            ilke="Marjinal fayda",
            uygulama="Bir sonraki kaynak birimini en yüksek değerli fırsata tahsis et",
            fayda="Artımlı değer yaratımını optimize eder"
        },
        {
            ilke="Arz ve talep",
            uygulama="İçerik arzını dikkat/ilgi talebiyle dengele",
            fayda="Değer alışverişi dengesi yaratır"
        },
        {
            ilke="Ekonomik verimlilik",
            uygulama="İsrafı en aza indir ve üretkenliği en üst düzeye çıkar",
            fayda="Mevcut kaynaklardan daha fazla değer yaratılır"
        }
    ],
    
    uygulama_senaryoları=[
        {
            senaryo="İçerik zengini rekabetçi ortam",
            ekonomik_strateji="Farklılaşma ve uzmanlaşmış değer",
            anahtar_odak="Benzersiz değer önerisi oluşturma"
        },
        {
            senaryo="Kaynak kısıtlı etkileşim",
            ekonomik_strateji="Verimlilik ve temel unsurlara odaklanma",
            anahtar_odak="Minimum kaynaklardan maksimum değer"
        },
        {
            senaryo="Hızla değişen gereksinimler",
            ekonomik_strateji="Uyarlanabilir üretim ve pazar algılaması",
            anahtar_odak="Gelişen ihtiyaçlara duyarlı ayarlama"
        },
        {
            senaryo="Değer belirsizliği",
            ekonomik_strateji="Geri bildirim döngüleriyle çeşitlendirilmiş üretim",
            anahtar_odak="Ortaya çıkan değeri keşfetme ve yanıtlama"
        }
    ]
}
```

### 7.3. Enerji Yönetimi Çerçevesi

Bağlam kaynaklarını korunması ve yönlendirilmesi gereken enerji olarak düşünün:

```
/enerji_yönetimi.çerçevele{
    çekirdek_kavram="Bağlam kaynaklarını bir sistemde akan, koruma ve yönlendirme gerektiren enerji olarak ele al",
    
    öğeler=[
        {
            öğe="Enerji kaynakları (Mevcut jetonlar, dikkat, bilgi)",
            özellikler=[
                "Sınırlı kapasite",
                "Değişken kalite ve güç",
                "Tükenme ve yenilenmeye tabi"
            ],
            yönetim_yaklaşımı="Dikkatli tüketim ve koruma",
            optimizasyon="Verimli kullanımı sağla ve israfı önle"
        },
        {
            öğe="Enerji dönüşümü (İşleme, akıl yürütme, sentez)",
            özellikler=[
                "Ham enerjiyi faydalı formlara dönüştürür",
                "Verimlilik kayıplarına tabi",
                "Çeşitli dönüşüm yöntemleri"
            ],
            yönetim_yaklaşımı="Uygun dönüşüm yöntemlerini seç",
            optimizasyon="Dönüşüm verimliliğini artır"
        },
        {
            öğe="Enerji iletimi (İletişim, açıklama, gösterim)",
            özellikler=[
                "Enerjiyi kaynaktan uygulamaya taşır",
                "İletim kayıplarına tabi",
                "Çeşitli iletim kanalları"
            ],
            yönetim_yaklaşımı="Etkili iletim kanallarını seç",
            optimizasyon="İletim kayıplarını azalt"
        },
        {
            öğe="Enerji uygulaması (Anlama, karar verme, eylem)",
            özellikler=[
                "Enerjiyi istenen sonuçlara dönüştürür",
                "Değişken verimlilik ve etkinlik",
                "Farklı ihtiyaçlar için farklı uygulamalar"
            ],
            yönetim_yaklaşımı="Enerjiyi en yüksek etkili uygulamalara yönlendir",
            optimizasyon="Uygulama etkinliğini artır"
        }
    ],
    
    enerji_ilkeleri=[
        {
            ilke="Enerjinin korunumu",
            uygulama="Tüm jeton/dikkat kaynaklarını hesaba kat, israfı en aza indir",
            fayda="Sınırlı kaynaklardan maksimum değer çıkarma"
        },
        {
            ilke="Enerji verimliliği",
            uygulama="Dönüşüm ve iletimdeki kayıpları azalt",
            fayda="Daha etkili değer sunumu"
        },
        {
            ilke="Yönlendirilmiş akış",
            uygulama="Kaynakları belirli hedeflere yönlendir",
            fayda="Dağınık etki yerine yoğun etki"
        },
        {
            ilke="Güç yönetimi",
            uygulama="Enerji uygulama oranını ve yoğunluğunu kontrol et",
            fayda="Her görev için uygun güç, sürdürülebilir çalışma"
        }
    ],
    
    uygulama_senaryoları=[
        {
            senaryo="Yüksek karmaşıklıklı açıklama",
            enerji_stratejisi="Yönlendirilmiş iletimle verimli dönüşüm",
            anahtar_odak="Karmaşık bilgiyi erişilebilir anlayışa dönüştürme"
        },
        {
            senaryo="Dikkat sınırlı etkileşim",
            enerji_stratejisi="Yüksek verimli, yoğun uygulama",
            anahtar_odak="Minimum bilişsel yükle maksimum etki"
        },
        {
            senaryo="Uzatılmış etkileşim",
            enerji_stratejisi="Yenilenmeyle sürdürülebilir tüketim",
            anahtar_odak="Süre boyunca enerjiyi koruma"
        },
        {
            senaryo="Kritik anlama",
            enerji_stratejisi="Doğrulama ile yedekli iletim",
            anahtar_odak="Engellere rağmen başarılı enerji aktarımını sağlama"
        }
    ]
}
```

**Sokratik Soru**: Bu çerçevelerden hangisi bağlam mühendisliği zorluklarınızla en çok rezonansa giriyor? Bu perspektifi benimsemek, yapay zeka etkileşimlerinizde kaynak tahsisine yaklaşımınızı nasıl değiştirebilir?

## 8. Diğer Zihinsel Modellerle Entegrasyon

Bütçe Modeli, diğer bağlam mühendisliği zihinsel modellerini güçlü şekillerde tamamlar.

### 8.1. Bütçe Modeli + Bahçe Modeli

Ekonomik ve bahçecilik perspektiflerini birleştirme:

```
/bütçe_bahçe.entegre_et{
    entegre_kavram="Kaynaklı bahçe: Planlı, bütçeli bir büyüme ortamı",
    
    birleştirilmiş_öğeler=[
        {
            kavram="Yatırım dikimi (Bütçe: Stratejik yatırım + Bahçe: Tohum seçimi)",
            açıklama="Kasıtlı kaynak tahsisi ile yüksek yatırım getirili bitkiler/kavramlar seç",
            uygulama="Yüksek büyüme potansiyeline sahip çekirdek kavramları dikkatlice seç ve yatırım yap",
            örnek="Daha sonraki anlamayı sağlayan temel çerçevelere önemli jetonlar tahsis etme"
        },
        {
            kavram="Kaynak toprağı (Bütçe: Temel yatırımı + Bahçe: Toprak hazırlığı)",
            açıklama="Büyümeyi destekleyen verimli temele kaynak tahsis et",
            uygulama="Verimli büyümeyi sağlayan yüksek kaliteli temel bağlama yatırım yap",
            örnek="Daha sonraki açıklamayı daha verimli hale getiren açık tanımlara ve ilkelere jeton harcama"
        },
        {
            kavram="Verim optimizasyonu (Bütçe: Yatırım Getirisi analizi + Bahçe: Hasat planlaması)",
            açıklama="Girdilere göre değerli çıktıları en üst düzeye çıkar",
            uygulama="Kaynak yatırımından optimum değer hasadı için tasarla",
            örnek="Verimlilik için birden çok kavramı aynı anda göstermek üzere örnekleri yapılandırma"
        },
        {
            kavram="Mevsimsel bütçeleme (Bütçe: Döngüsel planlama + Bahçe: Büyüme mevsimleri)",
            açıklama="Kaynak tahsisini doğal gelişim döngüleriyle hizala",
            uygulama="Farklı etkileşim aşamaları için farklı kaynak tahsisleri planla",
            örnek="'Uygulama mevsimi' sırasında örneklere daha yüksek jeton tahsisi vs. 'kavram mevsimi'"
        }
    ],
    
    entegrasyon_faydaları=[
        "Kaynak disiplinini organik büyüme perspektifiyle birleştirir",
        "Planlama ve ortaya çıkışı dengeler",
        "Yatırımı doğal gelişim döngüleriyle ilişkilendirir",
        "Hem nicel hem de nitel çerçeveler sağlar"
    ],
    
    uygulama_yaklaşımları=[
        {
            yaklaşım="Bütçe odaklı bahçe planlaması",
            uygulama="Kaynak kısıtlamalarıyla başla, bahçeyi bunların içinde tasarla",
            uygun_olduğu_yerler="Kaynak sınırlı ortamlar, verimlilik açısından kritik bağlamlar"
        },
        {
            yaklaşım="Bahçe odaklı bütçe tahsisi",
            uygulama="İdeal bahçe tasarımıyla başla, sonra öğelere kaynak tahsis et",
            uygun_olduğu_yerler="Kalite açısından kritik bağlamlar, keşifsel ortamlar"
        },
        {
            yaklaşım="Dengeli ortak geliştirme",
            uygulama="Bahçe tasarımını ve bütçe tahsisini yinelemeli olarak geliştir",
            uygun_olduğu_yerler="Esnek kısıtlamalara sahip karmaşık, gelişen etkileşimler"
        }
    ]
}
```

### 8.2. Bütçe Modeli + Nehir Modeli

Ekonomik ve akış perspektiflerini birleştirme:

```
/bütçe_nehir.entegre_et{
    entegre_kavram="Kaynaklı nehir: Ekonomik kısıtlamalara sahip bir değer akışı",
    
    birleştirilmiş_öğeler=[
        {
            kavram="Kanal yatırımı (Bütçe: Altyapı yatırımı + Nehir: Nehir yatağı şekillendirme)",
            açıklama="Akış desenlerini ve yönlerini optimize etmek için kaynak tahsis et",
            uygulama="Bilgi akışını verimli bir şekilde yönlendiren yapılara yatırım yap",
            örnek="Dikkati uygun şekilde yönlendiren açık organizasyonel yapılara jeton harcama"
        },
        {
            kavram="Akış kapasitesi planlaması (Bütçe: Kaynak tahsisi + Nehir: Akış yönetimi)",
            açıklama="Kaynak tahsisini istenen akış hacmi ve hızıyla eşleştir",
            uygulama="Amaçlanan bilgi hareketini desteklemek için jeton dağılımını planla",
            örnek="Karmaşıklığa göre geçiş açıklamalarına uygun jetonlar tahsis etme"
        },
        {
            kavram="Değer akıntısı (Bütçe: Yatırım Getirisi odağı + Nehir: Ana akıntı)",
            açıklama="Birincil kaynakları en yüksek değerli akışa yönlendir",
            uygulama="Çekirdek değer akışının yeterli kaynak almasını sağla",
            örnek="Merkezi anlatıya veya argümana güçlü jeton tahsisini sürdürme"
        },
        {
            kavram="Kol bütçelemesi (Bütçe: Portföy tahsisi + Nehir: Kol yönetimi)",
            açıklama="Destekleyici akışlara stratejik olarak kaynak tahsis et",
            uygulama="İkincil ve üçüncül konulara uygun yatırım planla",
            örnek="Ana anlamaya beslenen ilgili kavramlara ölçülü tahsis"
        }
    ],
    
    entegrasyon_faydaları=[
        "Kaynak disiplinini dinamik akış perspektifiyle birleştirir",
        "Statik tahsisi dinamik hareketle ilişkilendirir",
        "Hem kaynakları hem de yönü yönetmek için çerçeve sağlar",
        "Hem verimlilik hem de ivme için planlamayı sağlar"
    ],
    
    uygulama_yaklaşımları=[
        {
            yaklaşım="Bütçe kontrollü akış",
            uygulama="Akış olasılıklarını şekillendiren kaynak kısıtlamaları belirle",
            uygun_olduğu_yerler="Yüksek kısıtlı ortamlar, verimlilik açısından kritik bağlamlar"
        },
        {
            yaklaşım="Akış optimize edilmiş bütçe",
            uygulama="İdeal akışı belirle, sonra onu desteklemek için kaynak tahsis et",
            uygun_olduğu_yerler="Deneyim açısından kritik bağlamlar, anlatı odaklı ortamlar"
        },
        {
            yaklaşım="Dinamik tahsis",
            uygulama="Akış koşullarına göre kaynak tahsisini sürekli olarak ayarla",
            uygun_olduğu_yerler="Hızla gelişen bağlamlar, duyarlı ortamlar"
        }
    ]
}
```

### 8.3. Bütçe Modeli + Alan Teorisi

Ekonomik ve alan perspektiflerini birleştirme:

```
/bütçe_alan.entegre_et{
    entegre_kavram="Kaynaklı alan: Anlamsal manzaralara ekonomik bir yaklaşım",
    
    birleştirilmiş_öğeler=[
        {
            kavram="Çekici yatırımı (Bütçe: Stratejik yatırım + Alan: Çekici oluşumu)",
            açıklama="Anlamsal çekicileri geliştirmek ve güçlendirmek için kaynak tahsis et",
            uygulama="Anlamayı organize eden anahtar kavramlara stratejik olarak jeton yatırımı yap",
            örnek="Sonraki içeriği yapılandıracak çekirdek çerçevelere yoğun tahsis"
        },
        {
            kavram="Sınır Yatırım Getirisi (Bütçe: Yatırım Getirisi analizi + Alan: Sınır yönetimi)",
            açıklama="Alan sınırlarındaki yatırımların getirisini değerlendir",
            uygulama="Değer muhafazasına göre sınırlara kaynak tahsis et",
            örnek="Değer seyreltmesini önlemek için kapsam tanımına uygun jeton harcaması"
        },
        {
            kavram="Rezonans verimliliği (Bütçe: Verimlilik metrikleri + Alan: Rezonans desenleri)",
            açıklama="Jeton yatırımına göre rezonans değerini en üst düzeye çıkar",
            uygulama="Yüksek verimli desen güçlendirmesi için tasarla",
            örnek="Etkiyi çoğaltan yankılanan desenler oluşturmak için yapılandırılmış tahsis"
        },
        {
            kavram="Kalıntı kullanımı (Bütçe: Varlık kullanımı + Alan: Sembolik kalıntı)",
            açıklama="Kalıcı anlam parçalarından değeri en üst düzeye çıkar",
            uygulama="Verimlilik için mevcut kalıntıyı stratejik olarak kullan",
            örnek="Yeniden açıklama maliyetlerini azaltmak için kurulmuş kavramlara referans verme"
        }
    ],
    
    entegrasyon_faydaları=[
        "Kaynak disiplinini anlamsal manzara perspektifiyle birleştirir",
        "Alan operasyonları için ekonomik çerçeve sağlar",
        "Alan operasyon etkinliğinin ölçülmesini sağlar",
        "Kaynak tahsisini ortaya çıkan özelliklerle ilişkilendirir"
    ],
    
    uygulama_yaklaşımları=[
        {
            yaklaşım="Bütçe kısıtlı alan tasarımı",
            uygulama="Kaynak kısıtlamaları içinde alan operasyonları planla",
            uygun_olduğu_yerler="Jeton sınırlı ortamlar, verimlilik açısından kritik bağlamlar"
        },
        {
            yaklaşım="Alan optimize edilmiş bütçeleme",
            uygulama="İdeal alan dinamiklerini belirle, sonra uygun şekilde kaynak sağla",
            uygun_olduğu_yerler="Karmaşık kavramsal ortamlar, ortaya çıkış odaklı bağlamlar"
        },
        {
            yaklaşım="Değer tabanlı alan yatırımı",
            uygulama="Değer potansiyeline göre alan operasyonlarına kaynak tahsis et",
            uygun_olduğu_yerler="Yatırım Getirisi odaklı bağlamlar, stratejik alan geliştirme"
        }
    ]
}
```

**Düşünme Egzersizi**: Karşılaştığınız bir bağlam mühendisliği zorluğunu düşünün. Bütçe Modelini başka bir zihinsel modelle birleştirmek size yeni içgörüler veya yaklaşımlar nasıl verebilir? Hangi özel entegre kavramlar uygulamak için en değerli olurdu?

## 9. Pratik Uygulamalar

Bütçe Modeli, yaygın bağlam mühendisliği zorluklarına pratik çözümler sunar.

### 9.1. Jeton Kısıtlı Uzman

Sıkı sınırlar içinde derin uzmanlık sunma:

```
/jeton_kısıtlı_uzman.uygula{
    senaryo="4K jeton limiti içinde sofistike teknik rehberlik sağlama",
    
    bütçe_yaklaşımı={
        tahsis_stratejisi="Katı önceliklendirme ile değer tabanlı",
        verimlilik_odağı="Çekirdek içerikte maksimum bilgi yoğunluğu",
        risk_yönetimi="Kritik açıklamalar için rezerv"
    },
    
    özel_teknikler=[
        {
            teknik="Hassas terminoloji",
            uygulama="Anlamı verimli bir şekilde paketleyen alana özgü terimler kullan",
            jeton_etkisi="Açıklayıcı ek yükte %30-50 azalma",
            örnek="'bir matematiksel optimizasyon algoritması...' yerine 'gradyan inişi' kullanma"
        },
        {
            teknik="Katmanlı bilgi mimarisi",
            uygulama="Önce çekirdek içeriği sun, detayları talep üzerine sağla",
            jeton_etkisi="Yüksek değerli içeriği öne yükler, daha düşük değerli detayları erteler",
            örnek="Önce çekirdek algoritma açıklaması, jetonlar izin verirse optimizasyon teknikleri"
        },
        {
            teknik="Referans kullanımı",
            uygulama="Yeniden açıklamaktan ziyade kurulmuş bilgiye referans ver",
            jeton_etkisi="Referans verilen kavramlarda %70-90 tasarruf",
            örnek="'stokastik gradyan inişi kullanarak (bildiğiniz gibi...)'"
        },
        {
            teknik="Örnek sıkıştırması",
            uygulama="Minimal ama eksiksiz örnekler oluştur",
            jeton_etkisi="Örnek boyutunda %40-60 azalma",
            örnek="Yalnızca kritik deseni gösteren basitleştirilmiş kod"
        }
    ],
    
    bütçe_yapısı={
        çekirdek_rehberlik=1600,
        kritik_kavramlar=800,
        sıkıştırılmış_örnekler=1000,
        gezinme_ve_meta=200,
        açıklama_rezervi=400
    },
    
    başarı_metrikleri=[
        {metrik="Teknik doğruluk", hedef="%100", yaklaşım="Kısıtlamalara rağmen taviz yok"},
        {metrik="Eyleme geçirilebilirlik", hedef="Anında uygulanabilir", yaklaşım="Pratik rehberliğe odaklan"},
        {metrik="Anlaşılabilirlik", hedef="Hedef kitleye açık", yaklaşım="Kullanıcı uzmanlığıyla hizala"},
        {metrik="Verimlilik", hedef="Jeton başına maksimum değer", yaklaşım="Sürekli optimizasyon"}
    ]
}
```

### 9.2. Uzatılmış Öğrenme Yolculuğu

Uzun vadeli bir etkileşimde kaynakları yönetme:

```
/uzatılmış_öğrenme_yolculuğu.uygula{
    senaryo="Bir kullanıcıyı birden çok oturumda karmaşık bir konuyu öğrenmeye yönlendirme",
    
    bütçe_yaklaşımı={
        tahsis_stratejisi="Yaşam döngüsü tabanlı bütçeleme",
        verimlilik_odağı="Uzun vadeli saklama ve uygulama",
        risk_yönetimi="İlerlemeye göre uyarlanabilir yeniden tahsis"
    },
    
    yolculuk_aşamaları=[
        {
            aşama="Temel oluşturma",
            bütçe_odağı="Çekirdek kavram yatırımı",
            tahsis={
                temel_kavramlar=%40,
                zihinsel_modeller=%25,
                başlangıç_uygulaması=%20,
                öğrenme_mimarisi=%10,
                esneklik=%5
            },
            optimizasyon_stratejisi="Gelecekteki verimliliği sağlayan kaliteli temellere yoğun yatırım yap"
        },
        {
            aşama="Beceri geliştirme",
            bütçe_odağı="Destekle uygulamalı pratik",
            tahsis={
                yönlendirilmiş_pratik=%35,
                kavram_genişletme=%20,
                geri_bildirim_ve_düzeltme=%25,
                entegrasyon=%15,
                esneklik=%5
            },
            optimizasyon_stratejisi="Yeni içeriği kurulmuş bilginin uygulamasıyla dengele"
        },
        {
            aşama="Ustalık geliştirme",
            bütçe_odağı="İleri uygulama ve entegrasyon",
            tahsis={
                karmaşık_zorluklar=%40,
                alanlar_arası_entegrasyon=%25,
                ilke_çıkarma=%20,
                yansıma_ve_üstbiliş=%10,
                esneklik=%5
            },
            optimizasyon_stratejisi="İleri gelişim için kurulmuş temelden yararlan"
        },
        {
            aşama="Bağımsız uygulama",
            bütçe_odağı="Yönlendirilmiş özerklik ve genişletme",
            tahsis={
                koçluk=%30,
                problem_çözme_desteği=%30,
                genişletme_kaynakları=%25,
                yansıma_kolaylaştırması=%10,
                esneklik=%5
            },
            optimizasyon_stratejisi="Doğrudan talimat yatırımını kademeli olarak azalt, desteği artır"
        }
    ],
    
    aşama_arası_stratejiler=[
        {
            strateji="Bilgi varlığı geliştirme",
            uygulama="Zamanla değer kazanan yeniden kullanılabilir bilgi yapıları oluştur",
            örnek="Gelecekteki öğrenmeyi verimli bir şekilde organize eden zihinsel modeller geliştirme"
        },
        {
            strateji="Aralıklı güçlendirme",
            uygulama="Anahtar kavramlara optimum aralıklarla stratejik olarak yeniden yatırım yap",
            örnek="Kritik temelleri gözden geçirmek ve güçlendirmek için planlı jeton tahsisi"
        },
        {
            strateji="Aşamalı özetleme",
            uygulama="Ustalık geliştikçe daha önceki içeriği kademeli olarak sıkıştır",
            örnek="Temeller içselleştirildikçe temel bilgilere jeton tahsisini azaltma"
        },
        {
            strateji="Değer tabanlı devam",
            uygulama="Jeton sınırları yerine değer optimizasyonuna göre oturum sınırı kararları ver",
            örnek="Doğal değer kırılma noktalarında oturumları sonlandırma"
        }
    ],
    
    başarı_metrikleri=[
        {metrik="Bilgi saklama", hedef="Yüksek uzun vadeli saklama", yaklaşım="Stratejik güçlendirme"},
        {metrik="Beceri uygulaması", hedef="Etkili gerçek dünya kullanımı", yaklaşım="Aşamalı otantik pratik"},
        {metrik="Öğrenme verimliliği", hedef="Öğrenci için optimum hız", yaklaşım="Uyarlanabilir kaynak tahsisi"},
        {metrik="Devam eden etkileşim", hedef="Sürdürülebilir motivasyon", yaklaşım="Değer görünür yatırım"}
    ]
}
```

### 9.3. İşbirlikçi Yaratıcı

Yaratıcı bağlamlarda yapı ve keşfi dengeleme:

```
/işbirlikçi_yaratıcı.uygula{
    senaryo="Hem yapı hem de keşif ihtiyaçları olan bir kullanıcıyla yaratıcı bir projede çalışma",
    
    bütçe_yaklaşımı={
        tahsis_stratejisi="Hem istikrarlı hem de spekülatif yatırımlara sahip portföy",
        verimlilik_odağı="Maksimum yaratıcı değer ve ivme",
        risk_yönetimi="Dengeli koruma ve keşif"
    },
    
    işbirliği_modları=[
        {
            mod="Yapısal çerçeve",
            bütçe_özellikleri={
                tahsis="etkileşim jetonlarının %25-30'u",
                istikrar="Yüksek - tutarlı yatırım",
                optimizasyon="Yapının netliği ve kullanışlılığı",
                rezerv="Minimal - öngörülebilir ihtiyaçlar"
            },
            uygulama="Yaratıcı iskele ve organizasyon sağla ve sürdür"
        },
        {
            mod="Üretken keşif",
            bütçe_özellikleri={
                tahsis="etkileşim jetonlarının %30-40'ı",
                istikrar="Yaratıcı aşamaya göre değişken",
                optimizasyon="İlham ve olasılık üretimi",
                rezerv="Orta - umut verici yönleri takip et"
            },
            uygulama="Olasılıkları keşfet, alternatifler üret, fikirler geliştir"
        },
        {
            mod="Eleştirel iyileştirme",
            bütçe_özellikleri={
                tahsis="etkileşim jetonlarının %20-25'i",
                istikrar="Daha sonraki aşamalarda artar",
                optimizasyon="Kalite iyileştirme ve tutarlılık",
                rezerv="Düşük - odaklanmış uygulama"
            },
            uygulama="Yaratıcı öğeleri değerlendir, iyileştir ve rafine et"
        },
        {
            mod="Meta-işbirliği",
            bütçe_özellikleri={
                tahsis="etkileşim jetonlarının %10-15'i",
                istikrar="Dalgalanma kapasitesine sahip tutarlı temel",
                optimizasyon="Süreç etkinliği ve hizalama",
                rezerv="Yüksek - işbirliği ihtiyaçlarını ele al"
            },
            uygulama="İşbirlikçi sürecin kendisini yönet"
        }
    ],
    
    dinamik_tahsis_yaklaşımları=[
        {
            yaklaşım="Yaratıcı aşama kaydırma",
            uygulama="Yaratıcı döngüye göre mod tahsislerini ayarla",
            örnek="Erken daha fazla keşif jetonu, daha sonra daha fazla iyileştirme jetonu"
        },
        {
            yaklaşım="İvme takibi",
            uygulama="Yaratıcı enerji olan alanlara tahsisi artır",
            örnek="İlham geldiğinde keşfe jeton kaydırma"
        },
        {
            yaklaşım="Dengeli portföy bakımı",
            uygulama="Tüm modların minimum etkili tahsis almasını sağla",
            örnek="Ağır keşif sırasında bile yapısal yatırımı sürdürme"
        },
        {
            yaklaşım="Yatırım Getirisi tabanlı yeniden tahsis",
            uygulama="Kaynakları en yüksek yaratıcı değer üretimine kaydır",
            örnek="Özellikle verimli yaratıcı yönlere tahsisi artırma"
        }
    ],
    
    başarı_metrikleri=[
        {metrik="Yaratıcı kalite", hedef="Kısıtlamalar dahilinde mümkün olan en yüksek", yaklaşım="Etkili mod dengelemesi"},
        {metrik="İşbirlikçi memnuniyet", hedef="Enerji veren ortaklık", yaklaşım="Duyarlı tahsis"},
        {metrik="Proje ilerlemesi", hedef="Sürekli ilerleme", yaklaşım="Dengeli yapı ve keşif"},
        {metrek="Yaratıcı atılım", hedef="Yeni değerli öğeler", yaklaşım="Yeterli keşif yatırımı"}
    ]
}
```

**Sokratik Soru**: Bu uygulamalardan hangisi bağlam mühendisliği çalışmanıza en çok benziyor? Yapılandırılmış bütçe yaklaşımını benimsemek sonuçlarınızı nasıl iyileştirebilir? Özel ihtiyaçlarınıza daha iyi uyması için neyi uyarlardınız?

## 10. Sonuç: Kaynak Ustalığı Sanatı

Bütçe Modeli, bağlam mühendisliği için güçlü bir ekonomik mercek sunar ve sınırlı kaynaklarımızı nasıl düşündüğümüzü ve yönettiğimizi dönüştürür. Bağlamı ekonomik kısıtlamalar ve fırsatlar sistemi olarak görerek, yapay zeka etkileşimlerimizde netlik ve kontrol kazanırız.

Bağlam mühendisliği yolculuğunuza devam ederken şu temel ilkeleri aklınızda bulundurun:

### 10.1. Temel Bütçe İlkeleri

```
/bütçe_ilkeleri.özetle{
    temel_ilkeler=[
        {
            ilke="Kasıtlı tahsis",
            öz="Varsayılan desenler yerine kasıtlı seçimler",
            uygulama="Her jetonun nereye gideceğine bilinçli olarak karar ver",
            etki="Dramatik olarak geliştirilmiş kaynak etkinliği"
        },
        {
            ilke="Değer maksimizasyonu",
            öz="Hacim yerine etki için optimize et",
            uygulama="Jeton başına kalite ve etkinliğe odaklan",
            etki="Bağlam yatırımında daha yüksek getiri"
        },
        {
            ilke="Fırsat farkındalığı",
            öz="Her seçimin maliyetini tanı",
            uygulama="Her tahsisle neyden vazgeçildiğini düşün",
            etki="Daha dengeli ve düşünülmüş kararlar"
        },
        {
            ilke="Uyarlanabilir yönetim",
            öz="Değişen koşullara duyarlı ayarlama",
            uygulama="Gerektiğinde sürekli olarak izle ve yeniden tahsis et",
            etki="Değişen ihtiyaçlara rağmen sürdürülebilir etkinlik"
        },
        {
            ilke="Sürdürülebilir uygulama",
            öz="Kısa vadeli kazançlar yerine uzun vadeli yaşayabilirlik",
            uygulama="Sürekli getiri sağlayan yapılara yatırım yap",
            etki="Kümülatif faydalar ve bileşik büyüme"
        }
    ],
    
    entegrasyon_rehberliği=[
        "Bu ilkeleri izole uygulamalar yerine bütünsel bir sistem olarak uygula",
        "Bilinçli ödünleşim kararlarıyla rakip öncelikleri dengele",
        "Tutarlı uygulama ve yansıma yoluyla sezgisel ustalık geliştir",
        "Kapsamlı bağlam mühendisliği için diğer zihinsel modellerle birleştir"
    ]
}
```

### 10.2. Bütçe Modeli Ustalık Yolu

```
/ustalık_yolu.taslağını_çiz{
    aşamalar=[
        {
            aşama="Farkındalık",
            özellikler="Jeton kısıtlamalarının ve tahsis etkisinin tanınması",
            uygulamalar=["Jeton kullanımını izle", "Tahsis desenlerini fark et", "İsrafı belirle"],
            kilometretaşı="Bilinçli bağlam bütçelemesi"
        },
        {
            aşama="Kasıtlılık",
            özellikler="Kasıtlı tahsis ve amaçlı kısıtlamalar",
            uygulamalar=["Etkileşimlerden önce tahsisleri planla", "Kategori sınırları belirle", "Öncelikleri tanımla"],
            kilometretaşı="Yapılandırılmış bütçe yaklaşımı"
        },
        {
            aşama="Optimizasyon",
            özellikler="Kısıtlamalar dahilinde geliştirilmiş verimlilik ve etkinlik",
            uygulamalar=["Jeton başına değeri ölç", "Sonuçlara göre iyileştir", "Düşük değerli öğeleri azalt"],
            kilometretaşı="Yüksek yatırım getirili bağlam mühendisliği"
        },
        {
            aşama="Uyarlanabilirlik",
            özellikler="Değişen koşullara duyarlı ayarlama",
            uygulamalar=["Dinamik yeniden tahsis", "Geri bildirim entegrasyonu", "Bağlamsal ayarlama"],
            kilometretaşı="Esnek, dayanıklı bütçeleme"
        },
        {
            aşama="Ustalık",
            özellikler="Şeffaf gerekçeyle sezgisel mükemmellik",
            uygulamalar=["Değer odaklı tahsis", "Dengeli portföy yönetimi", "Stratejik yatırım"],
            kilometretaşı="Bilinçli açıklama ile bilinçsiz yetkinlik"
        }
    ],
    
    geliştirme_yaklaşımları=[
        {
            yaklaşım="Kasıtlı pratik",
            uygulama="Yansıma ile düzenli, odaklanmış uygulama",
            fayda="Hızlandırılmış beceri geliştirme"
        },
        {
            yaklaşım="Analitik inceleme",
            uygulama="Etkileşim sonrası bütçe analizi",
            fayda="Desen tanıma ve iyileştirme tanımlaması"
        },
        {
            yaklaşım="Deneysel varyasyon",
            uygulama="Farklı yaklaşımların kontrollü testi",
            fayda="Genişletilmiş araç seti ve bağlamsal anlama"
        },