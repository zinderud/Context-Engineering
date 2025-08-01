
Alan Rezonans Ölçüm Aracı
--------------------------------

Bu modül, bağlam mühendisliği uygulamalarında nöral alanların rezonansını, tutarlılığını ve diğer özelliklerini ölçmek için araçlar sağlar.
Alan durumlarının nicel olarak değerlendirilmesini sağlayarak optimizasyon ve ayarlamaya rehberlik eder.

Kullanım:
    # Bir rezonans ölçer başlat
    measurer = FieldResonanceMeasurer()
    
    # Desenler arasındaki rezonansı ölç
    score = measurer.measure_resonance(pattern1, pattern2)
    
    # Alan tutarlılığını ölç
    coherence = measurer.measure_coherence(field)
    
    # Kapsamlı alan metriklerini al
    metrics = measurer.get_field_metrics(field)


import math
import time
import logging
from typing import Dict, List, Any, Optional, Callable, Union, Tuple, Set
from collections import defaultdict
import yaml
import json

# Günlüğe kaydetmeyi yapılandır
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("field_resonance")

# ------------------------------------------------------------------------------
# Rezonans Ölçümü
# ------------------------------------------------------------------------------

class ResonanceMeasurer:
    """Bir nöral alandaki desenler arasındaki rezonansı ölçer."""
    
    def __init__(self, method: str = "cosine", threshold: float = 0.2, amplification: float = 1.2):
        """
        Rezonans ölçeri başlatır.
        
        Args:
            method: Rezonans hesaplama yöntemi ("cosine", "overlap", "embedding")
            threshold: Rezonans etkileri için minimum eşik
            amplification: Rezonans etkileri için yükseltme faktörü
        """
        self.method = method
        self.threshold = threshold
        self.amplification = amplification
        
        # Gerekirse gömme modelini başlat
        self.embedding_model = None
        if method == "embedding":
            try:
                self._initialize_embedding_model()
            except ImportError:
                logger.warning("Gömme modeli mevcut değil, kosinüs benzerliğine geri dönülüyor")
                self.method = "cosine"
    
    def _initialize_embedding_model(self):
        """Anlamsal benzerlik için gömme modelini başlatır."""
        try:
            import numpy as np
            from sentence_transformers import SentenceTransformer
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.np = np
        except ImportError:
            raise ImportError("Sentence-transformers kurulu değil. 'pip install sentence-transformers' ile kurun")
    
    def measure(self, pattern1: str, pattern2: str) -> float:
        """
        İki desen arasındaki rezonansı ölçer.
        
        Args:
            pattern1: Birinci desen
            pattern2: İkinci desen
            
        Returns:
            Rezonans puanı (0.0 ile 1.0 arası)
        """
        if not pattern1 or not pattern2:
            return 0.0
            
        if self.method == "cosine":
            return self._cosine_similarity(pattern1, pattern2)
        elif self.method == "overlap":
            return self._word_overlap(pattern1, pattern2)
        elif self.method == "embedding":
            return self._embedding_similarity(pattern1, pattern2)
        else:
            logger.warning(f"Bilinmeyen rezonans yöntemi: {self.method}, kosinüse geri dönülüyor")
            return self._cosine_similarity(pattern1, pattern2)
    
    def _cosine_similarity(self, pattern1: str, pattern2: str) -> float:
        """Kelime frekansına dayalı kosinüs benzerliğini hesaplar."""
        # Kelime frekans sözlüklerini al
        words1 = self._get_word_freq(pattern1)
        words2 = self._get_word_freq(pattern2)
        
        # Ortak kelimeleri bul
        common_words = set(words1.keys()) & set(words2.keys())
        
        # Nokta çarpımını hesapla
        dot_product = sum(words1[word] * words2[word] for word in common_words)
        
        # Büyüklükleri hesapla
        mag1 = math.sqrt(sum(value ** 2 for value in words1.values()))
        mag2 = math.sqrt(sum(value ** 2 for value in words2.values()))
        
        # Sıfıra bölmekten kaçın
        if mag1 == 0 or mag2 == 0:
            return 0.0
            
        # Kosinüs benzerliğini hesapla
        similarity = dot_product / (mag1 * mag2)
        
        # Yükseltme ve eşik uygula
        if similarity < self.threshold:
            return 0.0
            
        return min(1.0, similarity * self.amplification)
    
    def _word_overlap(self, pattern1: str, pattern2: str) -> float:
        """Kelime örtüşmesine dayalı benzerliği hesaplar."""
        # Kelime kümelerini al
        words1 = set(pattern1.lower().split())
        words2 = set(pattern2.lower().split())
        
        # Örtüşmeyi hesapla
        if not words1 or not words2:
            return 0.0
            
        overlap = len(words1 & words2)
        union = len(words1 | words2)
        
        # Jaccard benzerliğini hesapla
        similarity = overlap / union
        
        # Yükseltme ve eşik uygula
        if similarity < self.threshold:
            return 0.0
            
        return min(1.0, similarity * self.amplification)
    
    def _embedding_similarity(self, pattern1: str, pattern2: str) -> float:
        """Gömme vektörlerine dayalı benzerliği hesaplar."""
        if self.embedding_model is None:
            logger.warning("Gömme modeli başlatılmadı, kosinüs benzerliğine geri dönülüyor")
            return self._cosine_similarity(pattern1, pattern2)
            
        # Gömmeleri al
        embedding1 = self.embedding_model.encode([pattern1])[0]
        embedding2 = self.embedding_model.encode([pattern2])[0]
        
        # Kosinüs benzerliğini hesapla
        similarity = self.np.dot(embedding1, embedding2) / (
            self.np.linalg.norm(embedding1) * self.np.linalg.norm(embedding2)
        )
        
        # Yükseltme ve eşik uygula
        if similarity < self.threshold:
            return 0.0
            
        return min(1.0, float(similarity * self.amplification))
    
    def _get_word_freq(self, text: str) -> Dict[str, int]:
        """Metinden kelime frekans sözlüğü alır."""
        words = text.lower().split()
        freq = defaultdict(int)
        for word in words:
            freq[word] += 1
        return freq

