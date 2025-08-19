# Bilişsel Programlar

> "Programlar insanların okuması için yazılmalı, sadece tesadüfen makinelerin çalıştırması için." — Harold Abelson

## Genel Bakış

Bilişsel programlar, dil modellerini spesifik akıl yürütme süreçleri boyunca yönlendiren yapılandırılmış, yeniden kullanılabilir istem kalıplarıdır. Geleneksel şablonlardan farklı olarak, bilişsel programlar değişkenler, fonksiyonlar, kontrol yapıları ve kompozisyon gibi programlama kavramlarını içererek daha sofistike ve uyarlanabilir akıl yürütme çerçeveleri oluşturur.

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  BİLİŞSEL PROGRAM YAPISI                                    │
│                                                              │
│  function programAdı(parametreler) {                        │
│    // İşleme mantığı                                         │
│    return istemMetni;                                        │
│  }                                                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Program Kategorileri

### 🎯 [Temel Programlar](basic-programs.md)
**İçerik**: Temel programlama kavramları ve basit bilişsel operasyonlar
- Fonksiyonlar ve Parametreler
- Koşullu Mantık  
- Döngüler ve İterasyon
- Basit Problem Çözme

### 🚀 [Gelişmiş Programlar](advanced-programs.md)
**İçerik**: Karmaşık akıl yürütme süreçleri ve sofistike programlama kalıpları
- Çok Aşamalı Analiz
- Özyinelemeli Akıl Yürütme
- Paralel İşleme
- Dinamik Adaptasyon

### 📚 [Program Kütüphanesi](program-library.py)
**İçerik**: Kullanıma hazır program koleksiyonu
- Matematik Problemleri
- Metin Analizi
- Karar Verme
- Yaratıcı Yazım

### 💡 [Program Örnekleri](program-examples.ipynb)
**İçerik**: Interaktif Jupyter notebook örnekleri
- Adım Adım Gösterimler
- Farklı Kullanım Senaryoları
- Performance Karşılaştırmaları
- Best Practice Örnekleri

## Program Geliştirme Süreci

### 1. Tasarım Aşaması
```javascript
// Örnek: Problem Çözme Programı Tasarımı
function problemÇöz(problem, yaklaşım="sistematik", detay="orta") {
  // Girdi analizi
  // Strateji belirleme
  // Adım adım çözüm
  // Doğrulama
}
```

### 2. Uygulama Aşaması
```javascript
// Program bileşenlerini tanımlama
const YAKLAŞIMLAR = {
  sistematik: "Adım adım metodoloji",
  yaratıcı: "Yaratıcı problem çözme",
  analitik: "Veri odaklı analiz"
};

const DETAY_SEVİYELERİ = {
  kısa: "Özet açıklama",
  orta: "Detaylı açıklama", 
  uzun: "Kapsamlı analiz"
};
```

### 3. Test Aşaması
```javascript
// Test senaryoları
const testProblemleri = [
  "Matematik problemi",
  "Mantık problemi", 
  "Yaratıcı problem",
  "Analiz problemi"
];

// Performance metrikleri
const metrikler = {
  doğruluk: "Çözüm doğruluğu",
  hız: "Yanıt süresi",
  verimlilik: "Token kullanımı",
  tutarlılık: "Sonuç tutarlılığı"
};
```

## Programlama Kalıpları

### Fonksiyonel Programlama
```javascript
// Saf fonksiyonlar
function analiz(veri) {
  return analizSonucu;
}

// Fonksiyon kompozisyonu
function birleştir(f1, f2) {
  return function(girdi) {
    return f2(f1(girdi));
  };
}
```

### Nesne Yönelimli Programlama
```javascript
class BilişselAnaliz {
  constructor(tip, parametreler) {
    this.tip = tip;
    this.parametreler = parametreler;
  }
  
  çalıştır(veri) {
    // Analiz implementasyonu
  }
}
```

### Reaktif Programlama
```javascript
// Event-driven program akışı
function dinle(olay, işleyici) {
  // Olay dinleyici ekleme
}

function tetikle(olay, veri) {
  // Olay tetikleme
}
```

## Token Optimizasyonu

