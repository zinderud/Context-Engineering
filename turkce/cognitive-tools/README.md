# Context Engineering için Bilişsel Araçlar

> "Bana yeterince uzun bir kaldıraç ve altına koyabileceğim bir dayanak noktası verin, dünyayı yerinden oynatayım." — Arşimet

## Bilişsel Araçlar Nedir?
> "GPT-4.1'e 'bilişsel araçlarımızı' sağlamak, AIME2024'teki pass@1 performansını %26.7'den %43.3'e çıkarıyor ve o1-preview'un performansına çok yaklaştırıyor." — [IBM Haziran 2025](https://www.arxiv.org/pdf/2506.12115)

<div align="center">
    
![image](https://github.com/user-attachments/assets/a6402827-8bc0-40b5-93d8-46a07154fa4e)

"Araç, eldeki ana kavramları tanımlayarak, soruda ilgili bilgileri çıkararak ve problemi çözmede yardımcı olabilecek anlamlı özellikleri, teoremleri ve teknikleri vurgulayarak problemi parçalara ayırır." — [Dil Modellerinde Bilişsel Araçlarla Akıl Yürütmeyi Ortaya Çıkarma — IBM Haziran 2025](https://www.arxiv.org/pdf/2506.12115)

</div>

Bilişsel araçlar, dil modellerini belirli akıl yürütme işlemleri boyunca yönlendiren yapılandırılmış istem kalıplarıdır. İnsanların problemleri çözmek için kullandığı zihinsel araçlar (analojiler, zihinsel modeller, buluşsal yöntemler) gibi, bu araçlar modellere karmaşık akıl yürütme görevleri için iskelet sağlar.

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  BAĞLAM MÜHENDİSLİĞİ İLERLEMESİ                             │
│                                                              │
│  Atomlar     → Moleküller  → Hücreler    → Organlar    → Bilişsel Araçlar  │
│  (İstemler)    (Az-örnekli)  (Bellek)      (Çoklu-ajan)  (Akıl Yürütme Kalıpları) │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Yapı
```
cognitive-tools/
├── README.md                       # Genel bakış ve hızlı başlangıç rehberi
├── cognitive-templates/            # Bilişsel süreçler için şablonlar
│   ├── understanding.md            # Anlama şablonları
│   ├── reasoning.md                # Akıl yürütme şablonları
│   ├── verification.md             # Doğrulama şablonları
│   ├── composition.md              # Kompozisyon şablonları
│   ├── emergence.md                # Ortaya çıkış şablonları
│   ├── quantum_interpretation.md   # Kuantum semantik şablonları
│   ├── unified_field_reasoning.md  # Birleşik alan şablonları
│   ├── meta_recursive_reasoning.md # Öz-gelişim şablonları
│   ├── interpretability_scaffolding.md # Şeffaflık şablonları
│   ├── collaborative_co_evolution.md # İnsan-AI şablonları
│   └── cross_modal_integration.md  # Çoklu-modal şablonlar
├── cognitive-programs/             # Çalıştırılabilir bilişsel süreçler
│   ├── basic-programs.md           # Temel programlar
│   ├── advanced-programs.md        # Karmaşık programlar
│   ├── program-library.py          # Program koleksiyonu
│   ├── program-examples.ipynb      # Program gösterimleri
│   ├── emergence-programs.md       # Ortaya çıkış programları
│   ├── quantum_semantic_programs.md # Kuantum semantik programları
│   ├── unified_field_programs.md   # Birleşik alan programları
│   ├── meta_recursive_programs.md  # Öz-gelişim programları
│   ├── interpretability_programs.md # Şeffaflık programları
│   ├── collaborative_evolution_programs.md # İnsan-AI programları
│   └── cross_modal_programs.md     # Çoklu-modal programlar
├── cognitive-schemas/              # Bilgi temsil yapıları
│   ├── user-schemas.md             # Kullanıcı modelleme şemaları
│   ├── domain-schemas.md           # Alan bilgisi şemaları
│   ├── task-schemas.md             # Görev temsil şemaları
│   ├── schema-library.yaml         # Şema koleksiyonu
│   ├── field-schemas.md            # Alan teorisi şemaları
│   ├── quantum_schemas.md          # Kuantum semantik şemaları
│   ├── unified_schemas.md          # Birleşik alan şemaları
│   ├── meta_recursive_schemas.md   # Öz-gelişim şemaları
│   ├── interpretability_schemas.md # Şeffaflık şemaları
│   ├── collaborative_schemas.md    # İnsan-AI şemaları
│   └── cross_modal_schemas.md      # Çoklu-modal şemalar
├── cognitive-architectures/        # Sistem seviyesi çerçeveler
│   ├── solver-architecture.md      # Problem çözme mimarisi
│   ├── tutor-architecture.md       # Eğitim mimarisi
│   ├── research-architecture.md    # Araştırma asistanı mimarisi
│   ├── architecture-examples.py    # Mimari gösterimleri
│   ├── field-architecture.md       # Alan teorisi mimarisi
│   ├── quantum_architecture.md     # Kuantum semantik mimarisi
│   ├── unified_architecture.md     # Birleşik alan mimarisi
│   ├── meta_recursive_architecture.md # Öz-gelişim mimarisi
│   ├── interpretability_architecture.md # Şeffaflık mimarisi
│   ├── collaborative_architecture.md # İnsan-AI mimarisi
│   └── cross_modal_architecture.md # Çoklu-modal mimari
├── integration/                    # Diğer sistemlerle entegrasyon
│   ├── with-rag.md                 # Geri getirme entegrasyonu
│   ├── with-memory.md              # Bellek sistemi entegrasyonu
│   ├── with-agents.md              # Ajan sistemi entegrasyonu
│   ├── evaluation-metrics.md       # Değerlendirme yöntemleri
│   ├── with-fields.md              # Alan teorisi entegrasyonu
│   ├── with-quantum.md             # Kuantum semantik entegrasyonu
│   ├── with-unified.md             # Birleşik alan entegrasyonu
│   ├── with-meta-recursion.md      # Öz-gelişim entegrasyonu
│   ├── with-interpretability.md    # Şeffaflık entegrasyonu
│   ├── with-collaboration.md       # İnsan-AI entegrasyonu
│   └── with-cross-modal.md         # Çoklu-modal entegrasyon
└── meta-cognition/                 # Meta-bilişsel yetenekler
    ├── self-reflection.md          # Öz-analiz sistemleri
    ├── recursive-improvement.md    # Öz-geliştirme yöntemleri
    ├── meta-awareness.md           # Sistem öz-farkındalığı
    ├── attribution-engines.md      # Nedensel atıf sistemleri
    ├── symbolic-echo-processing.md # Sembolik kalıp işleme
    ├── meta-interpretability.md    # Meta-seviye şeffaflık
    ├── meta-collaboration.md       # Meta-seviye insan-AI ortaklığı
    └── meta-modal-integration.md   # Meta-seviye modal entegrasyon
```

## Bilişsel Araçlar Neden Önemli

Araştırmalar, akıl yürütmeyi bilişsel araçlarla yapılandırmanın model performansını dramatik şekilde artırabileceğini göstermiştir:

- **Performans**: Matematiksel akıl yürütme kıyaslamalarında %16.6'ya kadar gelişme
- **Güvenilirlik**: Akıl yürütme hatalarında ve halüsinasyonlarda önemli azalma
- **Verimlilik**: Daha az toplam token ile daha iyi sonuçlar
- **Esneklik**: Matematikten yaratıcı yazıma kadar alanlarda uygulanabilir

## Hızlı Başlangıç

Bir bilişsel araç kullanmak için, görevinizle eşleşen bir şablonu `cognitive-templates/` klasöründen seçin:

```python
# Örnek: "soruyu_anla" bilişsel aracını kullanma
from cognitive_tools.templates import understand_question

problem = "Bir tren saatte 60 mil hızla 2.5 saat giderse, ne kadar yol kat eder?"
understanding = llm.generate(understand_question(problem))
print(understanding)
```

Daha karmaşık akıl yürütme için, `cognitive-programs/` klasöründen yapılandırılmış istem programları kullanın:

```python
# Örnek: Çok adımlı akıl yürütme programı kullanma
from cognitive_tools.programs import solve_math_problem

problem = "Bir tren saatte 60 mil hızla 2.5 saat giderse, ne kadar yol kat eder?"
solution = solve_math_problem(problem, llm=my_llm_interface)
print(solution.steps)  # Adım adım akıl yürütmeyi görüntüle
print(solution.answer)  # Nihai cevabı görüntüle
```

## Dizin Yapısı

- `cognitive-templates/`: Farklı akıl yürütme işlemleri için yeniden kullanılabilir şablonlar
- `cognitive-programs/`: Kod benzeri kalıplarla yapılandırılmış istem programları
- `cognitive-schemas/`: Farklı alanlar için bilgi temsil formatları
- `cognitive-architectures/`: Birden fazla aracı birleştiren tam akıl yürütme sistemleri
- `integration/`: Diğer bileşenlerle (RAG, bellek, vb.) entegrasyon rehberleri

## Öğrenme Yolu

1. **Şablonlarla başlayın**: Temel bilişsel işlemleri öğrenin
2. **Programları keşfedin**: İşlemlerin akıl yürütme akışlarında nasıl birleştirilebileceğini görün
3. **Şemaları inceleyin**: Bilgiyi etkili şekilde nasıl yapılandıracağınızı anlayın
4. **Mimarilerde ustalaşın**: Tam akıl yürütme sistemleri kurun
5. **Bileşenleri entegre edin**: RAG, bellek ve diğer bağlam mühendisliği bileşenleriyle birleştirin

## Etkinliği Ölçme

Bilişsel araçların belirli görevlerinizdeki etkisini her zaman ölçün:

```python
# Örnek: Performans gelişimini ölçme
from cognitive_tools.evaluation import measure_reasoning_quality

baseline_score = measure_reasoning_quality(problem, baseline_prompt)
tool_score = measure_reasoning_quality(problem, cognitive_tool_prompt)

improvement = (tool_score / baseline_score - 1) * 100
print(f"Bilişsel araç performansı %{improvement:.1f} artırdı")
```

## Araştırma Temeli

Bu araçlar şu araştırmalara dayanmaktadır:

- Brown et al. (2025): "Dil Modellerinde Bilişsel Araçlarla Akıl Yürütmeyi Ortaya Çıkarma"
- Wei et al. (2023): "Düşünce Zinciri İstemleme Büyük Dil Modellerinde Akıl Yürütmeyi Ortaya Çıkarır"
- Huang et al. (2022): "İç Monolog: Dil Modellerinde Bilgi ve Akıl Yürütmeyi Somutlaştırma"

## Katkıda Bulunma

İyi çalışan yeni bir bilişsel araç kalıbınız var mı? Şablonlarınızı, programlarınızı veya mimarilerinizi göndermek için [CONTRIBUTING.md](../../.github/CONTRIBUTING.md) rehberini görün.

## Sonraki Adımlar

- Temel anlama araçları için [understanding.md](./cognitive-templates/understanding.md) dosyasına bakın
- Temel program yapıları için [basic-programs.md](./cognitive-programs/basic-programs.md) dosyasını deneyin
- Tam problem çözme sistemi için [solver-architecture.md](./cognitive-architectures/solver-architecture.md) dosyasını keşfedin
