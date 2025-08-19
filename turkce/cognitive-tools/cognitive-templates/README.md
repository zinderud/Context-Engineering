# Bilişsel Şablonlar

> "Herhangi bir aracın değeri, onu kullanan kişinin maharetindedir." — Leonardo da Vinci

## Genel Bakış

Bilişsel şablonlar, dil modellerinin spesifik düşünce süreçlerini sistematik olarak gerçekleştirmesini sağlayan yapılandırılmış istem kalıplarıdır. Bu şablonlar, insan bilişinin temel operasyonlarını (anlama, akıl yürütme, doğrulama, kompozisyon) AI sistemleri için kullanılabilir araçlara dönüştürür.

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  BİLİŞSEL ŞABLON KATEGORİLERİ                               │
│                                                              │
│  Anlama     → Akıl Yürütme → Doğrulama → Kompozisyon        │
│  (Understand) (Reason)       (Verify)    (Compose)          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Şablon Kategorileri

### 🧩 [Anlama Şablonları](understanding.md)
**Amaç**: Bilgiyi analiz etme ve yapılandırma  
**Ana Şablonlar**:
- Soru Analizi - Soruları bileşenlerine ayırma
- Bilgi Çıkarma - Metinden strukturel bilgi çıkarma
- Problem Ayrıştırma - Karmaşık problemleri parçalara ayırma
- Kavramsal Haritalama - Kavramlar arası ilişkileri belirleme

### 🤔 [Akıl Yürütme Şablonları](reasoning.md)
**Amaç**: Mantıklı ve sistematik düşünce süreçleri  
**Ana Şablonlar**:
- Düşünce Zinciri - Adım adım mantıksal akıl yürütme
- Nedensel Analiz - Sebep-sonuç ilişkilerini belirleme
- Karşılaştırmalı Analiz - Alternatifler arasında karşılaştırma
- Hipotez Testi - Varsayımları test etme

### ✅ [Doğrulama Şablonları](verification.md)
**Amaç**: Sonuçları kontrol etme ve doğrulama  
**Ana Şablonlar**:
- Mantık Kontrolü - Mantıksal tutarlılığı kontrol etme
- Gerçek Kontrolü - Olgusal doğruluğu teyit etme
- Çözüm Doğrulama - Problem çözümlerini kontrol etme
- Kalite Değerlendirme - Çıktı kalitesini değerlendirme

### 🔧 [Kompozisyon Şablonları](composition.md)
**Amaç**: Birden fazla şablonu birleştirme  
**Ana Şablonlar**:
- Sıralı Kompozisyon - Şablonları sırayla çalıştırma
- Paralel Kompozisyon - Şablonları paralel çalıştırma
- Koşullu Kompozisyon - Duruma göre şablon seçimi
- İteratif Kompozisyon - Döngüsel şablon uygulaması

## Şablon Kullanım Rehberi

### 1. Temel Kullanım
```markdown
# Basit Şablon Kullanımı
Bir şablonu doğrudan kopyalayıp özelleştirin:
- {{değişken}} alanlarını kendi içeriğinizle doldurun
- İhtiyaca göre bölümleri ekleyin veya çıkarın
- Token limitlerini göz önünde bulundurun
```

### 2. Parametre Özelleştirme
```markdown
# Şablon Parametrelerini Ayarlama
Şablonları spesifik kullanım senaryolarınıza göre uyarlayın:
- Ayrıntı seviyesini ayarlayın (brief/detailed/comprehensive)
- Hedef kitleyi belirtin (technical/general/expert)
- Çıktı formatını tanımlayın (bullet points/paragraphs/structured)
```

### 3. Kombine Kullanım
```markdown
# Şablonları Birleştirme
Daha güçlü sonuçlar için şablonları kombinleyin:
1. Anlama şablonu ile başlayın
2. Akıl yürütme şablonu ile devam edin
3. Doğrulama şablonu ile sonlandırın
```

## Performans Optimizasyonu

### Token Verimliliği
- **Kısa Şablonlar**: Basit görevler için ~50-100 token
- **Orta Şablonlar**: Standart analizler için ~100-200 token  
- **Uzun Şablonlar**: Kapsamlı çalışmalar için ~200-500 token