# ------------------------------------------------------------------------------
# Tutarlılık Ölçümü
# ------------------------------------------------------------------------------

class CoherenceMeasurer:
    """Bir nöral alanın tutarlılığını ölçer."""
    
    def __init__(self, method: str = "attractor_alignment", sampling: str = "strength_weighted", sample_size: int = 100):
        """
        Tutarlılık ölçeri başlatır.
        
        Args:
            method: Tutarlılık hesaplama yöntemi ("pairwise", "attractor_alignment", "entropy")
            sampling: Büyük alanlar için örnekleme stratejisi ("full", "random", "strength_weighted")
            sample_size: Büyük alanlar için örneklem boyutu
        """
        self.method = method
        self.sampling = sampling
        self.sample_size = sample_size
        self.resonance_measurer = ResonanceMeasurer()
    
    def measure(self, field: Any) -> float:
        """
        Bir alanın tutarlılığını ölçer.
        
        Args:
            field: Ölçülecek nöral alan
            
        Returns:
            Tutarlılık puanı (0.0 ile 1.0 arası)
        """
        if self.method == "pairwise":
            return self._pairwise_coherence(field)
        elif self.method == "attractor_alignment":
            return self._attractor_alignment(field)
        elif self.method == "entropy":
            return self._entropy_coherence(field)
        else:
            logger.warning(f"Bilinmeyen tutarlılık yöntemi: {self.method}, attractor_alignment'a geri dönülüyor")
            return self._attractor_alignment(field)
    
    def _pairwise_coherence(self, field: Any) -> float:
        """İkili desen rezonansına dayalı tutarlılığı hesaplar."""
        # Değerlendirilecek desenleri al
        patterns = self._sample_patterns(field)
        
        if len(patterns) < 2:
            return 1.0  # Tek bir desen için mükemmel tutarlılık
            
        # Tüm ikili rezonansları hesapla
        total_resonance = 0.0
        pair_count = 0
        
        for i, (pattern1, strength1) in enumerate(patterns):
            for j, (pattern2, strength2) in enumerate(patterns):
                if i < j:  # Her çifti yalnızca bir kez karşılaştır
                    resonance = self.resonance_measurer.measure(pattern1, pattern2)
                    weighted_resonance = resonance * strength1 * strength2
                    total_resonance += weighted_resonance
                    pair_count += 1
        
        if pair_count == 0:
            return 0.0
            
        # Ortalama rezonansı hesapla
        avg_resonance = total_resonance / pair_count
        
        return avg_resonance
    
    def _attractor_alignment(self, field: Any) -> float:
        """Çekicilerle hizalamaya dayalı tutarlılığı hesaplar."""
        # Çekicileri ve desenleri al
        attractors = self._get_attractors(field)
        patterns = self._sample_patterns(field)
        
        if not attractors:
            return self._pairwise_coherence(field)  # Çekici yoksa ikiliye geri dön
            
        # Çekicilerle hizalamayı hesapla
        total_alignment = 0.0
        total_weight = 0.0
        
        for pattern, pattern_strength in patterns:
            # Her çekiciyle hizalamayı hesapla
            best_alignment = 0.0
            for attractor, attractor_strength in attractors:
                alignment = self.resonance_measurer.measure(pattern, attractor)
                if alignment > best_alignment:
                    best_alignment = alignment
            
            # Desen gücüne göre ağırlıklandır
            total_alignment += best_alignment * pattern_strength
            total_weight += pattern_strength
        
        if total_weight == 0:
            return 0.0
            
        # Ortalama hizalamayı hesapla
        avg_alignment = total_alignment / total_weight
        
        return avg_alignment
    
    def _entropy_coherence(self, field: Any) -> float:
        """Entropi azalmasına dayalı tutarlılığı hesaplar."""
        # Bu, entropi tabanlı tutarlılığın basitleştirilmiş bir yaklaşımıdır
        # Tam bir uygulama, uygun bilgi teorisi metriklerini kullanırdı
        
        # Desenleri ve çekicileri al
        patterns = self._sample_patterns(field)
        attractors = self._get_attractors(field)
        
        if not patterns:
            return 0.0
            
        # Desen organizasyonunu hesapla
        organization = 0.0
        total_strength = sum(strength for _, strength in patterns)
        
        for pattern, pattern_strength in patterns:
            # En rezonanslı çekiciyi bul
            best_resonance = 0.0
            for attractor, _ in attractors:
                resonance = self.resonance_measurer.measure(pattern, attractor)
                if resonance > best_resonance:
                    best_resonance = resonance
            
            # Daha organize desenler daha düşük entropiye katkıda bulunur
            pattern_organization = best_resonance * (pattern_strength / total_strength)
            organization += pattern_organization
        
        # Tutarlılık puanına dönüştür (daha yüksek organizasyon = daha yüksek tutarlılık)
        coherence = organization
        
        return coherence
    
    def _sample_patterns(self, field: Any) -> List[Tuple[str, float]]:
        """Örnekleme stratejisine göre alandan desenleri örnekler."""
        # Alandan desenleri çıkar
        try:
            patterns = [(pattern, strength) for pattern, strength in field.state.items()]
        except AttributeError:
            # Alan yapısının farklı olduğu durumu ele al
            try:
                patterns = field.get_patterns()
            except (AttributeError, TypeError):
                logger.warning("Alandan desenler çıkarılamadı, boş liste kullanılıyor")
                return []
        
        if not patterns:
            return []
            
        # Örnekleme stratejisini uygula
        if self.sampling == "full" or len(patterns) <= self.sample_size:
            return patterns
            
        if self.sampling == "random":
            import random
            return random.sample(patterns, min(self.sample_size, len(patterns)))
            
        if self.sampling == "strength_weighted":
            # Güce göre sırala ve en üst desenleri al
            sorted_patterns = sorted(patterns, key=lambda x: x[1], reverse=True)
            return sorted_patterns[:self.sample_size]
            
        # Varsayılan olarak tam örnekleme
        return patterns
    
    def _get_attractors(self, field: Any) -> List[Tuple[str, float]]:
        """Alandan çekicileri çıkarır."""
        try:
            attractors = [(attractor['pattern'], attractor['strength']) 
                         for attractor in field.attractors.values()]
        except AttributeError:
            # Alan yapısının farklı olduğu durumu ele al
            try:
                attractors = field.get_attractors()
            except (AttributeError, TypeError):
                logger.warning("Alandan çekiciler çıkarılamadı, boş liste kullanılıyor")
                return []
        
        return attractors

