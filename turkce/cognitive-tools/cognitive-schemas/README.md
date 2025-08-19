# Bilişsel Şemalar

> "Yapı, özgürlük getirir." — John C. Maxwell

## Genel Bakış

Bilişsel şemalar, farklı alan ve görevler için bilgi temsilinin nasıl yapılandırılacağını tanımlayan standart formatlar ve çerçevelerdir. Bu şemalar, dil modellerinin tutarlı, tahmin edilebilir ve verimli şekilde bilgiyi işlemesini sağlar.

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  BİLİŞSEL ŞEMA HİYERARŞİSİ                                  │
│                                                              │
│  Kullanıcı Şemaları → Görev Şemaları → Alan Şemaları        │
│       ↓                    ↓               ↓                │
│  Birleşik Şemalar ←── Entegre Sistem ←── Meta Şemalar       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Şema Kategorileri

### 👤 [Kullanıcı Şemaları](user-schemas.md)
**Amaç**: Kullanıcı davranışları, tercihleri ve bağlamları modelleme
**Ana Şemalar**:
- Kullanıcı Profili - Demografik ve psikografik özellikler
- Tercih Matrisi - Kullanıcı seçimleri ve öncelikleri
- Davranış Kalıpları - Etkileşim geçmişi ve desenler
- Bağlam Modeli - Durumsal faktörler ve çevre

### 📋 [Görev Şemaları](task-schemas.md)
**Amaç**: Spesifik görevler için yapılandırılmış yaklaşımlar
**Ana Şemalar**:
- Problem Tanımı - Görev parametreleri ve kısıtları
- Çözüm Metodolojisi - Adım adım yaklaşım planı
- Kalite Kriterleri - Başarı metrikleri ve değerlendirme
- Kaynak Gereksinimi - Gerekli araçlar ve veriler

### 🎓 [Alan Şemaları](domain-schemas.md)
**Amaç**: Belirli bilgi alanları için uzmanlaşmış yapılar
**Ana Şemalar**:
- Bilimsel Araştırma - Hipotez, deney, sonuç yapısı
- İş Analizi - Pazar, strateji, operasyon çerçeveleri
- Eğitim - Öğrenme hedefleri, içerik, değerlendirme
- Yaratıcı Süreçler - İlham, geliştirme, iyileştirme

### 🌐 [Birleşik Şemalar](unified-schemas.md)
**Amaç**: Farklı şema türlerini entegre eden kapsamlı yapılar
**Ana Şemalar**:
- Multi-Modal Entegrasyon - Çoklu veri tipi desteği
- Cross-Domain Transfer - Alan arası bilgi transferi
- Adaptive Frameworks - Dinamik uyarlama mekanizmaları
- Emergence Patterns - Ortaya çıkan davranış kalıpları

## Şema Tasarım İlkeleri

### 🎯 Netlik ve Spesifiklik
```yaml
# ❌ Belirsiz şema
kullanıcı:
  bilgi: "çeşitli"
  tercih: "var"

# ✅ Net şema
kullanıcı:
  demografik:
    yaş: integer
    cinsiyet: enum[erkek, kadın, diğer]
    lokasyon: string
  tercihler:
    format: enum[kısa, detaylı, kapsamlı]
    ton: enum[resmi, samimi, teknik]
```

### 🔄 Esneklik ve Genişletilebilirlik
```yaml
# Temel şema yapısı
temel_şema:
  zorunlu_alanlar: ["id", "tip", "içerik"]
  opsiyonel_alanlar: ["meta", "bağlam", "uzantılar"]
  uzantı_noktaları: ["özel_alanlar", "eklentiler"]
```

### 📊 Ölçülebilirlik ve Doğrulanabilirlik
```yaml
# Doğrulama kuralları
doğrulama:
  alan_tipleri:
    sayısal: {min: 0, max: 100}
    metin: {min_uzunluk: 1, max_uzunluk: 1000}
    liste: {min_eleman: 1, max_eleman: 50}
  zorunluluk_kontrolleri: true
  format_kontrolleri: true
```

## Şema Kütüphanesi

### YAML Formatında Şemalar
```yaml
# schema-library.yaml yapısı
şema_kütüphanesi:
  versiyon: "1.0"
  şemalar:
    kullanıcı_profili:
      tip: "kullanıcı"
      alan: "genel"
      zorunlu: ["id", "ad", "tercihler"]
    görev_tanımı:
      tip: "görev"
      alan: "genel" 
      zorunlu: ["hedef", "kısıtlar", "metrikler"]
```

### JSON Schema Entegrasyonu
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Bilişsel Şema",
  "type": "object",
  "properties": {
    "şema_id": {"type": "string"},
    "tip": {"enum": ["kullanıcı", "görev", "alan", "birleşik"]},
    "içerik": {"type": "object"}
  },
  "required": ["şema_id", "tip", "içerik"]
}
```

## Şema Uygulama Kalıpları

### 1. Şema Validasyonu
```python
import jsonschema

def şema_doğrula(veri, şema):
    try:
        jsonschema.validate(veri, şema)
        return {"valid": True, "errors": []}
    except jsonschema.ValidationError as e:
        return {"valid": False, "errors": [str(e)]}
```

### 2. Şema Dönüştürme
```python
def şema_dönüştür(kaynak_veri, kaynak_şema, hedef_şema):
    # Şema arası veri dönüştürme
    mapping = şema_mapping_oluştur(kaynak_şema, hedef_şema)
    hedef_veri = mapping.apply(kaynak_veri)
    return hedef_veri
