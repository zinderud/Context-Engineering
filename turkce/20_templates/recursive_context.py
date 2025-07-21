
Bağlam Mühendisliği için Özyinelemeli Bağlam Çerçevesi
------------------------------------------

Bu modül, kendilerini genişletebilen, iyileştirebilen ve geliştirebilen özyinelemeli bağlamları
uygulamak için bir çerçeve sağlar. Nöral alan kavramlarını protokol kabukları ve
kendi kendini geliştirme mekanizmalarıyla birleştirerek, özyinelemeli yinelemelerle daha
etkili hale gelen bağlamlar oluşturur.

Anahtar yetenekler:
1. Kendi üzerine düşünme ve iç gözlem
2. Özyinelemeli kendi kendini geliştirme
3. Nöral alan entegrasyonu
4. Protokol kabuğu düzenlemesi
5. Sembolik kalıntı izleme
6. Atıf ve yorumlanabilirlik

Kullanım:
    # Temel bir özyinelemeli çerçeve oluştur
    framework = RecursiveFramework(
        description="Matematiksel problem çözücü",
        model="gpt-4"
    )
    
    # Kendi kendini geliştirme döngüsü ekle
    framework.add_self_improvement_loop(
        evaluation_metric="çözüm_doğruluğu",
        improvement_strategy="adım_iyileştirme"
    )
    
    # Özyinelemeli iyileştirme ile yürüt
    result = framework.execute_recursive(
        "x için çöz: 3x + 7 = 22",
        max_iterations=3
    )


import time
import json
import logging
import re
import math
import copy
from typing import Dict, List, Any, Optional, Union, Callable, Tuple, Set
from enum import Enum
from abc import ABC, abstractmethod

# Günlüğe kaydetmeyi yapılandır
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("recursive_framework")

# ------------------------------------------------------------------------------
# Temel Model Arayüzü
# ------------------------------------------------------------------------------

class ModelInterface(ABC):
    """Dil modeli arayüzleri için soyut temel sınıf."""
    
    @abstractmethod
    def generate(self, context: str, max_tokens: int = 1000) -> str:
        """Bir bağlam verildiğinde modelden bir yanıt üretir."""
        pass

class OpenAIInterface(ModelInterface):
    """Dil modelleri için OpenAI API arayüzü."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """
        OpenAI arayüzünü başlatır.
        
        Args:
            model_name: Kullanılacak OpenAI modelinin adı
            api_key: OpenAI API anahtarı (ortamda ayarlanmışsa isteğe bağlı)
        """
        try:
            import openai
            self.openai = openai
            if api_key:
                openai.api_key = api_key
            self.model_name = model_name
        except ImportError:
            raise ImportError("OpenAI paketi kurulu değil. 'pip install openai' ile kurun")
    
    def generate(self, context: str, max_tokens: int = 1000) -> str:
        """OpenAI API'sini kullanarak bir yanıt üretir."""
        try:
            response = self.openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": context}],
                max_tokens=max_tokens,
                n=1,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API hatası: {e}")
            raise

class AnthropicInterface(ModelInterface):
    """Claude modelleri için Anthropic API arayüzü."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """
        Anthropic arayüzünü başlatır.
        
        Args:
            model_name: Kullanılacak Anthropic modelinin adı
            api_key: Anthropic API anahtarı (ortamda ayarlanmışsa isteğe bağlı)
        """
        try:
            import anthropic
            self.anthropic = anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model_name = model_name
        except ImportError:
            raise ImportError("Anthropic paketi kurulu değil. 'pip install anthropic' ile kurun")
    
    def generate(self, context: str, max_tokens: int = 1000) -> str:
        """Anthropic API'sini kullanarak bir yanıt üretir."""
        try:
            response = self.client.completion(
                model=self.model_name,
                prompt=f"\n\nİnsan: {context}\n\nAsistan:",
                max_tokens_to_sample=max_tokens,
                temperature=0.7,
            )
            return response.completion
        except Exception as e:
            logger.error(f"Anthropic API hatası: {e}")
            raise

# ------------------------------------------------------------------------------
# Nöral Alan Bileşenleri
# ------------------------------------------------------------------------------