# ------------------------------------------------------------------------------
# Kararlılık Ölçümü
# ------------------------------------------------------------------------------

class StabilityMeasurer:
    """Bir nöral alanın kararlılığını ölçer."""
    
    def __init__(self, attractor_weight: float = 0.6, organization_weight: float = 0.4):
        """
        Kararlılık ölçeri başlatır.
        
        Args:
            attractor_weight: Kararlılık hesaplamasında çekici gücü için ağırlık
            organization_weight: Kararlılık hesaplamasında desen organizasyonu için ağırlık
        """
        self.attractor_weight = attractor_weight
        self.organization_weight = organization_weight
        self.coherence_measurer = CoherenceMeasurer()
    
    def measure(self, field: Any) -> float:
        """
        Bir alanın kararlılığını ölçer.
        
        Args:
            field: Ölçülecek nöral alan
            
        Returns:
            Kararlılık puanı (0.0 ile 1.0 arası)
        """
        # Çekicileri al
        attractors = self._get_attractors(field)
        
        if not attractors:
            return 0.0  # Çekici yok = kararlılık yok
            
        # Ortalama çekici gücünü hesapla
        avg_attractor_strength = sum(strength for _, strength in attractors) / len(attractors)
        
        # Desen organizasyonunu hesapla (bir vekil olarak tutarlılığı kullanarak)
        organization = self.coherence_measurer.measure(field)
        
        # Metrikleri birleştir
        stability = (avg_attractor_strength * self.attractor_weight) + (organization * self.organization_weight)
        
        return min(1.0, stability)  # 1.0'da sınırla
    
    def _get_attractors(self, field: Any) -> List[Tuple[str, float]]:
        """Alandan çekicileri çıkarır."""
        try:
            attractors = [(attractor['pattern'], attractor['strength']) 
                         for attractor in field.attractors.values()]
        except AttributeError:
            # Alan yapısının farklı olduğu durumu ele al
            try:
                attractors = field.get_attractors()
            except (AttributeError, TypeError):
                logger.warning("Alandan çekiciler çıkarılamadı, boş liste kullanılıyor")
                return []
        
        return attractors

# ------------------------------------------------------------------------------
# Kapsamlı Alan Metrikleri
# ------------------------------------------------------------------------------