```

### 3. Dinamik Şema Oluşturma
```python
def dinamik_şema_oluştur(veri_örnekleri):
    # Veri örneklerinden otomatik şema çıkarma
    şema = {
        "type": "object",
        "properties": {}
    }
    
    for alan, değer in veri_örnekleri[0].items():
        şema["properties"][alan] = tip_çıkar(değer)
    
    return şema
```

## Performance ve Optimizasyon

### Şema Boyutu Optimizasyonu
```yaml
# Kompakt şema tasarımı
kompakt_şema:
  # Kısa alan isimleri
  id: string
  tp: enum[u, t, d, b]  # user, task, domain, unified
  dt: object           # data
  
  # Referans tabanlı değerler
  refs:
    common_fields: &common
      created: timestamp
      updated: timestamp
      version: string
    
  user_schema:
    <<: *common
    profile: object
```

### Bellek Verimliliği
```python
# Lazy loading şema implementasyonu
class LazySchema:
    def __init__(self, schema_path):
        self.schema_path = schema_path
        self._schema = None
    
    @property
    def schema(self):
        if self._schema is None:
            self._schema = self.load_schema()
        return self._schema
    
    def load_schema(self):
        # Şemayı sadece gerektiğinde yükle
        pass
```

## Versiyonlama ve Migrasyon

### Şema Versiyonlama
```yaml
şema_versiyonu:
  major: 1      # Breaking changes
  minor: 2      # Backward compatible additions
  patch: 3      # Bug fixes
  
  migration_path:
    "1.1.0": "migration_scripts/v1_1_to_1_2.py"
    "1.2.0": "migration_scripts/v1_2_to_1_3.py"
```

### Otomatik Migrasyon
```python
def şema_migrasyonu(eski_veri, eski_versiyon, yeni_versiyon):
    migration_path = get_migration_path(eski_versiyon, yeni_versiyon)
    
    current_data = eski_veri
    for migration_script in migration_path:
        current_data = migration_script.migrate(current_data)
    
    return current_data
```

## Kalite Güvencesi

### Test Stratejileri
```python
# Şema test suite
def şema_test_suite(şema):
    tests = [
        test_zorunlu_alanlar(şema),
        test_veri_tipleri(şema),
        test_kısıtlar(şema),
        test_referans_bütünlüğü(şema),
        test_performance(şema)
    ]
    
    return all(tests)
```

### Kalite Metrikleri
| Metrik | Hedef | Ölçüm |
|--------|-------|--------|
| Validasyon Başarısı | >99% | Otomatik test |
| Performans | <100ms | Benchmark |
| Bellek Kullanımı | <10MB | Profiling |
| Uyumluluk | %100 | Cross-validation |

## Entegrasyon Rehberi

### Database Entegrasyonu
```sql
-- PostgreSQL JSON schema validation
CREATE TABLE cognitive_data (
    id SERIAL PRIMARY KEY,
    schema_type VARCHAR(50),
    data JSONB,
    CONSTRAINT valid_schema CHECK (
        jsonb_matches_schema(schema_type, data)
    )
);
```

### API Entegrasyonu
```python
# REST API şema validasyonu
from flask import Flask, request, jsonify
from marshmallow import Schema, ValidationError

@app.route('/api/data', methods=['POST'])
def process_data():
    try:
        schema = get_schema(request.headers.get('Schema-Type'))
        validated_data = schema.load(request.json)
        result = process_with_schema(validated_data, schema)
        return jsonify(result)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
```

## İleri Seviye Konular

### Machine Learning Şema Öğrenme
```python
# ML ile otomatik şema discovery
from sklearn.cluster import KMeans

def şema_keşfi(veri_koleksiyonu):
    # Veri kalıplarından şema çıkarma
    patterns = extract_patterns(veri_koleksiyonu)
    clusters = KMeans(n_clusters=5).fit(patterns)
    schemas = [pattern_to_schema(cluster) for cluster in clusters]
    return schemas
```

### Quantum Schema Concepts
```yaml
# Quantum-inspired schema superposition
quantum_schema:
  superposition_states:
    - schema_variant_1
    - schema_variant_2
    - schema_variant_3
  
  measurement_criteria:
    context: "user_context"
    collapse_function: "max_relevance"
```

## Topluluk ve Ekosistem

### Şema Marketplace
- **Public Repository**: Açık kaynak şema koleksiyonu
- **Community Ratings**: Topluluk değerlendirmeleri
- **Usage Analytics**: Kullanım istatistikleri
- **Contribution Guidelines**: Katkı rehberleri

### Standards Compliance
- **JSON Schema**: Official JSON schema compliance
- **OpenAPI**: API documentation standards
- **W3C**: Web standards adherence
- **ISO**: International standardization

## Başlarken

1. **[User Schemas](user-schemas.md)** ile kullanıcı modellemeyi öğrenin
2. **[Task Schemas](task-schemas.md)** ile görev yapılandırmayı keşfedin
3. **[Domain Schemas](domain-schemas.md)** ile alan spesifik yaklaşımları inceleyin
4. **[Schema Library](schema-library.yaml)** den hazır şemaları kullanın

---

**Not**: Etkili şema tasarımı, deneyim ve iterasyon gerektirir. Küçük başlayıp kademeli olarak karmaşıklık ekleyin.