### Etkinlik Metrikleri
```
┌────────────────┬──────────────────┬──────────────────┐
│    Metrik      │     Hedef        │   Ölçüm Yöntemi  │
├────────────────┼──────────────────┼──────────────────┤
│ Doğruluk       │     >90%         │ Gerçek kontrolü  │
│ Tutarlılık     │     >85%         │ Çapraz test      │
│ Hız            │     <3 saniye    │ Yanıt süresi     │
│ Token Verimli  │     <1000 token  │ Token sayımı     │
└────────────────┴──────────────────┴──────────────────┘
```

## En İyi Uygulamalar

### 🎯 Doğru Şablon Seçimi
1. **Problemi tanımlayın**: Ne tür bir düşünce süreci gerekli?
2. **Karmaşıklığı değerlendirin**: Basit mi, karmaşık mı?
3. **Çıktı formatını belirleyin**: Nasıl bir sonuç istiyorsunuz?
4. **Uygun şablonu seçin**: İhtiyaçlarınızla eşleşen şablonu kullanın

### 🔄 İteratif Geliştirme
1. **Başlangıç şablonu**: Temel şablonla başlayın
2. **Test etme**: Küçük örneklerle deneyin
3. **İyileştirme**: Sonuçlara göre ayarlama yapın
4. **Ölçeklendirme**: Daha geniş kullanım için genişletin

### 🤝 Şablon Kombinasyonu
```markdown
# Örnek: Araştırma Analizi Workflow'u
1. **Problem Ayrıştırma** → Ana soruyu parçalara ayır
2. **Bilgi Çıkarma** → Her parça için veri topla
3. **Karşılaştırmalı Analiz** → Alternatifleri karşılaştır
4. **Doğrulama** → Sonuçları kontrol et
```

## Hata Ayıklama Rehberi

### Yaygın Sorunlar ve Çözümler

| Sorun | Sebep | Çözüm |
|-------|-------|--------|
| Belirsiz çıktı | Şablon çok genel | Daha spesifik parametreler ekle |
| Eksik bilgi | Şablon eksik | Ek analiz bölümleri ekle |
| Uzun yanıt | Şablon çok ayrıntılı | Token limitlerini belirt |
| Tutarsız sonuç | Şablon belirsiz | Net talimatlar ekle |

### Kalite Kontrol Kontrol Listesi
- [ ] Şablon parametreleri doğru tanımlanmış mı?
- [ ] Çıktı formatı net belirtilmiş mi?
- [ ] Token limitleri uygun mu?
- [ ] Test örnekleri başarılı mı?
- [ ] Hata durumları düşünülmüş mü?

## İleri Seviye Teknikler

### Dinamik Şablon Seçimi
```markdown
# Otomatik Şablon Seçimi
Girdi tipine göre otomatik şablon seçimi:
- Soru → Soru Analizi Şablonu
- Metin → Bilgi Çıkarma Şablonu  
- Problem → Problem Ayrıştırma Şablonu
- Karşılaştırma → Karşılaştırmalı Analiz Şablonu
```

### Şablon Miras Alma
```markdown
# Şablon Hiyerarşisi
Genel Analiz Şablonu
├── Teknik Analiz Şablonu
├── İş Analizi Şablonu
└── Akademik Analiz Şablonu
```

## Topluluk Katkıları

### Yeni Şablon Ekleme
1. **Şablon tasarımı**: Tekrarlanabilir kalıp oluşturun
2. **Test süreci**: Farklı senaryolarda test edin
3. **Dokümantasyon**: Kullanım rehberi yazın
4. **Topluluk gözden geçirme**: Geri bildirimleri toplayın

### Şablon Paylaşımı
- GitHub repository'ye katkıda bulunun
- Kullanım örnekleri paylaşın
- Performance metrikleri sağlayın
- Best practice önerilerinizi iletin

## Sonraki Adımlar

1. **[Understanding.md](understanding.md)** ile anlama şablonlarına başlayın
2. **[Reasoning.md](reasoning.md)** ile akıl yürütme becerilerinizi geliştirin  
3. **[Verification.md](verification.md)** ile doğrulama sistemlerinizi güçlendirin
4. **[Composition.md](composition.md)** ile gelişmiş kombinasyonları öğrenin

---

**Not**: Bu şablonlar sürekli gelişen, topluluk destekli araçlardır. Kullanım deneyimlerinizi paylaşarak ecosystem'in gelişmesine katkıda bulunun.
