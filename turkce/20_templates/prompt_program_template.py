
İstem Programı Şablonu
----------------------

Bu şablon, istem programları oluşturmak için yapılandırılmış bir çerçeve sağlar -
LLM akıl yürütmesini açık, adım adım talimatlarla yönlendirmek için kod benzeri yapılar.
İstem programları, doğal dilin esnekliğini programlama yapılarının titizliğiyle birleştirir.

Anahtar özellikler:
1. Oluşturulabilen modüler istem bileşenleri
2. Kontrol akışı yapıları (if/else, döngüler)
3. Bağlam takibi için değişken yönetimi
4. Açık akıl yürütme adımları
5. Hata işleme ve geri dönüş mantığı
6. Kalıcılık için nöral alanlarla entegrasyon

Kullanım:
    # Temel bir istem programı oluştur
    program = PromptProgram("Matematiksel kelime problemlerini adım adım çöz")
    
    # Akıl yürütme adımları ekle
    program.add_step("Değişkenleri ve ilişkileri belirlemek için problemi ayrıştır")
    program.add_step("Uygun denklemleri kur")
    program.add_step("Bilinmeyen değişkenleri çöz")
    program.add_step("Çözümün orijinal bağlamda mantıklı olup olmadığını doğrula")
    
    # Programı yürüt
    result = program.execute("Bir tren saatte 60 mil hızla 2.5 saat giderse ne kadar yol alır?")


import re
import json
import time
import logging
from typing import Dict, List, Any, Optional, Union, Callable, Tuple
from enum import Enum

# Günlüğe kaydetmeyi yapılandır
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("prompt_program")

# ------------------------------------------------------------------------------
# İstem Programı Bileşenleri
# ------------------------------------------------------------------------------

class StepType(Enum):
    """Bir istem programındaki adım türleri."""
    INSTRUCTION = "talimat"  # Temel talimat adımı
    CONDITION = "koşul"      # Koşullu dal
    LOOP = "döngü"                # Yineleme
    VARIABLE = "değişken"        # Değişken ataması
    FUNCTION = "fonksiyon"        # Fonksiyon çağrısı
    ERROR = "hata"              # Hata işleme