class FieldResonanceMeasurer:
    """
    Nöral alan özelliklerini ölçmek için kapsamlı bir araç.
    Rezonans, tutarlılık, kararlılık ve diğer metrikleri birleştirir.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Alan rezonans ölçerini başlatır.
        
        Args:
            config_path: Yapılandırma dosyasının yolu (YAML)
        """
        self.config = self._load_config(config_path)
        
        # Bileşen ölçerlerini başlat
        self.resonance_measurer = ResonanceMeasurer(
            method=self.config.get('resonance', {}).get('method', 'cosine'),
            threshold=self.config.get('resonance', {}).get('threshold', 0.2),
            amplification=self.config.get('resonance', {}).get('amplification', 1.2)
        )
        
        self.coherence_measurer = CoherenceMeasurer(
            method=self.config.get('coherence', {}).get('method', 'attractor_alignment'),
            sampling=self.config.get('coherence', {}).get('sampling', 'strength_weighted'),
            sample_size=self.config.get('coherence', {}).get('sample_size', 100)
        )
        
        self.stability_measurer = StabilityMeasurer(
            attractor_weight=self.config.get('stability', {}).get('attractor_weight', 0.6),
            organization_weight=self.config.get('stability', {}).get('organization_weight', 0.4)
        )
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Yapılandırmayı dosyadan yükler veya varsayılanları kullanır."""
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                logger.warning(f"{config_path} konumundan yapılandırma yüklenemedi: {e}")
                logger.info("Varsayılan yapılandırma kullanılıyor")
        
        # Varsayılan yapılandırma
        return {
            'resonance': {
                'method': 'cosine',
                'threshold': 0.2,
                'amplification': 1.2
            },
            'coherence': {
                'method': 'attractor_alignment',
                'sampling': 'strength_weighted',
                'sample_size': 100
            },
            'stability': {
                'attractor_weight': 0.6,
                'organization_weight': 0.4
            }
        }
    
    def measure_resonance(self, pattern1: str, pattern2: str) -> float:
        """
        İki desen arasındaki rezonansı ölçer.
        
        Args:
            pattern1: Birinci desen
            pattern2: İkinci desen
            
        Returns:
            Rezonans puanı (0.0 ile 1.0 arası)
        """
        return self.resonance_measurer.measure(pattern1, pattern2)
    
    def measure_coherence(self, field: Any) -> float:
        """
        Bir alanın tutarlılığını ölçer.
        
        Args:
            field: Ölçülecek nöral alan
            
        Returns:
            Tutarlılık puanı (0.0 ile 1.0 arası)
        """
        return self.coherence_measurer.measure(field)
    
    def measure_stability(self, field: Any) -> float:
        """
        Bir alanın kararlılığını ölçer.
        
        Args:
            field: Ölçülecek nöral alan
            
        Returns:
            Kararlılık puanı (0.0 ile 1.0 arası)
        """
        return self.stability_measurer.measure(field)
    
    def get_field_metrics(self, field: Any) -> Dict[str, float]:
        """
        Bir alan için kapsamlı metrikleri alır.
        
        Args:
            field: Ölçülecek nöral alan
            
        Returns:
            Metrikler sözlüğü
        """
        # Temel metrikler
        metrics = {
            'coherence': self.measure_coherence(field),
            'stability': self.measure_stability(field)
        }
        
        # Çekici metriklerini ekle
        attractors = self._get_attractors(field)
        if attractors:
            metrics['attractor_count'] = len(attractors)
            metrics['avg_attractor_strength'] = sum(strength for _, strength in attractors) / len(attractors)
            metrics['max_attractor_strength'] = max(strength for _, strength in attractors) if attractors else 0.0
        else:
            metrics['attractor_count'] = 0
            metrics['avg_attractor_strength'] = 0.0
            metrics['max_attractor_strength'] = 0.0
        
        # Desen metriklerini ekle
        patterns = self._get_patterns(field)
        if patterns:
            metrics['pattern_count'] = len(patterns)
            metrics['avg_pattern_strength'] = sum(strength for _, strength in patterns) / len(patterns)
        else:
            metrics['pattern_count'] = 0
            metrics['avg_pattern_strength'] = 0.0
        
        # Entropiyi hesapla (bilgi düzensizliği)
        entropy = self._calculate_entropy(field)
        metrics['entropy'] = entropy
        
        # Bilgi yoğunluğunu hesapla
        if patterns:
            total_chars = sum(len(pattern) for pattern, _ in patterns)
            metrics['information_density'] = total_chars / max(1, len(patterns))
        else:
            metrics['information_density'] = 0.0
        
        return metrics
    
    def _get_attractors(self, field: Any) -> List[Tuple[str, float]]:
        """Alandan çekicileri çıkarır."""
        try:
            attractors = [(attractor['pattern'], attractor['strength']) 
                         for attractor in field.attractors.values()]
        except AttributeError:
            # Alan yapısının farklı olduğu durumu ele al
            try:
                attractors = field.get_attractors()
            except (AttributeError, TypeError):
                logger.warning("Alandan çekiciler çıkarılamadı, boş liste kullanılıyor")
                return []
        
        return attractors
    
    def _get_patterns(self, field: Any) -> List[Tuple[str, float]]:
        """Alandan desenleri çıkarır."""
        try:
            patterns = [(pattern, strength) for pattern, strength in field.state.items()]
        except AttributeError:
            # Alan yapısının farklı olduğu durumu ele al
            try:
                patterns = field.get_patterns()
            except (AttributeError, TypeError):
                logger.warning("Alandan desenler çıkarılamadı, boş liste kullanılıyor")
                return []
        
        return patterns
    
    def _calculate_entropy(self, field: Any) -> float:
        """
        Alanın entropisini (düzensizliğini) hesaplar.
        Daha yüksek entropi = daha fazla düzensizlik = daha az organizasyon.
        
        Args:
            field: Ölçülecek nöral alan
            
        Returns:
            Entropi puanı (0.0 ile 1.0 arası)
        """
        # Desenleri al
        patterns = self._get_patterns(field)
        
        if not patterns:
            return 1.0  # Boş alan için maksimum entropi
            
        # Toplam gücü hesapla
        total_strength = sum(strength for _, strength in patterns)
        
        if total_strength == 0:
            return 1.0
            
        # Olasılıkları hesapla
        probabilities = [strength / total_strength for _, strength in patterns if strength > 0]
        
        # Shannon entropisini hesapla
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        
        # 0-1 aralığına normalleştir
        max_entropy = math.log2(len(patterns))
        if max_entropy == 0:
            normalized_entropy = 0.0
        else:
            normalized_entropy = entropy / max_entropy
        
        return normalized_entropy
    
    def visualize_field(self, field: Any, format: str = "ascii") -> str:
        """
        Alanın bir görselleştirmesini oluşturur.
        
        Args:
            field: Görselleştirilecek nöral alan
            format: Görselleştirme formatı ("ascii", "text", "json")
            
        Returns:
            Görselleştirme dizesi
        """
        if format == "json":
            return self._visualize_json(field)
        elif format == "text":
            return self._visualize_text(field)
        else:
            return self._visualize_ascii(field)
    
    def _visualize_ascii(self, field: Any) -> str:
        """Alanın ASCII görselleştirmesini oluşturur."""
        # Alan bileşenlerini al
        attractors = self._get_attractors(field)
        patterns = self._get_patterns(field)
        metrics = self.get_field_metrics(field)
        
        # Güce göre sırala
        attractors = sorted(attractors, key=lambda x: x[1], reverse=True)
        patterns = sorted(patterns, key=lambda x: x[1], reverse=True)
        
        # Görselleştirmeyi oluştur
        lines = []
        lines.append("=" * 80)
        lines.append("NÖRAL ALAN GÖRSELLEŞTİRMESİ")
        lines.append("=" * 80)
        
        # Metrikleri ekle
        lines.append("ALAN METRİKLERİ:")
        lines.append(f"Tutarlılık:    {'*' * int(metrics['coherence'] * 20):<20} {metrics['coherence']:.2f}")
        lines.append(f"Kararlılık:     {'*' * int(metrics['stability'] * 20):<20} {metrics['stability']:.2f}")
        lines.append(f"Entropi:       {'*' * int(metrics['entropy'] * 20):<20} {metrics['entropy']:.2f}")
        lines.append(f"Çekiciler:    {metrics['attractor_count']}")
        lines.append(f"Desenler:      {metrics['pattern_count']}")
        lines.append("-" * 80)
        
        # Çekicileri ekle
        lines.append("ÇEKİCİLER:")
        for i, (pattern, strength) in enumerate(attractors[:5]):  # En iyi 5'i göster
            short_pattern = pattern[:50] + "..." if len(pattern) > 50 else pattern
            lines.append(f"A{i+1} ({strength:.2f}): {'#' * int(strength * 20):<20} {short_pattern}")
        lines.append("-" * 80)
        
        # Aktif desenleri ekle
        lines.append("AKTİF DESENLER:")
        for i, (pattern, strength) in enumerate(patterns[:7]):  # En iyi 7'yi göster
            short_pattern = pattern[:40] + "..." if len(pattern) > 40 else pattern
            lines.append(f"P{i+1} ({strength:.2f}): {'*' * int(strength * 20):<20} {short_pattern}")
        lines.append("-" * 80)
        
        # Rezonans görselleştirmesini ekle
        if attractors and patterns:
            lines.append("REZONANS HARİTASI:")
            # En iyi çekiciler ve desenler arasındaki rezonansı göster
            for i, (pattern, p_strength) in enumerate(patterns[:3]):  # En iyi 3 desen
                for j, (attractor, a_strength) in enumerate(attractors[:3]):  # En iyi 3 çekici
                    resonance = self.resonance_measurer.measure(pattern, attractor)
                    if resonance > 0.2:  # Yalnızca önemli rezonansı göster
                        lines.append(f"P{i+1} ↔ A{j+1}: {'-' * int(resonance * 20):<20} {resonance:.2f}")
            lines.append("-" * 80)
        
        return "\n".join(lines)
    
    def _visualize_text(self, field: Any) -> str:
        """Alanın metin görselleştirmesini oluşturur."""
        # Alan bileşenlerini al
        attractors = self._get_attractors(field)
        patterns = self._get_patterns(field)
        metrics = self.get_field_metrics(field)
        
        # Görselleştirmeyi oluştur
        lines = []
        lines.append("NÖRAL ALAN DURUMU")
        lines.append("")
        
        # Metrikleri ekle
        lines.append("Alan Metrikleri:")
        lines.append(f"- Tutarlılık: {metrics['coherence']:.2f}")
        lines.append(f"- Kararlılık: {metrics['stability']:.2f}")
        lines.append(f"- Entropi: {metrics['entropy']:.2f}")
        lines.append(f"- Çekici sayısı: {metrics['attractor_count']}")
        lines.append(f"- Desen sayısı: {metrics['pattern_count']}")
        lines.append("")
        
        # Çekicileri ekle
        lines.append("Anahtar Çekiciler:")
        for i, (pattern, strength) in enumerate(sorted(attractors, key=lambda x: x[1], reverse=True)[:3]):
            short_pattern = pattern[:100] + "..." if len(pattern) > 100 else pattern
            lines.append(f"- Çekici {i+1} (Güç: {strength:.2f}): {short_pattern}")
        lines.append("")
        
        # Desenleri ekle
        lines.append("Aktif Desenler:")
        for i, (pattern, strength) in enumerate(sorted(patterns, key=lambda x: x[1], reverse=True)[:5]):
            short_pattern = pattern[:80] + "..." if len(pattern) > 80 else pattern
            lines.append(f"- Desen {i+1} (Güç: {strength:.2f}): {short_pattern}")
        
        return "\n".join(lines)
    
    def _visualize_json(self, field: Any) -> str:
        """Alanın JSON görselleştirmesini oluşturur."""
        # Alan bileşenlerini al
        attractors = self._get_attractors(field)
        patterns = self._get_patterns(field)
        metrics = self.get_field_metrics(field)
        
        # Veri yapısını hazırla
        data = {
            "metrics": metrics,
            "attractors": [
                {
                    "id": f"A{i+1}",
                    "pattern": pattern[:100] + "..." if len(pattern) > 100 else pattern,
                    "strength": strength
                }
                for i, (pattern, strength) in enumerate(sorted(attractors, key=lambda x: x[1], reverse=True)[:5])
            ],
            "patterns": [
                {
                    "id": f"P{i+1}",
                    "pattern": pattern[:80] + "..." if len(pattern) > 80 else pattern,
                    "strength": strength
                }
                for i, (pattern, strength) in enumerate(sorted(patterns, key=lambda x: x[1], reverse=True)[:7])
            ],
            "resonance": []
        }
        
        # Rezonans verilerini ekle
        if attractors and patterns:
            top_attractors = sorted(attractors, key=lambda x: x[1], reverse=True)[:3]
            top_patterns = sorted(patterns, key=lambda x: x[1], reverse=True)[:3]
            
            for i, (pattern, _) in enumerate(top_patterns):
                for j, (attractor, _) in enumerate(top_attractors):
                    resonance = self.resonance_measurer.measure(pattern, attractor)
                    if resonance > 0.2:  # Yalnızca önemli rezonansı dahil et
                        data["resonance"].append({
                            "source": f"P{i+1}",
                            "target": f"A{j+1}",
                            "strength": resonance
                        })
        
        # JSON'a dönüştür
        return json.dumps(data, indent=2)

# ------------------------------------------------------------------------------
# Alan Analiz Araçları
# ------------------------------------------------------------------------------

class FieldAnalyzer:
    """Nöral alanları analiz etmek ve içgörüler sağlamak için araçlar."""
    
    def __init__(self, measurer: Optional[FieldResonanceMeasurer] = None):
        """
        Alan analizörünü başlatır.
        
        Args:
            measurer: FieldResonanceMeasurer örneği veya yeni bir tane oluşturmak için None
        """
        self.measurer = measurer or FieldResonanceMeasurer()
    
    def analyze_field(self, field: Any) -> Dict[str, Any]:
        """
        Bir alanın kapsamlı analizini yapar.
        
        Args:
            field: Analiz edilecek nöral alan
            
        Returns:
            Analiz sonuçları
        """
        # Temel metrikleri al
        metrics = self.measurer.get_field_metrics(field)
        
        # Alan bileşenlerini al
        attractors = self._get_attractors(field)
        patterns = self._get_patterns(field)
        
        # Çekici yapısını analiz et
        attractor_analysis = self._analyze_attractors(attractors)
        
        # Desen organizasyonunu analiz et
        pattern_analysis = self._analyze_patterns(patterns, attractors)
        
        # Alan evrim potansiyelini analiz et
        evolution_analysis = self._analyze_evolution_potential(field, metrics)
        
        # Analizi derle
        analysis = {
            "metrics": metrics,
            "attractor_analysis": attractor_analysis,
            "pattern_analysis": pattern_analysis,
            "evolution_analysis": evolution_analysis,
            "recommendations": self._generate_recommendations(metrics, attractor_analysis, pattern_analysis)
        }
        
        return analysis
    
    def _get_attractors(self, field: Any) -> List[Tuple[str, float]]:
        """Alandan çekicileri çıkarır."""
        try:
            attractors = [(attractor['pattern'], attractor['strength']) 
                         for attractor in field.attractors.values()]
        except AttributeError:
            # Alan yapısının farklı olduğu durumu ele al
            try:
                attractors = field.get_attractors()
            except (AttributeError, TypeError):
                logger.warning("Alandan çekiciler çıkarılamadı, boş liste kullanılıyor")
                return []
        
        return attractors
    
    def _get_patterns(self, field: Any) -> List[Tuple[str, float]]:
        """Alandan desenleri çıkarır."""
        try:
            patterns = [(pattern, strength) for pattern, strength in field.state.items()]
        except AttributeError:
            # Alan yapısının farklı olduğu durumu ele al
            try:
                patterns = field.get_patterns()
            except (AttributeError, TypeError):
                logger.warning("Alandan desenler çıkarılamadı, boş liste kullanılıyor")
                return []
        
        return patterns
    
    def _analyze_attractors(self, attractors: List[Tuple[str, float]]) -> Dict[str, Any]:
        """
        Çekici yapısını analiz eder.
        
        Args:
            attractors: (desen, güç) demetleri listesi
            
        Returns:
            Çekici analizi
        """
        if not attractors:
            return {
                "count": 0,
                "strength_distribution": "none",
                "diversity": 0.0,
                "dominant_theme": None
            }
        
        # Çekicileri say
        count = len(attractors)
        
        # Güç dağılımını analiz et
        strengths = [strength for _, strength in attractors]
        max_strength = max(strengths)
        min_strength = min(strengths)
        avg_strength = sum(strengths) / count
        strength_range = max_strength - min_strength
        
        if strength_range < 0.2:
            strength_distribution = "uniform"
        elif max_strength > 0.8 and avg_strength < 0.5:
            strength_distribution = "dominant"
        else:
            strength_distribution = "balanced"
        
        # Çeşitliliği analiz et
        # Basit bir yaklaşım: ikili benzerliği kontrol et
        total_similarity = 0.0
        pair_count = 0
        
        for i, (pattern1, _) in enumerate(attractors):
            for j, (pattern2, _) in enumerate(attractors):
                if i < j:  # Her çifti yalnızca bir kez karşılaştır
                    similarity = self.measurer.measure_resonance(pattern1, pattern2)
                    total_similarity += similarity
                    pair_count += 1
        
        diversity = 1.0 - (total_similarity / max(1, pair_count))
        
        # Baskın temayı belirle (basitleştirilmiş)
        strongest_attractor = max(attractors, key=lambda x: x[1])
        dominant_theme = strongest_attractor[0][:50] + "..." if len(strongest_attractor[0]) > 50 else strongest_attractor[0]
        
        return {
            "count": count,
            "strength_distribution": strength_distribution,
            "diversity": diversity,
            "dominant_theme": dominant_theme,
            "max_strength": max_strength,
            "min_strength": min_strength,
            "avg_strength": avg_strength
        }
    
    def _analyze_patterns(self, patterns: List[Tuple[str, float]], 
                         attractors: List[Tuple[str, float]]) -> Dict[str, Any]:
        """
        Desen organizasyonunu analiz eder.
        
        Args:
            patterns: (desen, güç) demetleri listesi
            attractors: (desen, güç) demetleri listesi
            
        Returns:
            Desen analizi
        """
        if not patterns:
            return {
                "count": 0,
                "organization": "none",
                "attractor_alignment": 0.0,
                "fragmentation": 0.0
            }
        
        # Desenleri say
        count = len(patterns)
        
        # Desen güç dağılımını analiz et
        strengths = [strength for _, strength in patterns]
        max_strength = max(strengths) if strengths else 0.0
        min_strength = min(strengths) if strengths else 0.0
        avg_strength = sum(strengths) / count if count > 0 else 0.0
        
        # Çekici hizalamasını hesapla
        if attractors:
            total_alignment = 0.0
            for pattern, pattern_strength in patterns:
                best_alignment = 0.0
                for attractor, _ in attractors:
                    alignment = self.measurer.measure_resonance(pattern, attractor)
                    if alignment > best_alignment:
                        best_alignment = alignment
                
                total_alignment += best_alignment * pattern_strength
            
            attractor_alignment = total_alignment / sum(strengths) if sum(strengths) > 0 else 0.0
        else:
            attractor_alignment = 0.0
        
        # Parçalanmayı analiz et
        # Kaç tane bağlantısız desen kümesi olduğunu kontrol et
        if count > 1:
            # Basit yaklaşım: diğerlerine düşük benzerliği olan desenleri say
            isolated_patterns = 0
            for i, (pattern1, _) in enumerate(patterns):
                max_similarity = 0.0
                for j, (pattern2, _) in enumerate(patterns):
                    if i != j:
                        similarity = self.measurer.measure_resonance(pattern1, pattern2)
                        if similarity > max_similarity:
                            max_similarity = similarity
                
                if max_similarity < 0.3:  # İzolasyon için eşik
                    isolated_patterns += 1
            
            fragmentation = isolated_patterns / count
        else:
            fragmentation = 0.0
        
        # Organizasyon türünü belirle
        if attractor_alignment > 0.7:
            organization = "strongly_aligned"
        elif attractor_alignment > 0.4:
            organization = "moderately_aligned"
        elif fragmentation > 0.5:
            organization = "fragmented"
        else:
            organization = "loosely_connected"
        
        return {
            "count": count,
            "organization": organization,
            "attractor_alignment": attractor_alignment,
            "fragmentation": fragmentation,
            "max_strength": max_strength,
            "min_strength": min_strength,
            "avg_strength": avg_strength
        }
    
    def _analyze_evolution_potential(self, field: Any, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Alan evrim potansiyelini analiz eder.
        
        Args:
            field: Analiz edilecek nöral alan
            metrics: Alan metrikleri
            
        Returns:
            Evrim analizi
        """
        # Kararlılık vs. plastisiteyi analiz et
        stability = metrics.get('stability', 0.0)
        entropy = metrics.get('entropy', 1.0)
        
        plasticity = 1.0 - stability
        
        # Evrim potansiyelini belirle
        if stability > 0.8 and entropy < 0.3:
            # Yüksek kararlılık, düşük entropi = katı alan
            evolution_potential = "limited"
            bottleneck = "field_rigidity"
        elif stability < 0.3 and entropy > 0.7:
            # Düşük kararlılık, yüksek entropi = kaotik alan
            evolution_potential = "unstable"
            bottleneck = "field_instability"
        elif stability > 0.6 and entropy > 0.6:
            # Yüksek kararlılık, yüksek entropi = kritik alan
            evolution_potential = "optimal"
            bottleneck = None
        else:
            # Dengeli alan
            evolution_potential = "moderate"
            bottleneck = "needs_tuning"
        
        # Optimal işlemleri belirle
        if evolution_potential == "limited":
            recommended_operations = ["attenuate_attractors", "inject_novelty"]
        elif evolution_potential == "unstable":
            recommended_operations = ["strengthen_attractors", "prune_weak_patterns"]
        elif evolution_potential == "optimal":
            recommended_operations = ["maintain_balance", "selective_amplification"]
        else:
            recommended_operations = ["tune_parameters", "consolidate_patterns"]
        
        return {
            "evolution_potential": evolution_potential,
            "bottleneck": bottleneck,
            "stability": stability,
            "plasticity": plasticity,
            "recommended_operations": recommended_operations
        }
    
    def _generate_recommendations(self, metrics: Dict[str, float],
                                attractor_analysis: Dict[str, Any],
                                pattern_analysis: Dict[str, Any]) -> List[str]:
        """
        Alan iyileştirmesi için öneriler oluşturur.
        
        Args:
            metrics: Alan metrikleri
            attractor_analysis: Çekici analizi
            pattern_analysis: Desen analizi
            
        Returns:
            Öneriler listesi
        """
        recommendations = []
        
        # Çekici yapısını kontrol et
        if attractor_analysis["count"] == 0:
            recommendations.append("Alan yapısı sağlamak için başlangıç çekicileri oluşturun")
        elif attractor_analysis["count"] < 3:
            recommendations.append("Daha zengin bir alan yapısı oluşturmak için daha fazla çekici ekleyin")
        elif attractor_analysis["diversity"] < 0.3:
            recommendations.append("Daha geniş anlamsal alanı kapsamak için çekici çeşitliliğini artırın")
        
        if attractor_analysis.get("strength_distribution") == "dominant" and attractor_analysis.get("count") > 1:
            recommendations.append("Aşırı baskınlığı önlemek için çekici güçlerini dengeleyin")
        
        # Desen organizasyonunu kontrol et
        if pattern_analysis["organization"] == "fragmented":
            recommendations.append("Desenler arasındaki ilişkileri güçlendirerek parçalanmayı azaltın")
        
        if pattern_analysis["attractor_alignment"] < 0.3 and pattern_analysis["count"] > 0:
            recommendations.append("Desenler ve çekiciler arasındaki hizalamayı iyileştirin")
        
        # Alan metriklerini kontrol et
        if metrics.get("coherence", 0.0) < 0.4:
            recommendations.append("Desen birleştirme yoluyla alan tutarlılığını artırın")
        
        if metrics.get("stability", 0.0) < 0.3:
            recommendations.append("Çekicileri güçlendirerek alan kararlılığını iyileştirin")
        elif metrics.get("stability", 0.0) > 0.9:
            recommendations.append("Alan evrimini sağlamak için kontrollü istikrarsızlık getirin")
        
        if metrics.get("entropy", 0.0) > 0.8:
            recommendations.append("Desen organizasyonu yoluyla entropiyi azaltın")
        elif metrics.get("entropy", 0.0) < 0.2:
            recommendations.append("Daha çeşitli alan durumları sağlamak için entropiyi artırın")
        
        # En az bir önerimiz olduğundan emin ol
        if not recommendations:
            if metrics.get("coherence", 0.0) > 0.7 and metrics.get("stability", 0.0) > 0.7:
                recommendations.append("Mevcut alan durumunu periyodik takviye ile koruyun")
            else:
                recommendations.append("Uygulama gereksinimlerine göre alan parametrelerini ayarlayın")
        
        return recommendations