class NeuralField:
    """
    Özyinelemeli bağlam mühendisliği için nöral alan uygulaması.
    Bağlamı ayrık jetonlar yerine sürekli bir alan olarak ele alır.
    """
    
    def __init__(self, 
                 decay_rate: float = 0.05,
                 boundary_permeability: float = 0.8,
                 resonance_bandwidth: float = 0.6,
                 attractor_formation_threshold: float = 0.7):
        """
        Nöral alanı başlatır.
        
        Args:
            decay_rate: Desen bozulmasının temel oranı
            boundary_permeability: Yeni bilgilerin ne kadar kolay girdiği
            resonance_bandwidth: Desenlerin ne kadar geniş rezonansa girdiği
            attractor_formation_threshold: Çekici oluşumu için eşik
        """
        self.state = {}  # Alan durumu
        self.attractors = {}  # Kararlı çekiciler
        self.history = []  # Alan evrim geçmişi
        
        # Alan özellikleri
        self.decay_rate = decay_rate
        self.boundary_permeability = boundary_permeability
        self.resonance_bandwidth = resonance_bandwidth
        self.attractor_threshold = attractor_formation_threshold
    
    def inject(self, pattern: str, strength: float = 1.0) -> 'NeuralField':
        """
        Alana yeni bir desen ekler.
        
        Args:
            pattern: Enjekte edilecek bilgi deseni
            strength: Desenin gücü
            
        Returns:
            Zincirleme için kendisi
        """
        # Sınır filtrelemesi uygula
        effective_strength = strength * self.boundary_permeability
        
        # Mevcut çekicilerle rezonansı kontrol et
        for attractor_id, attractor in self.attractors.items():
            resonance = self._calculate_resonance(pattern, attractor['pattern'])
            if resonance > 0.2:
                # Çekici, deseni kendine doğru çeker
                pattern = self._blend_patterns(
                    pattern, 
                    attractor['pattern'],
                    blend_ratio=resonance * 0.3
                )
                # Çekiciyi güçlendir
                self.attractors[attractor_id]['strength'] += resonance * 0.1
        
        # Alan durumunu yeni desenle güncelle
        if pattern in self.state:
            self.state[pattern] += effective_strength
        else:
            self.state[pattern] = effective_strength
            
        # Geçmişi kaydet
        self.history.append(("inject", pattern, effective_strength))
        
        # Çekici oluşumunu kontrol et
        if pattern in self.state and self.state[pattern] > self.attractor_threshold:
            self._form_attractor(pattern)
        
        # Rezonans etkilerini işle
        self._process_resonance(pattern)
        
        return self
    
    def _form_attractor(self, pattern: str) -> str:
        """
        Güçlü bir desen etrafında yeni bir çekici oluşturur.
        
        Args:
            pattern: Etrafında çekici oluşturulacak desen
            
        Returns:
            Oluşturulan çekicinin kimliği
        """
        attractor_id = f"attractor_{len(self.attractors)}"
        self.attractors[attractor_id] = {
            'pattern': pattern,
            'strength': self.state[pattern],
            'formation_time': len(self.history),
            'basin_width': self.resonance_bandwidth
        }
        return attractor_id
    
    def _process_resonance(self, trigger_pattern: str) -> 'NeuralField':
        """
        Bir tetikleyici desenden gelen rezonans etkilerini işler.
        
        Args:
            trigger_pattern: Rezonansı tetikleyen desen
            
        Returns:
            Zincirleme için kendisi
        """
        # Her mevcut desen için, tetikleyici ile rezonansı hesapla
        resonance_effects = {}
        for pattern, strength in self.state.items():
            if pattern != trigger_pattern:
                resonance = self._calculate_resonance(pattern, trigger_pattern)
                effect = resonance * strength * 0.2
                resonance_effects[pattern] = effect
        
        # Rezonans etkilerini uygula
        for pattern, effect in resonance_effects.items():
            self.state[pattern] += effect
        
        return self
    
    def decay(self) -> 'NeuralField':
        """
        Tüm desenlere doğal bozulma uygular.
        
        Returns:
            Zincirleme için kendisi
        """
        # Alan durumuna bozulma uygula
        for pattern in list(self.state.keys()):
            # Çekicilerle rezonansa giren desenler daha yavaş bozulur
            attractor_protection = 0
            for attractor in self.attractors.values():
                resonance = self._calculate_resonance(pattern, attractor['pattern'])
                attractor_protection += resonance * 0.5
            
            effective_decay = self.decay_rate * (1 - min(attractor_protection, 0.9))
            self.state[pattern] *= (1 - effective_decay)
            
        # Çekicilere minimal bozulma uygula
        for attractor_id in list(self.attractors.keys()):
            self.attractors[attractor_id]['strength'] *= (1 - self.decay_rate * 0.2)
            
        # Eşiğin altına düşen desenleri kaldır
        self.state = {k: v for k, v in self.state.items() if v > 0.01}
        self.attractors = {k: v for k, v in self.attractors.items() if v['strength'] > 0.1}
        
        return self
    
    def _calculate_resonance(self, pattern1: str, pattern2: str) -> float:
        """
        İki desen arasındaki rezonansı hesaplar.
        
        Args:
            pattern1: Birinci desen
            pattern2: İkinci desen
            
        Returns:
            Rezonans puanı (0.0 ile 1.0 arası)
        """
        # Basit kelime örtüşme benzerliği
        words1 = set(pattern1.lower().split())
        words2 = set(pattern2.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        overlap = len(words1.intersection(words2))
        similarity = overlap / max(len(words1), len(words2))
        
        # Bant genişliği modülasyonu uygula
        resonance = similarity * self.resonance_bandwidth
        
        return resonance
    
    def _blend_patterns(self, pattern1: str, pattern2: str, blend_ratio: float) -> str:
        """
        İki deseni orana göre karıştırır.
        
        Args:
            pattern1: Birinci desen
            pattern2: İkinci desen
            blend_ratio: Karıştırma oranı (0.0 ile 1.0 arası)
            
        Returns:
            Karıştırılmış desen
        """
        # Ağırlıklandırma göstergesi ile basit birleştirme
        return f"{pattern1} {blend_ratio:.2f}↔️ {pattern2}"
    
    def measure_field_stability(self) -> float:
        """
        Alanın ne kadar kararlı olduğunu ölçer.
        
        Returns:
            Kararlılık puanı (0.0 ile 1.0 arası)
        """
        if not self.attractors:
            return 0.0
        
        # Ortalama çekici gücünü ölç
        avg_strength = sum(a['strength'] for a in self.attractors.values()) / len(self.attractors)
        
        # Çekiciler etrafındaki desen organizasyonunu ölç
        organization = 0
        for pattern, strength in self.state.items():
            best_resonance = max(
                self._calculate_resonance(pattern, a['pattern']) 
                for a in self.attractors.values()
            ) if self.attractors else 0
            
            organization += best_resonance * strength
            
        if self.state:
            organization /= sum(self.state.values())
        else:
            organization = 0
        
        # Metrikleri birleştir
        stability = (avg_strength * 0.6) + (organization * 0.4)
        return min(1.0, stability)  # 1.0'da sınırla
    
    def get_context_representation(self) -> str:
        """
        Mevcut alan durumunun bir dize temsilini alır.
        
        Returns:
            Alanın dize temsili
        """
        parts = []
        
        # Çekicileri ekle
        if self.attractors:
            parts.append("# Alan Çekicileri")
            for attractor_id, attractor in self.attractors.items():
                parts.append(f"- {attractor_id} (Güç: {attractor['strength']:.2f}): {attractor['pattern'][:100]}...")
            parts.append("")
        
        # En aktif desenleri ekle
        parts.append("# Aktif Desenler")
        active_patterns = sorted(self.state.items(), key=lambda x: x[1], reverse=True)[:5]
        for pattern, strength in active_patterns:
            parts.append(f"- ({strength:.2f}): {pattern[:100]}...")
        
        # Alan metriklerini ekle
        parts.append("")
        parts.append(f"Alan Kararlılığı: {self.measure_field_stability():.2f}")
        parts.append(f"Aktif Desenler: {len(self.state)}")
        parts.append(f"Çekici Sayısı: {len(self.attractors)}")
        
        return "\n".join(parts)

# ------------------------------------------------------------------------------
# Sembolik Kalıntı Bileşenleri
# ------------------------------------------------------------------------------

class SymbolicResidue:
    """Nöral alandaki bir sembolik kalıntı parçasını temsil eder."""
    
    def __init__(self, 
                 content: str,
                 source: str,
                 strength: float = 1.0,
                 state: str = "surfaced"):
        """
        Bir sembolik kalıntıyı başlatır.
        
        Args:
            content: Kalıntının içeriği/deseni
            source: Kalıntının nereden kaynaklandığı
            strength: Başlangıç gücü
            state: Kalıntının mevcut durumu (yüzeye çıkarılmış, entegre edilmiş, yankı)
        """
        self.content = content
        self.source = source
        self.strength = strength
        self.state = state
        self.timestamp = time.time()
        self.id = f"residue_{hash(content)}_{int(self.timestamp)}"
        self.interactions = []
    
    def interact(self, target: str, interaction_type: str, strength_delta: float) -> None:
        """Başka bir öğeyle bir etkileşimi kaydeder."""
        self.interactions.append({
            "target": target,
            "type": interaction_type,
            "strength_delta": strength_delta,
            "timestamp": time.time()
        })
        
        # Gücü güncelle
        self.strength += strength_delta
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlük temsiline dönüştürür."""
        return {
            "id": self.id,
            "content": self.content,
            "source": self.source,
            "strength": self.strength,
            "state": self.state,
            "timestamp": self.timestamp,
            "interactions": self.interactions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SymbolicResidue':
        """Sözlük temsilinden oluşturur."""
        residue = cls(
            content=data["content"],
            source=data["source"],
            strength=data["strength"],
            state=data["state"]
        )
        residue.id = data["id"]
        residue.timestamp = data["timestamp"]
        residue.interactions = data.get("interactions", [])
        return residue

class SymbolicResidueTracker:
    """Nöral alanlardaki sembolik kalıntıyı izler ve yönetir."""
    
    def __init__(self):
        """Kalıntı izleyiciyi başlatır."""
        self.residues: Dict[str, SymbolicResidue] = {}
        self.history: List[Dict[str, Any]] = []
    
    def surface(self, content: str, source: str, strength: float = 1.0) -> str:
        """
        Yeni bir sembolik kalıntıyı yüzeye çıkarır.
        
        Args:
            content: Kalıntının içeriği/deseni
            source: Kalıntının nereden kaynaklandığı
            strength: Başlangıç gücü
            
        Returns:
            Yüzeye çıkarılan kalıntının kimliği
        """
        residue = SymbolicResidue(content, source, strength)
        self.residues[residue.id] = residue
        
        self.history.append({
            "action": "surface",
            "residue_id": residue.id,
            "timestamp": time.time()
        })
        
        return residue.id
    
    def integrate(self, residue_id: str, target: str, strength_delta: float = 0.5) -> None:
        """
        Bir kalıntıyı bir hedefe entegre eder.
        
        Args:
            residue_id: Entegre edilecek kalıntının kimliği
            target: Entegre edilecek hedef
            strength_delta: Entegrasyondan kaynaklanan güç değişikliği
        """
        if residue_id not in self.residues:
            raise ValueError(f"Kalıntı {residue_id} bulunamadı")
        
        residue = self.residues[residue_id]
        residue.state = "integrated"
        residue.interact(target, "integration", strength_delta)
        
        self.history.append({
            "action": "integrate",
            "residue_id": residue_id,
            "target": target,
            "timestamp": time.time()
        })
    
    def echo(self, residue_id: str, target: str, strength_delta: float = -0.2) -> None:
        """
        Bir kalıntının yankısını oluşturur.
        
        Args:
            residue_id: Yankılanacak kalıntının kimliği
            target: Yankının hedefi
            strength_delta: Yankıdan kaynaklanan güç değişikliği
        """
        if residue_id not in self.residues:
            raise ValueError(f"Kalıntı {residue_id} bulunamadı")
        
        residue = self.residues[residue_id]
        residue.state = "echo"
        residue.interact(target, "echo", strength_delta)
        
        self.history.append({
            "action": "echo",
            "residue_id": residue_id,
            "target": target,
            "timestamp": time.time()
        })
    
    def get_active_residues(self, min_strength: float = 0.5) -> List[SymbolicResidue]:
        """Belirtilen güç eşiğinin üzerindeki aktif kalıntıları alır."""
        return [r for r in self.residues.values() if r.strength >= min_strength]
    
    def get_residues_by_state(self, state: str) -> List[SymbolicResidue]:
        """Belirtilen durumdaki kalıntıları alır."""
        return [r for r in self.residues.values() if r.state == state]
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlük temsiline dönüştürür."""
        return {
            "residues": {rid: r.to_dict() for rid, r in self.residues.items()},
            "history": self.history
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SymbolicResidueTracker':
        """Sözlük temsilinden oluşturur."""
        tracker = cls()
        
        for rid, rdata in data.get("residues", {}).items():
            tracker.residues[rid] = SymbolicResidue.from_dict(rdata)
        
        tracker.history = data.get("history", [])
        return tracker

# ------------------------------------------------------------------------------
# Protokol Kabuğu Bileşenleri
# ------------------------------------------------------------------------------

class ProtocolShell:
    """
    Yapılandırılmış bağlam işlemlerini tanımlamak için protokol kabuğu.
    Context-Engineering projesindeki pareto-lang formatına dayanmaktadır.
    """
    
    def __init__(self, 
                 intent: str,
                 input_params: Dict[str, Any] = None,
                 process_steps: List[Dict[str, Any]] = None,
                 output_schema: Dict[str, Any] = None,
                 meta: Dict[str, Any] = None):
        """
        Protokol kabuğunu başlatır.
        
        Args:
            intent: Protokolün amacı veya hedefi
            input_params: Girdi parametreleri ve yapısı
            process_steps: Yürütülecek süreç adımları listesi
            output_schema: Beklenen çıktı yapısı
            meta: Protokol hakkında meta veriler
        """
        self.intent = intent
        self.input_params = input_params or {}
        self.process_steps = process_steps or []
        self.output_schema = output_schema or {}
        self.meta = meta or {
            "name": "protocol",
            "version": "1.0.0",
            "timestamp": time.time()
        }
        
        # Yürütme durumu
        self.state = {
            "status": "initialized",
            "step_index": 0,
            "error": None,
            "output": {},
            "log": []
        }
    
    def format(self) -> str:
        """
        Protokol kabuğunu pareto-lang formatında bir dize olarak biçimlendirir.
        
        Returns:
            Biçimlendirilmiş protokol dizesi
        """
        parts = []
        
        # Protokol adı (varsa meta verilerden türetilir)
        protocol_name = self.meta.get("name", "protocol")
        parts.append(f"/{protocol_name}{{")
        
        # Niyet
        parts.append(f'    intent="{self.intent}",')
        
        # Girdi parametreleri
        parts.append("    input={")
        for key, value in self.input_params.items():
            if isinstance(value, str):
                parts.append(f'        {key}="{value}",')
            else:
                parts.append(f"        {key}={value},")
        parts.append("    },")
        
        # Süreç adımları
        parts.append("    process=[")
        for step in self.process_steps:
            step_name = next(iter(step)) if isinstance(step, dict) else step
            
            if isinstance(step, dict):
                parts.append(f"        /{step_name}{{")
                
                step_content = step[step_name]
                if isinstance(step_content, dict):
                    for k, v in step_content.items():
                        if isinstance(v, str):
                            parts.append(f'            {k}="{v}",')
                        else:
                            parts.append(f"            {k}={v},")
                elif isinstance(step_content, list):
                    content_str = ", ".join(f'"{item}"' if isinstance(item, str) else str(item) for item in step_content)
                    parts.append(f"            {content_str}")
                else:
                    if isinstance(step_content, str):
                        parts.append(f'            "{step_content}"')
                    else:
                        parts.append(f"            {step_content}")
                
                parts.append("        },")
            else:
                parts.append(f"        {step},")
        parts.append("    ],")
        
        # Çıktı şeması
        parts.append("    output={")
        for key, value in self.output_schema.items():
            if isinstance(value, str):
                parts.append(f'        {key}="{value}",')
            else:
                parts.append(f"        {key}={value},")
        parts.append("    },")
        
        # Meta
        parts.append("    meta={")
        for key, value in self.meta.items():
            if isinstance(value, str):
                parts.append(f'        {key}="{value}",')
            else:
                parts.append(f"        {key}={value},")
        parts.append("    }")
        
        # Protokolü kapat
        parts.append("}")
        
        return "\n".join(parts)
    
    def execute(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Protokol adımlarını yürütür.
        Bu, değişkenleri çözmek için bağlamı kullanan basitleştirilmiş bir yürütmedir.
        
        Args:
            context: Yürütme bağlamı
            
        Returns:
            Çıktı sözlüğü
        """
        context = context or {}
        self.state["status"] = "running"
        self.state["log"].append(f"'{self.meta.get('name', 'protocol')}' protokolünün yürütülmesi başlatılıyor")
        
        try:
            # Girdi parametrelerini işle
            processed_inputs = {}
            for key, value in self.input_params.items():
                if isinstance(value, str) and value.startswith("<") and value.endswith(">"):
                    # Bu bir değişken referansıdır
                    var_name = value[1:-1]
                    if var_name in context:
                        processed_inputs[key] = context[var_name]
                    else:
                        self.state["log"].append(f"Uyarı: {var_name} değişkeni bağlamda bulunamadı")
                        processed_inputs[key] = None
                else:
                    processed_inputs[key] = value
            
            # Süreç adımlarını yürüt
            step_results = []
            for i, step in enumerate(self.process_steps):
                self.state["step_index"] = i
                step_name = next(iter(step)) if isinstance(step, dict) else step
                self.state["log"].append(f"{i+1}/{len(self.process_steps)} adımı yürütülüyor: {step_name}")
                
                # Adımı yürüt (basitleştirilmiş simülasyon)
                # Tam bir uygulamada, bu her adımı yorumlar ve yürütürdü
                result = {
                    "step": step_name,
                    "status": "completed",
                    "output": f"{step_name} öğesinin simüle edilmiş yürütülmesi"
                }
                
                step_results.append(result)
            
            # Çıktıyı hazırla
            output = {}
            for key in self.output_schema:
                if key in context:
                    output[key] = context[key]
                else:
                    output[key] = f"<simulated_{key}>"
            
            self.state["output"] = output
            self.state["status"] = "completed"
            
        except Exception as e:
            self.state["status"] = "error"
            self.state["error"] = str(e)
            self.state["log"].append(f"Hata: {str(e)}")
        
        return {
            "status": self.state["status"],
            "output": self.state["output"],
            "log": self.state["log"],
            "error": self.state["error"]
        }

# ------------------------------------------------------------------------------
# Özyinelemeli Çerçeve Çekirdeği
# ------------------------------------------------------------------------------

class RecursiveFramework:
    """
    Kendi kendini geliştiren özyinelemeli bağlamları uygulamak için çerçeve.
    Nöral alanları, protokol kabuklarını ve sembolik kalıntı izlemeyi birleştirir.
    """
    
    def __init__(self, 
                 description: str,
                 model: Union[str, ModelInterface],
                 field_params: Dict[str, Any] = None,
                 protocol_template: Dict[str, Any] = None,
                 recursion_depth: int = 3,
                 verbose: bool = False):
        """
        Özyinelemeli çerçeveyi başlatır.
        
        Args:
            description: Çerçevenin amacının açıklaması
            model: Model adı veya ModelInterface örneği
            field_params: Nöral alan için parametreler
            protocol_template: Protokol kabukları için şablon
            recursion_depth: Maksimum özyineleme derinliği
            verbose: Ayrıntılı bilgilerin günlüğe kaydedilip kaydedilmeyeceği
        """
        self.description = description
        self.recursion_depth = recursion_depth
        self.verbose = verbose
        
        # Modeli ayarla
        if isinstance(model, str):
            if "gpt" in model.lower():
                self.model = OpenAIInterface(model)
            elif "claude" in model.lower():
                self.model = AnthropicInterface(model)
            else:
                raise ValueError(f"Bilinmeyen model türü: {model}")
        else:
            self.model = model
        
        # Nöral alanı ayarla
        field_params = field_params or {}
        self.field = NeuralField(
            decay_rate=field_params.get('decay_rate', 0.05),
            boundary_permeability=field_params.get('boundary_permeability', 0.8),
            resonance_bandwidth=field_params.get('resonance_bandwidth', 0.6),
            attractor_formation_threshold=field_params.get('attractor_threshold', 0.7)
        )
        
        # Kalıntı izleyiciyi ayarla
        self.residue_tracker = SymbolicResidueTracker()
        
        # Protokol şablonunu ayarla
        self.protocol_template = protocol_template or {
            "intent": "Bilgiyi özyinelemeli olarak işle",
            "input": {
                "current_input": "<current_input>",
                "field_state": "<field_state>",
                "recursion_level": "<recursion_level>"
            },
            "process": [
                {
                    "analyze.input": {
                        "understand": "core request"
                    }
                },
                {
                    "process.field": {
                        "measure": ["resonance", "coherence", "stability"]
                    }
                },
                {
                    "generate.response": {
                        "style": "clear and helpful"
                    }
                },
                {
                    "self.improve": {
                        "target": "response quality"
                    }
                }
            ],
            "output": {
                "response": "<generated_response>",
                "field_update": "<field_update_suggestions>",
                "improvement": "<improvement_suggestions>"
            },
            "meta": {
                "name": "recursive_framework",
                "version": "1.0.0"
            }
        }
        
        # Yürütme durumu
        self.current_recursion_level = 0
        self.execution_trace = []
        self.improvement_history = []
        
        # Alanı temel kavramlarla başlat
        self._initialize_field()
    
    def _initialize_field(self) -> None:
        """Nöral alanı temel kavramlarla başlatır."""
        # Temel çekicileri ekle
        core_attractors = [
            (f"Bu çerçevenin amacı {self.description}", 0.9),
            ("Özyinelemeli iyileştirme daha iyi sonuçlara yol açar", 0.8),
            ("Bağlam, geri bildirime göre gelişmelidir", 0.8),
            ("Nöral alanlar sürekli bağlam temsilini sağlar", 0.7),
            ("Sembolik kalıntı, ince anlam parçalarını yakalar", 0.7)
        ]
        
        for pattern, strength in core_attractors:
            self.field.inject(pattern, strength)
            # Açıkça çekici oluştur
            self.field._form_attractor(pattern)
            
            # Sembolik kalıntı olarak yüzeye çıkar
            self.residue_tracker.surface(pattern, "initialization", strength)
    
    def add_attractor(self, pattern: str, strength: float = 1.0) -> None:
        """
        Nöral alana bir çekici ekler.
        
        Args:
            pattern: Çekici deseni
            strength: Çekici gücü
        """
        # Çekici oluşturmak için yüksek güçle enjekte et
        self.field.inject(pattern, strength)
        
        # Açıkça çekici oluştur
        self.field._form_attractor(pattern)
        
        # Sembolik kalıntı olarak yüzeye çıkar
        self.residue_tracker.surface(pattern, "manual_addition", strength)
    
    def add_self_improvement_strategy(self, 
                                     strategy_name: str,
                                     strategy_description: str,
                                     strategy_prompt: str) -> None:
        """
        Bir kendi kendini geliştirme stratejisi ekler.
        
        Args:
            strategy_name: Stratejinin adı
            strategy_description: Stratejinin açıklaması
            strategy_prompt: Strateji için istem şablonu
        """
        # Çekici olarak ekle
        pattern = f"Kendi kendini geliştirme stratejisi: {strategy_name} - {strategy_description}"
        self.add_attractor(pattern, strength=0.8)
        
        # Stratejiyi sakla
        if not hasattr(self, "self_improvement_strategies"):
            self.self_improvement_strategies = {}
        self.self_improvement_strategies[strategy_name] = strategy_prompt