class ProgramStep:
    """Bir istem programındaki tek bir adım."""
    
    def __init__(self, 
                 content: str, 
                 step_type: StepType = StepType.INSTRUCTION,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Bir program adımını başlatır.
        
        Args:
            content: Adımın içeriği
            step_type: Adımın türü
            metadata: Adım için ek meta veriler
        """
        self.content = content
        self.step_type = step_type
        self.metadata = metadata or {}
        self.substeps: List[ProgramStep] = []
    
    def add_substep(self, substep: 'ProgramStep') -> None:
        """Bu adıma bir alt adım ekler."""
        self.substeps.append(substep)
    
    def format(self, index: Optional[int] = None, indent: int = 0) -> str:
        """Adımı bir dize olarak biçimlendirir."""
        # Temel girinti
        indent_str = "  " * indent
        
        # Adım başlığı
        if index is not None:
            header = f"{indent_str}{index}. "
        else:
            header = f"{indent_str}- "
        
        # Adım türüne göre biçimlendir
        if self.step_type == StepType.INSTRUCTION:
            formatted = f"{header}{self.content}"
        elif self.step_type == StepType.CONDITION:
            condition = self.metadata.get("condition", "EĞER koşul")
            formatted = f"{header}EĞER {condition}:"
        elif self.step_type == StepType.LOOP:
            loop_var = self.metadata.get("variable", "öğe")
            loop_iterable = self.metadata.get("iterable", "öğeler")
            formatted = f"{header}HER {loop_var} İÇİN {loop_iterable}:"
        elif self.step_type == StepType.VARIABLE:
            var_name = self.metadata.get("name", "değişken")
            formatted = f"{header}AYARLA {var_name} = {self.content}"
        elif self.step_type == StepType.FUNCTION:
            func_name = self.metadata.get("name", "fonksiyon")
            formatted = f"{header}ÇAĞIR {func_name}({self.content})"
        elif self.step_type == StepType.ERROR:
            formatted = f"{header}HATA DURUMUNDA: {self.content}"
        else:
            formatted = f"{header}{self.content}"
        
        # Alt adımları ekle
        if self.substeps:
            substep_str = "\n".join(
                substep.format(i+1, indent+1) 
                for i, substep in enumerate(self.substeps)
            )
            formatted = f"{formatted}\n{substep_str}"
        
        return formatted

class PromptProgram:
    """
    LLM akıl yürütmesini yönlendirmek için yapılandırılmış bir program.
    Doğal dili programlama yapılarıyla birleştirir.
    """
    
    def __init__(self, 
                 description: str,
                 model: Optional[Any] = None,
                 variables: Optional[Dict[str, Any]] = None,
                 neural_field: Optional[Any] = None):
        """
        Bir istem programını başlatır.
        
        Args:
            description: Programın amacının açıklaması
            model: Dil modeli arayüzü (isteğe bağlı)
            variables: Başlangıç değişkenleri (isteğe bağlı)
            neural_field: Bağlam kalıcılığı için nöral alan (isteğe bağlı)
        """
        self.description = description
        self.model = model
        self.variables = variables or {}
        self.neural_field = neural_field
        
        self.steps: List[ProgramStep] = []
        self.error_handlers: List[ProgramStep] = []
        
        # Yürütme durumu
        self.current_step: int = 0
        self.execution_trace: List[Dict[str, Any]] = []
    
    def add_step(self, content: str, step_type: StepType = StepType.INSTRUCTION, 
                metadata: Optional[Dict[str, Any]] = None) -> ProgramStep:
        """
        Programa bir adım ekler.
        
        Args:
            content: Adımın içeriği
            step_type: Adımın türü
            metadata: Adım için ek meta veriler
            
        Returns:
            Oluşturulan adım
        """
        step = ProgramStep(content, step_type, metadata)
        self.steps.append(step)
        return step
    
    def add_condition(self, condition: str, true_step: str, 
                     false_step: Optional[str] = None) -> Tuple[ProgramStep, ProgramStep, Optional[ProgramStep]]:
        """
        Programa koşullu bir dal ekler.
        
        Args:
            condition: Değerlendirilecek koşul
            true_step: Koşul doğruysa yürütülecek adım
            false_step: Koşul yanlışsa yürütülecek adım (isteğe bağlı)
            
        Returns:
            (koşul_adımı, doğru_adımı, yanlış_adımı) demeti
        """
        # Koşul adımı oluştur
        condition_step = self.add_step(condition, StepType.CONDITION, {"condition": condition})
        
        # Doğru dalı oluştur
        true_branch = ProgramStep(true_step, StepType.INSTRUCTION)
        condition_step.add_substep(true_branch)
        
        # Sağlanırsa yanlış dalı oluştur
        false_branch = None
        if false_step:
            false_branch = ProgramStep(false_step, StepType.INSTRUCTION)
            condition_step.add_substep(false_branch)
        
        return condition_step, true_branch, false_branch
    
    def add_loop(self, variable: str, iterable: str, 
                body: str) -> Tuple[ProgramStep, ProgramStep]:
        """
        Programa bir döngü ekler.
        
        Args:
            variable: Döngü değişkeni adı
            iterable: Üzerinde döngü kurulacak yinelenebilir
            body: Döngü gövdesi içeriği
            
        Returns:
            (döngü_adımı, gövde_adımı) demeti
        """
        # Döngü adımı oluştur
        loop_step = self.add_step(f"{iterable} üzerinde döngü kur", StepType.LOOP, 
                                 {"variable": variable, "iterable": iterable})
        
        # Döngü gövdesi oluştur
        body_step = ProgramStep(body, StepType.INSTRUCTION)
        loop_step.add_substep(body_step)
        
        return loop_step, body_step
    
    def add_variable(self, name: str, value: str) -> ProgramStep:
        """
        Programa bir değişken ataması ekler.
        
        Args:
            name: Değişken adı
            value: Değişken değeri veya ifadesi
            
        Returns:
            Oluşturulan adım
        """
        return self.add_step(value, StepType.VARIABLE, {"name": name})
    
    def add_function(self, name: str, params: str) -> ProgramStep:
        """
        Programa bir fonksiyon çağrısı ekler.
        
        Args:
            name: Fonksiyon adı
            params: Fonksiyon parametreleri
            
        Returns:
            Oluşturulan adım
        """
        return self.add_step(params, StepType.FUNCTION, {"name": name})
    
    def add_error_handler(self, handler: str) -> ProgramStep:
        """
        Programa bir hata işleyici ekler.
        
        Args:
            handler: Hata işleme talimatı
            
        Returns:
            Oluşturulan adım
        """
        step = ProgramStep(handler, StepType.ERROR)
        self.error_handlers.append(step)
        return step
    
    def format(self) -> str:
        """Programı istemlerde kullanılmak üzere bir dize olarak biçimlendirir."""
        # Program başlığı
        parts = [
            f"# {self.description}",
            ""
        ]
        
        # Adımları biçimlendir
        if self.steps:
            parts.append("## Adımlar:")
            for i, step in enumerate(self.steps):
                parts.append(step.format(i+1))
        
        # Hata işleyicileri biçimlendir
        if self.error_handlers:
            parts.append("")
            parts.append("## Hata İşleme:")
            for handler in self.error_handlers:
                parts.append(handler.format())
        
        # Değişkenleri biçimlendir
        if self.variables:
            parts.append("")
            parts.append("## Başlangıç Bağlamı:")
            for name, value in self.variables.items():
                if isinstance(value, str):
                    parts.append(f"- {name} = \"{value}\"")
                else:
                    parts.append(f"- {name} = {value}")
        
        return "\n".join(parts)
    
    def execute(self, input_data: str, max_tokens: int = 1000) -> str:
        """
        İstem programını verilen girdiyle yürütür.
        
        Args:
            input_data: Program için girdi verileri
            max_tokens: Üretim için maksimum jeton sayısı
            
        Returns:
            Yürütme sonucu
        """
        if not self.model:
            raise ValueError("Yürütme için model sağlanmadı")
        
        # Yürütme durumunu sıfırla
        self.current_step = 0
        self.execution_trace = []
        
        # Programı biçimlendir
        program_str = self.format()
        
        # Varsa nöral alana enjekte et
        if self.neural_field:
            try:
                self.neural_field.inject(f"İstem Programı: {self.description}", strength=0.9)
                self.neural_field.inject(program_str, strength=0.8)
                
                # Girdiyi enjekte et
                self.neural_field.inject(f"Girdi: {input_data}", strength=1.0)
                
                # Bağlam için alan temsilini al
                field_context = self.neural_field.get_context_representation()
                
                # Alan bağlamı ile yürütme istemi oluştur
                prompt = f"""
{field_context}

# Girdi
{input_data}

# Program
{program_str}

# Yürütme
Lütfen yukarıdaki programı sağlanan girdiyi kullanarak adım adım yürütün.
Her adım için:
1. Akıl yürütmenizi gösterin
2. Sonucu gösterin
3. Herhangi bir değişkeni güncelleyin

Tüm adımları yürüttükten sonra son cevabınızı verin.
"""
            except (AttributeError, TypeError):
                logger.warning("Nöral alan kullanılamadı, standart isteme geri dönülüyor")
                # Standart isteme geri dön
                prompt = self._create_standard_prompt(program_str, input_data)
        else:
            # Nöral alan olmadan standart istem
            prompt = self._create_standard_prompt(program_str, input_data)
        
        # Programı yürüt
        try:
            response = self.model.generate(prompt, max_tokens=max_tokens)
            
            # Yürütmeyi kaydet
            self.execution_trace.append({
                "timestamp": time.time(),
                "prompt": prompt,
                "response": response
            })
            
            # Varsa nöral alanı güncelle
            if self.neural_field:
                try:
                    self.neural_field.inject(f"Yürütme Sonucu: {response}", strength=0.7)
                except (AttributeError, TypeError):
                    pass
            
            return response
        except Exception as e:
            logger.error(f"Yürütme başarısız oldu: {e}")
            
            # Varsa hata işleyicileri dene
            if self.error_handlers and hasattr(self.model, 'generate'):
                error_prompt = f"""
Program yürütmesi bir hatayla karşılaştı: {str(e)}

Lütfen aşağıdaki hata işlemeyi uygulayın:
"""
                for handler in self.error_handlers:
                    error_prompt += f"\n- {handler.content}"
                
                error_prompt += f"\n\nGirdi: {input_data}"
                
                try:
                    return self.model.generate(error_prompt, max_tokens=max_tokens)
                except Exception as e2:
                    logger.error(f"Hata işleyici başarısız oldu: {e2}")
            
            return f"Yürütme başarısız oldu: {str(e)}"
    
    def _create_standard_prompt(self, program_str: str, input_data: str) -> str:
        """Standart bir yürütme istemi oluşturur."""
        return f"""
# Girdi
{input_data}

# Program
{program_str}

# Yürütme
Lütfen yukarıdaki programı sağlanan girdiyi kullanarak adım adım yürütün.
Her adım için:
1. Akıl yürütmenizi gösterin
2. Sonucu gösterin
3. Herhangi bir değişkeni güncelleyin

Tüm adımları yürüttükten sonra son cevabınızı verin.
"""
    
    def execute_with_trace(self, input_data: str, max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Programı yürütür ve ayrıntılı yürütme izi döndürür.
        
        Args:
            input_data: Program için girdi verileri
            max_tokens: Üretim için maksimum jeton sayısı
            
        Returns:
            Yürütme sonuçları ve izi içeren sözlük
        """
        result = self.execute(input_data, max_tokens)
        
        # Sonuçtan yürütme izini ayrıştır
        steps_trace = self._parse_execution_trace(result)
        
        return {
            "input": input_data,
            "result": result,
            "steps_trace": steps_trace,
            "execution_trace": self.execution_trace
        }
    
    def _parse_execution_trace(self, result: str) -> List[Dict[str, Any]]:
        """Sonuçtan adım adım yürütme izini ayrıştırır."""
        steps = []
        
        # Numaralandırılmış adımları ara
        step_pattern = r'(?:Adım|adım) (\d+)[\s\.:]+(.+?)(?=(?:Adım|adım) \d+[\s\.:]+|$)'
        step_matches = re.findall(step_pattern, result, re.DOTALL)
        
        if step_matches:
            for step_num, step_content in step_matches:
                # Akıl yürütme ve sonucu ayırmaya çalış
                parts = re.split(r'(?:Sonuç|sonuç|Çıktı|çıktı)[\s\.:]+', step_content, 1)
                
                if len(parts) == 2:
                    reasoning, result_text = parts
                else:
                    reasoning = step_content
                    result_text = ""
                
                steps.append({
                    "step": int(step_num),
                    "reasoning": reasoning.strip(),
                    "result": result_text.strip()
                })
        else:
            # Net bir adım yapısı yok, sadece tüm sonucu döndür
            steps.append({
                "step": 1,
                "reasoning": "Tam yürütme",
                "result": result
            })
        
        return steps

# ------------------------------------------------------------------------------
# Nöral Alan Entegrasyonu
# ------------------------------------------------------------------------------

class NeuralFieldProgram(PromptProgram):
    """Gelişmiş nöral alan entegrasyonuna sahip istem programı."""
    
    def __init__(self, 
                 description: str,
                 model: Optional[Any] = None,
                 variables: Optional[Dict[str, Any]] = None,
                 neural_field: Optional[Any] = None,
                 field_params: Optional[Dict[str, Any]] = None):
        """
        Bir nöral alan istem programını başlatır.
        
        Args:
            description: Programın amacının açıklaması
            model: Dil modeli arayüzü
            variables: Başlangıç değişkenleri
            neural_field: Bağlam kalıcılığı için nöral alan
            field_params: Nöral alan parametreleri
        """
        super().__init__(description, model, variables)
        
        # Nöral alanı ayarla
        if neural_field:
            self.neural_field = neural_field
        elif field_params:
            # Döngüsel içe aktarmayı önlemek için burada içe aktar
            try:
                # Yerel modülden içe aktarmayı dene
                from .field_resonance_measure import ResidueEnhancedNeuralField
                self.neural_field = ResidueEnhancedNeuralField(**field_params)
            except (ImportError, AttributeError):
                try:
                    # Ayrı modül olarak dene
                    from field_resonance_measure import ResidueEnhancedNeuralField
                    self.neural_field = ResidueEnhancedNeuralField(**field_params)
                except (ImportError, AttributeError):
                    logger.warning("ResidueEnhancedNeuralField içe aktarılamadı, temel NeuralField kullanılıyor")
                    self.neural_field = self._create_basic_neural_field(field_params)
        else:
            self.neural_field = None
    
    def _create_basic_neural_field(self, params: Dict[str, Any]) -> Any:
        """Parametrelerden temel bir nöral alan oluşturur."""
        # Basit nöral alan uygulaması
        class BasicNeuralField:
            def __init__(self, decay_rate=0.05, boundary_permeability=0.8):
                self.state = {}
                self.attractors = {}
                self.decay_rate = decay_rate
                self.boundary_permeability = boundary_permeability
                self.history = []
            
            def inject(self, pattern, strength=1.0):
                # Sınır filtrelemesi uygula
                effective_strength = strength * self.boundary_permeability
                
                # Alan durumunu güncelle
                if pattern in self.state:
                    self.state[pattern] += effective_strength
                else:
                    self.state[pattern] = effective_strength
                
                # Geçmişi kaydet
                self.history.append(("inject", pattern, effective_strength))
                
                return self
            
            def decay(self):
                # Tüm desenlere bozulma uygula
                for pattern in list(self.state.keys()):
                    self.state[pattern] *= (1 - self.decay_rate)
                
                # Eşiğin altına düşen desenleri kaldır
                self.state = {k: v for k, v in self.state.items() if v > 0.01}
                
                return self
            
            def get_context_representation(self):
                parts = ["# Nöral Alan Durumu"]
                
                # Aktif desenleri ekle
                parts.append("## Aktif Desenler")
                for pattern, strength in sorted(self.state.items(), key=lambda x: x[1], reverse=True)[:5]:
                    short_pattern = (pattern[:50] + "...") if len(pattern) > 50 else pattern
                    parts.append(f"- ({strength:.2f}) {short_pattern}")
                
                return "\n".join(parts)
        
        return BasicNeuralField(
            decay_rate=params.get("decay_rate", 0.05),
            boundary_permeability=params.get("boundary_permeability", 0.8)
        )
    
    def add_resonance_step(self, description: str, patterns: List[str]) -> ProgramStep:
        """
        Alandaki belirli desenlerle rezonansa giren bir adım ekler.
        
        Args:
            description: Adım açıklaması
            patterns: Rezonansa girilecek desenler
            
        Returns:
            Oluşturulan adım
        """
        step = self.add_step(description, StepType.INSTRUCTION)
        
        # Desenleri alana enjekte et
        if self.neural_field:
            for pattern in patterns:
                try:
                    self.neural_field.inject(pattern, strength=0.7)
                except (AttributeError, TypeError):
                    pass
        
        return step
    
    def add_attractor(self, pattern: str, strength: float = 1.0) -> None:
        """
        Nöral alana bir çekici ekler.
        
        Args:
            pattern: Çekici deseni
            strength: Çekici gücü
        """
        if not self.neural_field:
            return
            
        try:
            # Çekici oluşturmak için yüksek güçle enjekte et
            self.neural_field.inject(pattern, strength=strength)
            
            # Yöntem varsa açıkça çekici oluştur
            if hasattr(self.neural_field, "_form_attractor"):
                self.neural_field._form_attractor(pattern)
            elif hasattr(self.neural_field, "attractors"):
                attractor_id = f"attractor_{len(self.neural_field.attractors)}"
                self.neural_field.attractors[attractor_id] = {
                    "pattern": pattern,
                    "strength": strength
                }
        except (AttributeError, TypeError) as e:
            logger.warning(f"Çekici eklenemedi: {e}")
    
    def execute(self, input_data: str, max_tokens: int = 1000) -> str:
        """
        Nöral alan programını verilen girdiyle yürütür.
        
        Args:
            input_data: Program için girdi verileri
            max_tokens: Üretim için maksimum jeton sayısı
            
        Returns:
            Yürütme sonucu
        """
        # Yürütmeden önce alan bozulmasını uygula
        if self.neural_field:
            try:
                self.neural_field.decay()
            except (AttributeError, TypeError):
                pass
        
        # Programı yürüt
        result = super().execute(input_data, max_tokens)
        
        # Yürütmeden sonra alan özelliklerini ölç
        if self.neural_field:
            try:
                # Alan metriklerini almayı dene
                field_metrics = self._measure_field_metrics()
                
                # Metrikleri günlüğe kaydet
                logger.info(f"Yürütmeden sonra alan metrikleri: {field_metrics}")
                
                # Metrikleri yürütme izine kaydet
                if self.execution_trace:
                    self.execution_trace[-1]["field_metrics"] = field_metrics
            except (AttributeError, TypeError) as e:
                logger.warning(f"Alan metrikleri ölçülemedi: {e}")
        
        return result
    
    def _measure_field_metrics(self) -> Dict[str, float]:
        """Nöral alan metriklerini ölçer."""
        metrics = {}
        
        # Farklı alan ölçüm yaklaşımlarını dene
        try:
            # Alanın yerleşik ölçümünü kullanmayı dene
            if hasattr(self.neural_field, "measure_field_stability"):
                metrics["stability"] = self.neural_field.measure_field_stability()
            
            # Çekicileri say
            if hasattr(self.neural_field, "attractors"):
                metrics["attractor_count"] = len(self.neural_field.attractors)
            
            # Desenleri say
            if hasattr(self.neural_field, "state"):
                metrics["pattern_count"] = len(self.neural_field.state)
            
            # Rezonans ölçerini içe aktarmayı dene
            try:
                from field_resonance_measure import FieldResonanceMeasurer
                measurer = FieldResonanceMeasurer()
                
                # Kapsamlı metrikleri al
                field_metrics = measurer.get_field_metrics(self.neural_field)
                metrics.update(field_metrics)
            except (ImportError, AttributeError):
                pass
                
        except Exception as e:
            logger.warning(f"Alan metrikleri ölçülürken hata oluştu: {e}")
        
        return metrics

# ------------------------------------------------------------------------------
# Protokol Kabuğu Entegrasyonu
# ------------------------------------------------------------------------------

class ProtocolShellProgram(PromptProgram):
    """Protokol kabuğu entegrasyonuna sahip istem programı."""
    
    def __init__(self, 
                 description: str,
                 protocol: Dict[str, Any],
                 model: Optional[Any] = None,
                 variables: Optional[Dict[str, Any]] = None,
                 neural_field: Optional[Any] = None):
        """
        Bir protokol kabuğu istem programını başlatır.
        
        Args:
            description: Programın amacının açıklaması
            protocol: Protokol kabuğu tanımı
            model: Dil modeli arayüzü
            variables: Başlangıç değişkenleri
            neural_field: Bağlam kalıcılığı için nöral alan
        """
        super().__init__(description, model, variables, neural_field)
        
        # Protokolü ayarla
        self.protocol = protocol
        
        # Protokolden adımları oluştur
        self._generate_steps_from_protocol()
    
    def _generate_steps_from_protocol(self) -> None:
        """Protokol tanımından program adımları oluşturur."""
        # Süreç adımlarını çıkar
        process_steps = self.protocol.get("process", [])
        
        if not process_steps:
            return
            
        # Her süreç öğesi için adım oluştur
        for step in process_steps:
            if isinstance(step, dict):
                # Adım adını al
                step_name = next(iter(step))
                
                # Adım içeriği oluştur
                if isinstance(step[step_name], dict):
                    # Sözlüğü adım olarak biçimlendir
                    content = f"{step_name}: " + ", ".join(
                        f"{k}=\"{v}\"" if isinstance(v, str) else f"{k}={v}"
                        for k, v in step[step_name].items()
                    )
                elif isinstance(step[step_name], list):
                    # Listeyi adım olarak biçimlendir
                    content = f"{step_name}: " + ", ".join(
                        f"\"{item}\"" if isinstance(item, str) else f"{item}"
                        for item in step[step_name]
                    )
                else:
                    # Basit adım
                    content = f"{step_name}: {step[step_name]}"
                
                # Adım ekle
                self.add_step(content)
            elif isinstance(step, str):
                # Basit adım
                self.add_step(step)
    
    def format(self) -> str:
        """Programı protokol kabuğu ile biçimlendirir."""
        # Protokolü biçimlendir
        protocol_str = self._format_protocol()
        
        # Program adımlarını biçimlendir
        steps_str = super().format()
        
        return f"{protocol_str}\n\n{steps_str}"
    
    def _format_protocol(self) -> str:
        """Protokol kabuğunu bir dize olarak biçimlendirir."""
        parts = []
        
        # Protokol adı
        protocol_name = self.protocol.get("name", "protocol")
        parts.append(f"/{protocol_name}{{")
        
        # Niyet
        intent = self.protocol.get("intent", self.description)
        parts.append(f'    intent="{intent}",')
        
        # Girdi parametreleri
        input_params = self.protocol.get("input", {})
        if input_params:
            parts.append("    input={")
            for key, value in input_params.items():
                if isinstance(value, str):
                    parts.append(f'        {key}="{value}",')
                else:
                    parts.append(f"        {key}={value},")
            parts.append("    },")
        
        # Süreç adımları
        process_steps = self.protocol.get("process", [])
        if process_steps:
            parts.append("    process=[")
            for step in process_steps:
                if isinstance(step, dict):
                    step_name = next(iter(step))
                    parts.append(f"        /{step_name}{{")
                    
                    if isinstance(step[step_name], dict):
                        for k, v in step[step_name].items():
                            if isinstance(v, str):
                                parts.append(f'            {k}="{v}",')
                            else:
                                parts.append(f"            {k}={v},")
                    elif isinstance(step[step_name], list):
                        parts.append(f"            {', '.join(step[step_name])}")
                    else:
                        if isinstance(step[step_name], str):
                            parts.append(f'            "{step[step_name]}"')
                        else:
                            parts.append(f"            {step[step_name]}")
                    
                    parts.append("        },")
                elif isinstance(step, str):
                    parts.append(f"        {step},")
            parts.append("    ],")
        
        # Çıktı şeması
        output_schema = self.protocol.get("output", {})
        if output_schema:
            parts.append("    output={")
            for key, value in output_schema.items():
                if isinstance(value, str):
                    parts.append(f'        {key}="{value}",')
                else:
                    parts.append(f"        {key}={value},")
            parts.append("    },")
        
        # Meta
        meta = self.protocol.get("meta", {})
        if meta:
            parts.append("    meta={")
            for key, value in meta.items():
                if isinstance(value, str):
                    parts.append(f'        {key}="{value}",')
                else:
                    parts.append(f"        {key}={value},")
            parts.append("    }")
        
        # Protokolü kapat
        parts.append("}")
        
        return "\n".join(parts)
    
    def execute(self, input_data: str, max_tokens: int = 1000) -> str:
        """
        Protokol programını verilen girdiyle yürütür.
        
        Args:
            input_data: Program için girdi verileri
            max_tokens: Üretim için maksimum jeton sayısı
            
        Returns:
            Yürütme sonucu
        """
        # Protokoldeki girdi parametresini güncelle
        if "input" in self.protocol:
            input_key = next((k for k, v in self.protocol["input"].items() 
                            if v == "<current_input>" or v == "<input>"), None)
            if input_key:
                self.protocol["input"][input_key] = input_data
        
        # Programı yürüt
        return super().execute(input_data, max_tokens)
    
    def extract_output(self, response: str) -> Dict[str, Any]:
        """
        Protokol şemasına göre yanıttan yapılandırılmış çıktı çıkarır.
        
        Args:
            response: Yürütme yanıtı
            
        Returns:
            Çıkarılan çıktı sözlüğü
        """
        # Çıktı şemasını al
        output_schema = self.protocol.get("output", {})
        if not output_schema:
            return {"raw_output": response}
        
        # JSON çıktısını çıkarmayı dene
        json_pattern = r'```(?:json)?\s*({[\s\S]*?})\s*```'
        json_matches = re.findall(json_pattern, response)
        
        if json_matches:
            try:
                extracted = json.loads(json_matches[0])
                
                # Şemayla eşleşecek şekilde filtrele
                output = {}
                for key in output_schema:
                    if key in extracted:
                        output[key] = extracted[key]
                
                # Eksik anahtarları ekle
                for key in output_schema:
                    if key not in output:
                        output[key] = f"<missing_{key}>"
                
                return output
            except json.JSONDecodeError:
                pass
        
        # Çıktı bölümünü çıkarmayı dene
        output_section_pattern = r'(?:Çıktı|Sonuç):\s*\n([\s\S]*?)(?:\n\n|\Z)'
        section_matches = re.findall(output_section_pattern, response)
        
        if section_matches:
            section = section_matches[0]
            
            # Anahtar-değer çiftlerini çıkar
            output = {}
            for line in section.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    if key in output_schema:
                        output[key] = value.strip()
            
            # Eksik anahtarları ekle
            for key in output_schema:
                if key not in output:
                    output[key] = f"<missing_{key}>"
            
            return output
        
        # Geri dönüş: yalnızca ham çıktıyı döndür
        return {"raw_output": response}

# ------------------------------------------------------------------------------
# Kullanım Örnekleri
# ------------------------------------------------------------------------------

def basic_program_example():
    """Temel bir istem programı örneği."""
    # Gösterim için sahte model
    class MockModel:
        def generate(self, prompt, max_tokens=1000):
            return f"""
Adım 1: Değişkenleri ve ilişkileri belirlemek için problemi ayrıştır
Akıl Yürütme: Hangi değişkenlerin dahil olduğunu ve ilişkilerini anlamam gerekiyor.
Sonuç: Problem, saatte 60 mil hızla 2.5 saat giden bir treni içeriyor ve mesafeyi bulmam gerekiyor.

Adım 2: Uygun denklemleri kur
Akıl Yürütme: Mesafe = hız × zaman formülünü kullanacağım.
Sonuç: mesafe = 60 mil/saat × 2.5 saat

Adım 3: Bilinmeyen değişkenleri çöz
Akıl Yürütme: Değerleri yerine koyup hesaplayacağım.
Sonuç: mesafe = 60 × 2.5 = 150 mil

Adım 4: Çözümün orijinal bağlamda mantıklı olup olmadığını doğrula
Akıl Yürütme: Cevabın 2.5 saat giden bir tren için makul olup olmadığını kontrol etmem gerekiyor.
Sonuç: 150 mil, saatte 60 mil hızla 2.5 saat giden bir tren için makul bir mesafedir.

Son Cevap: Tren 150 mil yol alır.
"""
    
    # Program oluştur
    model = MockModel()
    program = PromptProgram("Matematiksel kelime problemlerini adım adım çöz", model)
    
    # Akıl yürütme adımları ekle
    program.add_step("Değişkenleri ve ilişkileri belirlemek için problemi ayrıştır")
    program.add_step("Uygun denklemleri kur")
    program.add_step("Bilinmeyen değişkenleri çöz")
    program.add_step("Çözümün orijinal bağlamda mantıklı olup olmadığını doğrula")
    
    # Biçimlendirilmiş programı yazdır
    print("Program:")
    print(program.format())
    print()
    
    # Programı yürüt
    result = program.execute("Bir tren saatte 60 mil hızla 2.5 saat giderse ne kadar yol alır?")
    print("Yürütme Sonucu:")
    print(result)
    
    # İz ile yürüt
    trace_result = program.execute_with_trace("Bir tren saatte 60 mil hızla 2.5 saat giderse ne kadar yol alır?")
    print("\nYürütme İzi:")
    for step in trace_result["steps_trace"]:
        print(f"Adım {step['step']}:")
        print(f"  Akıl Yürütme: {step['reasoning']}")
        print(f"  Sonuç: {step['result']}")

def neural_field_program_example():
    """Bir nöral alan istem programı örneği."""
    # Gösterim için sahte model
    class MockModel:
        def generate(self, prompt, max_tokens=1000):
            return f"""
Adım 1: İlgilenilen araştırma alanını anla
Akıl Yürütme: Kullanıcının ilgilendiği ana araştırma alanını belirlemem gerekiyor.
Sonuç: Kullanıcı iklim değişikliği araştırmasıyla ilgileniyor.

Adım 2: Bu araştırma alanındaki anahtar alt konuları belirle
Akıl Yürütme: İklim değişikliği araştırması birden çok alanı kapsar, ana alt konuları belirleyeceğim.
Sonuç: Anahtar alt konular şunlardır: atmosfer bilimi, oşinografi, ekoloji, yenilenebilir enerji, politika analizi ve iklim modellemesi.

Adım 3: En aktif araştırma sorularını belirle
Akıl Yürütme: Bu alt konular içinde, şu anda aktif olan araştırma sorularını belirlemem gerekiyor.
Sonuç: Aktif araştırma soruları şunlardır: 
- İklim değişikliği deniz ekosistemlerindeki biyoçeşitliliği nasıl etkileyecek?
- Etkili karbon yakalama teknolojileri nelerdir?
- İklim modelleri aşırı hava olaylarını daha iyi nasıl tahmin edebilir?
- Hangi politika çerçeveleri karbon azaltımını en iyi şekilde teşvik eder?

Adım 4: Belirli araştırma odak alanları öner
Akıl Yürütme: Aktif sorulara dayanarak, etki potansiyeli olan belirli odak alanları önereceğim.
Sonuç: Önerilen araştırma odak alanları:
1. Okyanus asitlenmesine karşı deniz ekosistemi direnci
2. İklim tahmininde makine öğrenmesi uygulamaları
3. Karbon fiyatlandırma mekanizmaları için ekonomik modeller
4. Karbon tutulması için doğa tabanlı çözümler

Son Cevap: İklim değişikliği araştırmasındaki mevcut eğilimlere dayanarak, şu umut verici alanlara odaklanmanızı öneririm:
1. Okyanus asitlenmesine karşı deniz ekosistemi direnci - Bu, ekoloji ve oşinografiyi acil pratik uygulamalarla birleştirir
2. İklim tahmininde makine öğrenmesi uygulamaları - Bu, iklim modelleme doğruluğunu iyileştirmek için yapay zeka ilerlemelerinden yararlanır
3. Karbon fiyatlandırma mekanizmaları için ekonomik modeller - Bu, politika uygulama boşluğunu giderir
4. Karbon tutulması için doğa tabanlı çözümler - Bu, karbon yakalama için ölçeklenebilir yaklaşımlar sunar

Bu alanların her birinin aktif finansman fırsatları, büyüyen araştırma toplulukları ve önemli etki potansiyeli vardır.
"""
    
    # Nöral alanlı program oluştur
    model = MockModel()
    field_params = {
        "decay_rate": 0.1,
        "boundary_permeability": 0.9
    }
    program = NeuralFieldProgram(
        "Bir alandaki umut verici araştırma yönlerini belirle",
        model=model,
        field_params=field_params
    )
    
    # Alana çekiciler ekle
    program.add_attractor("Araştırma, önemli etki potansiyeli olan alanlara odaklanmalıdır")
    program.add_attractor("Disiplinlerarası yaklaşımlar genellikle yeni görüşler ortaya çıkarır")
    program.add_attractor("Hem teorik ilerlemeleri hem de pratik uygulamaları göz önünde bulundurun")
    
    # Akıl yürütme adımları ekle
    program.add_step("İlgilenilen araştırma alanını anla")
    program.add_step("Bu araştırma alanındaki anahtar alt konuları belirle")
    program.add_step("En aktif araştırma sorularını belirle")
    program.add_resonance_step("Belirli araştırma odak alanları öner", [
        "Büyüyen finansman fırsatları olan alanlara öncelik ver",
        "Disiplinlerarası bağlantıları göz önünde bulundur",
        "Teorik ve uygulamalı araştırmayı dengele"
    ])
    
    # Biçimlendirilmiş programı yazdır
    print("Nöral Alan Programı:")
    print(program.format())
    print()
    
    # Programı yürüt
    result = program.execute("İklim değişikliğindeki umut verici araştırma yönleri nelerdir?")
    print("Yürütme Sonucu:")
    print(result)

def protocol_shell_program_example():
    """Bir protokol kabuğu istem programı örneği."""
    # Gösterim için sahte model
    class MockModel:
        def generate(self, prompt, max_tokens=1000):
            return f"""
Bu protokolü adım adım yürüteceğim.

Adım 1: Belge yapısını analiz et
Akıl Yürütme: Belgenin ana bölümlerini ve organizasyonunu belirlemem gerekiyor.
Sonuç: Belgenin 5 ana bölümü vardır: Giriş, Yöntemler, Sonuçlar, Tartışma ve Sonuç.

Adım 2: Her bölümdeki anahtar bilgileri belirle
Akıl Yürütme: Her bölümden en önemli bilgileri çıkarmam gerekiyor.
Sonuç: 
- Giriş: Çalışmanın amacı, diyetin kolesterol seviyeleri üzerindeki etkisini değerlendirmektir
- Yöntemler: 6 ay boyunca 200 katılımcıyla randomize kontrollü çalışma
- Sonuçlar: Bitki bazlı diyet grubu, LDL kolesterolde %15'lik bir azalma gösterdi
- Tartışma: Sonuçlar, benzer faydaları gösteren önceki çalışmalarla uyumludur
- Sonuç: Bitki bazlı diyetler kolesterol seviyelerini önemli ölçüde azaltabilir

Adım 3: Kısa bir özet oluştur
Akıl Yürütme: Temel bilgileri yakalayan bir özet oluşturmam gerekiyor.
Sonuç: 200 katılımcıyla yapılan bu 6 aylık randomize kontrollü çalışma, bitki bazlı bir diyetin LDL kolesterol seviyelerinde %15'lik bir azalmaya yol açtığını ve kardiyovasküler sağlık için diyet bazlı müdahaleler üzerine yapılan önceki araştırmaları desteklediğini bulmuştur.

Çıktı:
özet="200 katılımcıyla yapılan bu 6 aylık randomize kontrollü çalışma, bitki bazlı bir diyetin LDL kolesterol seviyelerinde %15'lik bir azalmaya yol açtığını ve kardiyovasküler sağlık için diyet bazlı müdahaleler üzerine yapılan önceki araştırmaları desteklediğini bulmuştur."
anahtar_bulgu="Bitki bazlı diyetle LDL kolesterolde %15 azalma"
çalışma_tasarımı="Randomize kontrollü çalışma, 200 katılımcı, 6 ay"
öneri="Bitki bazlı diyetler kolesterol seviyelerini önemli ölçüde azaltabilir"
"""
    
    # Protokol kabuğu oluştur
    protocol = {
        "intent": "Bir araştırma makalesini kısaca özetle",
        "input": {
            "document": "<current_input>",
            "focus_area": "anahtar bulgular ve metodoloji"
        },
        "process": [
            {
                "analyze.document": {
                    "target": "structure"
                }
            },
            {
                "identify": {
                    "information": "bölüm başına anahtar noktalar"
                }
            },
            {
                "generate.summary": {
                    "style": "kısa",
                    "length": "1-2 cümle"
                }
            }
        ],
        "output": {
            "summary": "<generated_summary>",
            "key_finding": "<main_result>",
            "study_design": "<methodology_summary>",
            "recommendation": "<primary_conclusion>"
        },
        "meta": {
            "name": "research.summarize",
            "version": "1.0.0",
            "timestamp": time.time()
        }
    }
    
    # Program oluştur
    model = MockModel()
    program = ProtocolShellProgram(
        "Araştırma Makalesi Özetleyici",
        protocol=protocol,
        model=model
    )
    
    # Biçimlendirilmiş programı yazdır
    print("Protokol Kabuğu Programı:")
    print(program.format())
    print()
    
    # Programı yürüt
    result = program.execute("Bitki bazlı diyetlerin kolesterol seviyeleri üzerindeki etkileri üzerine kapsamlı bir çalışma...")
    print("Yürütme Sonucu:")
    print(result)
    
    # Yapılandırılmış çıktıyı çıkar
    output = program.extract_output(result)
    print("\nÇıkarılan Çıktı:")
    for key, value in output.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    # Örnek kullanım
    print("Temel Program Örneği:")
    basic_program_example()
    
    print("\n\nNöral Alan Programı Örneği:")
    neural_field_program_example()
    
    print("\n\nProtokol Kabuğu Programı Örneği:")
    protocol_shell_program_example()