# ------------------------------------------------------------------------------
# Kullanım Örnekleri
# ------------------------------------------------------------------------------

def measure_field_resonance_example():
    """Alan rezonans ölçümü kullanım örneği."""
    # Gösterim için basit bir sahte alan oluştur
    class MockField:
        def __init__(self):
            self.state = {
                "Nöral alanlar bağlamı sürekli bir ortam olarak ele alır.": 0.9,
                "Bilgi, açık depolama yerine rezonans yoluyla devam eder.": 0.8,
                "Mevcut alan yapılarıyla hizalanan desenler daha yavaş bozulur.": 0.7,
                "Alan sınırları, bilginin içeri ve dışarı nasıl aktığını belirler.": 0.6,
                "Yeni girdiler, yalnızca son jetonlarla değil, tüm alanla etkileşime girer.": 0.5
            }
            self.attractors = {
                "attractor1": {
                    "pattern": "Nöral alanlar, bağlamı sürekli bir anlamsal manzara olarak temsil eder.",
                    "strength": 0.9
                },
                "attractor2": {
                    "pattern": "Rezonans, bilgi kalıcılığı için anahtar bir mekanizmadır.",
                    "strength": 0.8
                }
            }
    
    # Bir alan oluştur
    field = MockField()
    
    # Bir ölçer oluştur
    measurer = FieldResonanceMeasurer()
    
    # İki desen arasındaki rezonansı ölç
    pattern1 = "Nöral alanlar kalıcı bağlam sağlar."
    pattern2 = "Bilgi, nöral alanlarda rezonans yoluyla devam eder."
    resonance = measurer.measure_resonance(pattern1, pattern2)
    print(f"Desenler arasındaki rezonans: {resonance:.2f}")
    
    # Alan tutarlılığını ölç
    coherence = measurer.measure_coherence(field)
    print(f"Alan tutarlılığı: {coherence:.2f}")
    
    # Alan kararlılığını ölç
    stability = measurer.measure_stability(field)
    print(f"Alan kararlılığı: {stability:.2f}")
    
    # Kapsamlı metrikleri al
    metrics = measurer.get_field_metrics(field)
    print("Alan metrikleri:")
    for key, value in metrics.items():
        print(f"- {key}: {value:.2f}")
    
    # Alanı görselleştir
    visualization = measurer.visualize_field(field, format="ascii")
    print("\nAlan görselleştirmesi:")
    print(visualization)
    
    # Alanı analiz et
    analyzer = FieldAnalyzer(measurer)
    analysis = analyzer.analyze_field(field)
    
    print("\nAlan analizi:")
    print(f"Evrim potansiyeli: {analysis['evolution_analysis']['evolution_potential']}")
    print("Öneriler:")
    for recommendation in analysis['recommendations']:
        print(f"- {recommendation}")

if __name__ == "__main__":
    # Örnek kullanım
    measure_field_resonance_example()