### Verimli Program Yazma
```markdown
## Token Tasarrufu Teknikleri

1. **Kısa Değişken İsimleri**: `param` yerine `p` kullanın
2. **Şartlı İçerik**: Sadece gerekli bölümleri dahil edin
3. **Template Literal**: Dinamik içerik için şablon stringler
4. **Modüler Tasarım**: Küçük, yeniden kullanılabilir fonksiyonlar
```

### Performance Metrikleri
| Metrik | Hedef | Ölçüm |
|--------|-------|--------|
| Token/Operasyon | <100 | Otomatik sayım |
| Yanıt Süresi | <5s | Benchmark test |
| Bellek Kullanımı | <1MB | Sistem izleme |
| Başarı Oranı | >90% | Test sonuçları |

## Debugging ve Hata Ayıklama

### Yaygın Hatalar
```javascript
// ❌ Hatalı: Belirsiz parametreler
function analiz(veri) {
  return "Analiz tamamlandı";
}

// ✅ Doğru: Net parametreler
function analiz(veri, tip="detaylı", format="json") {
  // Implementasyon detayları
  return analizSonucu;
}
```

### Debug Teknikleri
```javascript
// Adım adım debug
function debugAnaliz(veri, debugMod=false) {
  if (debugMod) console.log("Başlangıç veri:", veri);
  
  const adım1 = önİşlem(veri);
  if (debugMod) console.log("Ön işlem sonucu:", adım1);
  
  const adım2 = işlem(adım1);
  if (debugMod) console.log("İşlem sonucu:", adım2);
  
  return adım2;
}
```

## Entegrasyon Rehberi

### API Entegrasyonu
```python
# Python örneği
import requests

def bilişsel_program_çalıştır(program, veri):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": program(veri)}]
        }
    )
    return response.json()
```

### Batch İşleme
```python
# Toplu veri işleme
def toplu_işlem(veri_listesi, program):
    sonuçlar = []
    for veri in veri_listesi:
        sonuç = bilişsel_program_çalıştır(program, veri)
        sonuçlar.append(sonuç)
    return sonuçlar
```

## İleri Seviye Konular

### Meta-Programlama
```javascript
// Kendi kendini değiştiren programlar
function metaProgram(kurallar) {
  return function(veri) {
    // Kurallara göre program oluştur
    const dinamikProgram = kurallarıUygula(kurallar);
    return dinamikProgram(veri);
  };
}
```

### Makine Öğrenmesi Entegrasyonu
```python
# ML model entegrasyonu
def akıllı_program(veri, model):
    # ML tahminleri ile program davranışını optimize et
    optimizasyonlar = model.predict(veri)
    program = programı_optimize_et(optimizasyonlar)
    return program(veri)
```

## Topluluk ve Katkı

### Program Paylaşımı
1. **GitHub repository**: Açık kaynak katkıları
2. **Program marketplace**: Hazır program satın alma/satma
3. **Community forum**: Program geliştirme tartışmaları
4. **Best practice guides**: Deneyim paylaşımları

### Kalite Standartları
- **Dokümantasyon**: Her program için detaylı açıklama
- **Test coverage**: %90+ test kapsamı
- **Performance benchmarks**: Standard metrikler
- **Security review**: Güvenlik değerlendirmesi

## Gelecek Yol Haritası

### Yakın Dönem (3-6 ay)
- [ ] Daha fazla temel program eklemek
- [ ] Performance optimization araçları
- [ ] Visual program editörü
- [ ] Otomatik test oluşturma

### Uzun Dönem (6-12 ay)
- [ ] AI-assisted program yazımı
- [ ] Cross-language support
- [ ] Enterprise integration tools
- [ ] Advanced analytics dashboard

## Başlarken

1. **[Basic Programs](basic-programs.md)** ile temel kavramları öğrenin
2. **[Advanced Programs](advanced-programs.md)** ile sofistike teknikleri keşfedin
3. **[Program Library](program-library.py)** den hazır çözümler kullanın
4. **[Examples](program-examples.ipynb)** ile pratik yapmaya başlayın

---

**İpucu**: En iyi öğrenme yöntemi direkt uygulama yapmaktır. Basit bir program ile başlayın ve kademeli olarak kompleksiteyi artırın.
