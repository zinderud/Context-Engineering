
Bağlam Mühendisliği Puanlama Fonksiyonları
------------------------------------

Bu modül, bağlam mühendisliği uygulamalarında bağlam kalitesini ve model yanıtlarını
değerlendirmek için puanlama fonksiyonları sağlar. Aşağıdakiler için metrikler içerir:

1. Alaka Düzeyi - İçeriğin sorgu veya hedefle ne kadar iyi ilişkili olduğu
2. Tutarlılık - İçeriğin ne kadar mantıksal olarak tutarlı ve iyi yapılandırılmış olduğu
3. Kapsamlılık - Bilginin ne kadar eksiksiz olduğu
4. Özlülük - Bilginin ne kadar verimli bir şekilde sunulduğu
5. Doğruluk - Bilginin olgusal olarak ne kadar doğru olduğu
6. Jeton Verimliliği - Jeton bütçesinin ne kadar etkili kullanıldığı
7. Alan Rezonansı - İçeriğin nöral alan desenleriyle ne kadar iyi hizalandığı

Kullanım:
    # Model yanıtı alaka düzeyini puanla
    relevance_score = score_relevance(response, query)
    
    # Bağlam tutarlılığını puanla
    coherence_score = score_coherence(context)
    
    # Bir yanıt için kapsamlı puanlama al
    scores = score_response(response, query, context, reference=None)


import math
import re
import time
import json
import logging
from typing import Dict, List, Any, Optional, Union, Tuple, Set, Callable
from collections import Counter

# Günlüğe kaydetmeyi yapılandır
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("scoring_functions")

# ------------------------------------------------------------------------------
# Metin İşleme Yardımcı Programları
# ------------------------------------------------------------------------------

def tokenize(text: str) -> List[str]:
    """
    Metin için basit jetonlaştırma işlevi.
    
    Args:
        text: Girdi metni
        
    Returns:
        Jeton listesi
    """
    # Noktalama işaretlerini kaldır ve küçük harfe dönüştür
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    
    # Jetonlara ayır
    return text.split()

def count_tokens(text: str) -> int:
    """
    Metindeki jeton sayısını tahmin eder.
    Bu, planlama amaçlı kaba bir yaklaşımdır.
    
    Args:
        text: Girdi metni
        
    Returns:
        Tahmini jeton sayısı
    """
    # Kaba yaklaşım: ortalama jeton ~4 karakterdir
    # Daha doğrusu, modeliniz için özel jetonlayıcıyı kullanmak olacaktır
    return len(text) // 4

def extract_sentences(text: str) -> List[str]:
    """
    Metinden cümleleri çıkarır.
    
    Args:
        text: Girdi metni
        
    Returns:
        Cümle listesi
    """
    # Cümle sınırlarında böl
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|
|\!)\s', text)
    
    # Boş cümleleri kaldır
    return [s.strip() for s in sentences if s.strip()]

def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """
    İki küme arasındaki Jaccard benzerliğini hesaplar.
    
    Args:
        set1: Birinci küme
        set2: İkinci küme
        
    Returns:
        Jaccard benzerliği (0.0 ile 1.0 arası)
    """
    if not set1 or not set2:
        return 0.0
        
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union

def cosine_similarity(vec1: Dict[str, int], vec2: Dict[str, int]) -> float:
    """
    İki vektör arasındaki kosinüs benzerliğini hesaplar.
    
    Args:
        vec1: Kelime frekans sözlüğü olarak birinci vektör
        vec2: Kelime frekans sözlüğü olarak ikinci vektör
        
    Returns:
        Kosinüs benzerliği (0.0 ile 1.0 arası)
    """
    if not vec1 or not vec2:
        return 0.0
        
    # Ortak kelimeleri bul
    common_words = set(vec1.keys()).intersection(set(vec2.keys()))
    
    # Nokta çarpımını hesapla
    dot_product = sum(vec1[word] * vec2[word] for word in common_words)
    
    # Büyüklükleri hesapla
    mag1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    mag2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
    
    # Sıfıra bölmekten kaçın
    if mag1 == 0 or mag2 == 0:
        return 0.0
        
    return dot_product / (mag1 * mag2)

def get_word_frequency(text: str) -> Dict[str, int]:
    """
    Metinden kelime frekans sözlüğü alır.
    
    Args:
        text: Girdi metni
        
    Returns:
        Kelime frekans sözlüğü
    """
    tokens = tokenize(text)
    return dict(Counter(tokens))

# ------------------------------------------------------------------------------
# Temel Puanlama Fonksiyonları
# ------------------------------------------------------------------------------

def score_relevance(response: str, query: str, method: str = "cosine") -> float:
    """
    Bir yanıtın bir sorguya olan alaka düzeyini puanlar.
    
    Args:
        response: Model yanıtı
        query: Orijinal sorgu
        method: Benzerlik yöntemi ("cosine" veya "jaccard")
        
    Returns:
        Alaka düzeyi puanı (0.0 ile 1.0 arası)
    """
    if not response or not query:
        return 0.0
        
    if method == "jaccard":
        # Jeton kümelerinde Jaccard benzerliği
        response_tokens = set(tokenize(response))
        query_tokens = set(tokenize(query))
        
        return jaccard_similarity(response_tokens, query_tokens)
        
    else:  # Varsayılan olarak kosinüs
        # Kelime frekanslarında kosinüs benzerliği
        response_freq = get_word_frequency(response)
        query_freq = get_word_frequency(query)
        
        return cosine_similarity(response_freq, query_freq)

def score_coherence(text: str) -> float:
    """
    Metnin cümle akışı ve yapısına göre tutarlılığını puanlar.
    
    Args:
        text: Girdi metni
        
    Returns:
        Tutarlılık puanı (0.0 ile 1.0 arası)
    """
    # Cümleleri çıkar
    sentences = extract_sentences(text)
    
    if len(sentences) <= 1:
        return 1.0  # Tek cümle varsayılan olarak tutarlıdır
        
    # Cümleler arası benzerliği ölç
    total_similarity = 0.0
    
    for i in range(len(sentences) - 1):
        sent1 = sentences[i]
        sent2 = sentences[i + 1]
        
        # Kelime kümelerini al
        words1 = set(tokenize(sent1))
        words2 = set(tokenize(sent2))
        
        # Benzerliği hesapla
        similarity = jaccard_similarity(words1, words2)
        total_similarity += similarity
    
    # Ortalama benzerlik
    avg_similarity = total_similarity / (len(sentences) - 1)
    
    # Geçiş kelimelerini/ifadelerini kontrol et
    transition_words = [
        "ancak", "bu nedenle", "böylece", "sonuç olarak", "ayrıca",
        "ek olarak", "dahası", "benzer şekilde", "aksine", "yine de",
        "rağmen", "çünkü", "-den beri", "sonuç olarak"
    ]
    
    transition_count = 0
    for sentence in sentences[1:]:  # İlk cümleyi atla
        if any(word in sentence.lower() for word in transition_words):
            transition_count += 1
    
    transition_ratio = transition_count / (len(sentences) - 1) if len(sentences) > 1 else 0
    
    # Metrikleri birleştir (ağırlıklı ortalama)
    coherence = (avg_similarity * 0.7) + (transition_ratio * 0.3)
    
    return coherence

def score_comprehensiveness(response: str, reference: Optional[str] = None, key_points: Optional[List[str]] = None) -> float:
    """
    Bir yanıtın kapsamlılığını puanlar.
    
    Args:
        response: Model yanıtı
        reference: İsteğe bağlı referans yanıtı
        key_points: Kapsanması gereken isteğe bağlı anahtar noktalar listesi
        
    Returns:
        Kapsamlılık puanı (0.0 ile 1.0 arası)
    """
    if not response:
        return 0.0
        
    # Referans sağlanmışsa
    if reference:
        # Anahtar terimlerin kapsamını karşılaştır
        response_terms = set(tokenize(response))
        reference_terms = set(tokenize(reference))
        
        # Kaç referans teriminin kapsandığı
        coverage = len(response_terms.intersection(reference_terms)) / len(reference_terms) if reference_terms else 0
        
        return coverage
        
    # Anahtar noktalar sağlanmışsa
    elif key_points:
        # Kaç anahtar noktanın belirtildiğini kontrol et
        mentioned = 0
        for point in key_points:
            point_tokens = set(tokenize(point))
            response_tokens = set(tokenize(response))
            
            # Örtüşmeyi hesapla
            overlap = jaccard_similarity(point_tokens, response_tokens)
            
            if overlap > 0.3:  # Bir noktanın belirtilmiş sayılması için eşik
                mentioned += 1
        
        return mentioned / len(key_points) if key_points else 0
        
    else:
        # Referans veya anahtar nokta yok, bir vekil olarak uzunluğu kullan
        # Bu zayıf bir vekildir ama hiç yoktan iyidir
        token_count = count_tokens(response)
        
        # 150 jetonun kapsamlı olduğunu varsay, buna göre ölçekle
        return min(1.0, token_count / 150)

def score_conciseness(response: str, reference: Optional[str] = None, key_points: Optional[List[str]] = None) -> float:
    """
    Bir yanıtın özlülüğünü puanlar.
    
    Args:
        response: Model yanıtı
        reference: İsteğe bağlı referans yanıtı
        key_points: Kapsanması gereken isteğe bağlı anahtar noktalar listesi
        
    Returns:
        Özlülük puanı (0.0 ile 1.0 arası)
    """
    if not response:
        return 0.0
        
    # Yanıt jeton sayısını al
    response_tokens = count_tokens(response)
    
    # Referans sağlanmışsa
    if reference:
        # Referans jeton sayısını al
        reference_tokens = count_tokens(reference)
        
        # Kapsamlılık puanı
        comprehensiveness = score_comprehensiveness(response, reference)
        
        # Mükemmel özlülük, daha az jetonla aynı kapsamlılığa sahip olmak olacaktır
        if response_tokens <= reference_tokens:
            # Yanıt referanstan daha öz
            conciseness = 1.0
        else:
            # Yanıt referanstan daha az öz
            token_ratio = reference_tokens / response_tokens
            # Kapsamlılığa göre ölçekle
            conciseness = token_ratio * comprehensiveness
        
        return conciseness
        
    # Anahtar noktalar sağlanmışsa
    elif key_points:
        # Kaç anahtar noktanın belirtildiğini kontrol et
        coverage = score_comprehensiveness(response, key_points=key_points)
        
        # Anahtar nokta başına 30 jetonun öz olduğunu varsay
        expected_tokens = len(key_points) * 30
        
        if response_tokens <= expected_tokens:
            # Yanıt beklenenden daha öz
            conciseness = 1.0
        else:
            # Yanıt beklenenden daha az öz
            token_ratio = expected_tokens / response_tokens
            # Kapsama göre ölçekle
            conciseness = token_ratio * coverage
        
        return conciseness
        
    else:
        # Referans veya anahtar nokta yok, bir vekil olarak jeton yoğunluğunu kullan
        # Bu zayıf bir vekildir ama hiç yoktan iyidir
        
        # Benzersiz özlü kelimeleri say (yaygın durdurma kelimeleri hariç)
        stop_words = {
            "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
            "in", "on", "at", "to", "for", "with", "by", "about", "as", "of"
        }
        
        tokens = tokenize(response)
        substantive_tokens = [t for t in tokens if t not in stop_words]
        unique_substantive = set(substantive_tokens)
        
        # Bilgi yoğunluğunu hesapla
        if response_tokens > 0:
            density = len(unique_substantive) / response_tokens
            
            # 0-1 aralığına ölçekle (ampirik olarak, 0.5 iyi bir yoğunluktur)
            conciseness = min(1.0, density * 2.0)
        else:
            conciseness = 0.0
        
        return conciseness

def score_accuracy(response: str, reference: Optional[str] = None, facts: Optional[List[str]] = None) -> float:
    """
    Bir yanıtın olgusal doğruluğunu puanlar.
    
    Args:
        response: Model yanıtı
        reference: İsteğe bağlı referans yanıtı
        facts: Dahil edilmesi gereken isteğe bağlı gerçekler listesi
        
    Returns:
        Doğruluk puanı (0.0 ile 1.0 arası)
    """
    if not response:
        return 0.0
        
    # Referans sağlanmışsa
    if reference:
        # Bu basitleştirilmiş bir yaklaşımdır - gerçek bir uygulamada,
        # daha karmaşık bir NLI veya gerçek kontrolü yaklaşımı kullanabilirsiniz
        
        # Referanstan önemli gerçekleri al (cümleler olarak basitleştirilmiş)
        reference_facts = extract_sentences(reference)
        
        if not reference_facts:
            return 0.0
            
        # Her gerçeği yanıta göre kontrol et
        response_tokens = set(tokenize(response))
        
        correct_facts = 0
        for fact in reference_facts:
            fact_tokens = set(tokenize(fact))
            
            # Jeton örtüşmesini hesapla
            overlap = len(fact_tokens.intersection(response_tokens)) / len(fact_tokens) if fact_tokens else 0
            
            if overlap > 0.7:  # Yüksek örtüşme, gerçeğin dahil edildiğini gösterir
                correct_facts += 1
        
        return correct_facts / len(reference_facts)
        
    # Belirli gerçekler sağlanmışsa
    elif facts:
        if not facts:
            return 0.0
            
        # Her gerçeği yanıta göre kontrol et
        response_lower = response.lower()
        
        correct_facts = 0
        for fact in facts:
            # Gerçeğin yanıtta içerilip içerilmediğini basitçe kontrol et
            # Daha karmaşık bir yaklaşım anlamsal eşdeğerliği kontrol ederdi
            if fact.lower() in response_lower:
                correct_facts += 1
        
        return correct_facts / len(facts)
        
    else:
        # Referans veya gerçek sağlanmadı
        # Altın bir standart olmadan doğruluğu değerlendiremeyiz
        logger.warning("Referans veya gerçekler olmadan doğruluk değerlendirilemez")
        return 0.5  # Nötr puan döndür

def score_token_efficiency(response: str, max_tokens: int = 500) -> float:
    """
    Bir yanıtın jeton verimliliğini puanlar.
    
    Args:
        response: Model yanıtı
        max_tokens: Maksimum jeton bütçesi
        
    Returns:
        Verimlilik puanı (0.0 ile 1.0 arası)
    """
    if not response:
        return 0.0
        
    # Yanıttaki jetonları say
    token_count = count_tokens(response)
    
    if token_count > max_tokens:
        # Yanıt jeton bütçesini aşıyor
        return 0.0
        
    # Bilgi yoğunluğunu hesapla
    tokens = tokenize(response)
    unique_tokens = set(tokens)
    
    # Benzersiz jeton oranı
    unique_ratio = len(unique_tokens) / token_count if token_count > 0 else 0
    
    # Jeton kullanım oranı
    utilization_ratio = token_count / max_tokens
    
    # İdeal kullanım, bütçenin yaklaşık %80-90'ıdır
    if utilization_ratio > 0.9:
        utilization_score = 1.0 - ((utilization_ratio - 0.9) * 10)  # Sınıra çok yakın olduğu için cezalandır
    else:
        utilization_score = utilization_ratio / 0.9  # %90 kullanım = 1.0 olacak şekilde ölçekle
    
    # Metrikleri birleştir (ağırlıklı ortalama)
    efficiency = (unique_ratio * 0.7) + (utilization_score * 0.3)
    
    return efficiency

# ------------------------------------------------------------------------------
# Nöral Alan Puanlama Fonksiyonları
# ------------------------------------------------------------------------------

def score_field_resonance(response: str, field: Any) -> float:
    """
    Bir yanıtın bir nöral alanla ne kadar iyi rezonansa girdiğini puanlar.
    
    Args:
        response: Model yanıtı
        field: Nöral alan nesnesi
        
    Returns:
        Rezonans puanı (0.0 ile 1.0 arası)
    """
    try:
        # Alanın yerleşik ölçümünü kullanmayı dene
        return field.measure_resonance(response)
    except (AttributeError, TypeError):
        try:
            # Alandan çekicileri almayı dene
            attractors = _get_field_attractors(field)
            if not attractors:
                return 0.5  # Çekici yoksa nötr puan
                
            # Her çekiciyle rezonansı hesapla
            total_resonance = 0.0
            total_weight = 0.0
            
            for attractor_pattern, attractor_strength in attractors:
                # Rezonans için basit jeton örtüşmesi
                response_tokens = set(tokenize(response))
                attractor_tokens = set(tokenize(attractor_pattern))
                
                overlap = jaccard_similarity(response_tokens, attractor_tokens)
                
                # Çekici gücüne göre ağırlıklandır
                total_resonance += overlap * attractor_strength
                total_weight += attractor_strength
            
            # Ortalama rezonans
            if total_weight > 0:
                avg_resonance = total_resonance / total_weight
            else:
                avg_resonance = 0.0
                
            return avg_resonance
            
        except Exception as e:
            logger.warning(f"Alan rezonansı hesaplanamadı: {e}")
            return 0.5  # Başarısızlık durumunda nötr puan

def score_field_coherence(response: str, field: Any) -> float:
    """
    Bir yanıtın bir nöral alanın yapısıyla ne kadar tutarlı olduğunu puanlar.
    
    Args:
        response: Model yanıtı
        field: Nöral alan nesnesi
        
    Returns:
        Tutarlılık puanı (0.0 ile 1.0 arası)
    """
    try:
        # Alanın yerleşik ölçümünü kullanmayı dene
        return field.measure_coherence(response)
    except (AttributeError, TypeError):
        try:
            # Alandan desenleri almayı dene
            patterns = _get_field_patterns(field)
            if not patterns:
                return 0.5  # Desen yoksa nötr puan
                
            # Yanıtı cümlelere ayır
            sentences = extract_sentences(response)
            if not sentences:
                return 0.0
                
            # Her cümle için alan desenleriyle tutarlılığı hesapla
            sentence_coherence = []
            
            for sentence in sentences:
                # Desenlerle rezonansı hesapla
                sentence_tokens = set(tokenize(sentence))
                
                max_resonance = 0.0
                for pattern, _ in patterns:
                    pattern_tokens = set(tokenize(pattern))
                    resonance = jaccard_similarity(sentence_tokens, pattern_tokens)
                    max_resonance = max(max_resonance, resonance)
                
                sentence_coherence.append(max_resonance)
            
            # Genel tutarlılık, ortalama ve tutarlılığı birleştirir
            avg_coherence = sum(sentence_coherence) / len(sentence_coherence)
            consistency = 1.0 - (max(sentence_coherence) - min(sentence_coherence))
            
            coherence = (avg_coherence * 0.7) + (consistency * 0.3)
            
            return coherence
            
        except Exception as e:
            logger.warning(f"Alan tutarlılığı hesaplanamadı: {e}")
            return 0.5  # Başarısızlık durumunda nötr puan

def score_field_stability_impact(response: str, field: Any, before_state: Optional[Dict[str, Any]] = None) -> float:
    """
    Bir yanıtın alan kararlılığı üzerindeki etkisini puanlar.
    
    Args:
        response: Model yanıtı
        field: Yanıttan sonraki nöral alan nesnesi
        before_state: Yanıttan önceki isteğe bağlı alan durumu
        
    Returns:
        Kararlılık etki puanı (0.0 ile 1.0 arası)
    """
    try:
        # Alanın yerleşik ölçümünü kullanmayı dene
        current_stability = field.measure_stability()
        
        if before_state:
            # Kararlılık değişikliğini hesapla
            prev_stability = before_state.get("stability", 0.5)
            stability_change = current_stability - prev_stability
            
            # Pozitif değişiklik iyi, negatif değişiklik kötüdür
            if stability_change >= 0:
                # Kararlılıkta iyileşme
                return min(1.0, 0.5 + stability_change)
            else:
                # Kararlılıkta azalma
                return max(0.0, 0.5 + stability_change)
        else:
            # Önceki durum yok, yalnızca mevcut kararlılığı kullan
            return current_stability
            
    except (AttributeError, TypeError):
        logger.warning("Alan desteği olmadan kararlılık etkisi hesaplanamaz")
        return 0.5  # Nötr puan

def _get_field_attractors(field: Any) -> List[Tuple[str, float]]:
    """Bir alan nesnesinden çekicileri çıkarır."""
    try:
        # Çekicilere doğrudan erişmeyi dene
        return [(attractor['pattern'], attractor['strength']) 
                for attractor in field.attractors.values()]
    except (AttributeError, TypeError):
        # Alternatif yöntemleri dene
        try:
            return field.get_attractors()
        except (AttributeError, TypeError):
            return []

def _get_field_patterns(field: Any) -> List[Tuple[str, float]]:
    """Bir alan nesnesinden desenleri çıkarır."""
    try:
        # Duruma doğrudan erişmeyi dene
        return [(pattern, strength) for pattern, strength in field.state.items()]
    except (AttributeError, TypeError):
        # Alternatif yöntemleri dene
        try:
            return field.get_patterns()
        except (AttributeError, TypeError):
            return []

# ------------------------------------------------------------------------------
# Protokol Puanlama Fonksiyonları
# ------------------------------------------------------------------------------

def score_protocol_adherence(response: str, protocol: Any) -> float:
    """
    Bir yanıtın bir protokol yapısına ne kadar iyi uyduğunu puanlar.
    
    Args:
        response: Model yanıtı
        protocol: Protokol nesnesi veya tanımı
        
    Returns:
        Uygunluk puanı (0.0 ile 1.0 arası)
    """
    # Protokol adımlarını çıkar
    steps = _extract_protocol_steps(protocol)
    if not steps:
        return 0.0
        
    # Yanıttaki her adımın kanıtını kontrol et
    step_scores = []
    
    for step in steps:
        step_name = step.get("name", "")
        step_keywords = _extract_step_keywords(step)
        
        if step_keywords:
            # Yanıttaki anahtar kelimeleri kontrol et
            response_lower = response.lower()
            matches = sum(1 for keyword in step_keywords if keyword.lower() in response_lower)
            score = matches / len(step_keywords)
        else:
            # Anahtar kelime yok, adım adını kontrol et
            score = 1.0 if step_name.lower() in response.lower() else 0.0
        
        step_scores.append(score)
    
    # Genel uygunluk puanı
    adherence = sum(step_scores) / len(step_scores)
    
    # Sırayı takip etme bonusu
    sequence_bonus = 0.0
    response_sentences = extract_sentences(response)
    
    # Adımların doğru sırada görünüp görünmediğini kontrol et
    last_step_pos = -1
    steps_in_order = 0
    
    for i, step in enumerate(steps):
        step_name = step.get("name", "").lower()
        step_keywords = [kw.lower() for kw in _extract_step_keywords(step)]
        
        # Yanıttaki adımın konumunu bul
        step_pos = -1
        for j, sentence in enumerate(response_sentences):
            sentence_lower = sentence.lower()
            if step_name in sentence_lower or any(kw in sentence_lower for kw in step_keywords):
                step_pos = j
                break
        
        if step_pos > last_step_pos and step_pos >= 0:
            steps_in_order += 1
            last_step_pos = step_pos
    
    if len(steps) > 1:
        sequence_bonus = steps_in_order / (len(steps) - 1)
    
    # Puanları birleştir
    final_score = (adherence * 0.7) + (sequence_bonus * 0.3)
    
    return final_score

def _extract_protocol_steps(protocol: Any) -> List[Dict[str, Any]]:
    """Bir protokol nesnesinden veya tanımından adımları çıkarır."""
    if isinstance(protocol, dict):
        # Protokol bir sözlüktür
        return protocol.get("process", [])
    else:
        # Protokol özniteliklerine erişmeyi dene
        try:
            return protocol.process_steps
        except AttributeError:
            try:
                return protocol.process
            except AttributeError:
                return []

def _extract_step_keywords(step: Dict[str, Any]) -> List[str]:
    """
    Bir protokol adımından anahtar kelimeleri çıkarır.
    """
    keywords = []
    
    # Adım adını ekle
    if "name" in step:
        keywords.append(step["name"])
    
    # Anahtar kelime olabilecek diğer değerleri ekle
    for key, value in step.items():
        if key != "name" and isinstance(value, str):
            keywords.append(value)
    
    return keywords

def score_protocol_output_match(response: str, protocol: Any) -> float:
    """
    Bir yanıtın beklenen protokol çıktısıyla ne kadar iyi eşleştiğini puanlar.
    
    Args:
        response: Model yanıtı
        protocol: Protokol nesnesi veya tanımı
        
    Returns:
        Çıktı eşleşme puanı (0.0 ile 1.0 arası)
    """
    # Beklenen çıktı şemasını çıkar
    output_schema = _extract_protocol_output(protocol)
    if not output_schema:
        return 0.5  # Şema yoksa nötr puan
    
    # Yanıttan yapılandırılmış çıktıyı çıkarmayı dene
    extracted_output = _extract_structured_output(response)
    if not extracted_output:
        return 0.0  # Yapılandırılmış çıktı bulunamadı
    
    # Beklenen anahtarların kapsamını kontrol et
    expected_keys = set(output_schema.keys())
    actual_keys = set(extracted_output.keys())
    
    # Anahtar kapsamını hesapla
    if expected_keys:
        key_coverage = len(expected_keys.intersection(actual_keys)) / len(expected_keys)
    else:
        key_coverage = 0.0
    
    # Biçim uygunluğunu kontrol et
    format_adherence = 1.0
    
    for key in expected_keys.intersection(actual_keys):
        expected_format = output_schema[key]
        actual_value = extracted_output[key]
        
        # Beklenen formata göre basit biçim kontrolü
        if isinstance(expected_format, str) and "<" in expected_format and ">" in expected_format:
            # Bu bir değişken referansıdır, biçim kontrol edilemez
            pass
        elif isinstance(expected_format, dict) and isinstance(actual_value, dict):
            # İç içe yapıyı kontrol et
            expected_nested_keys = set(expected_format.keys())
            actual_nested_keys = set(actual_value.keys())
            
            if expected_nested_keys:
                nested_coverage = len(expected_nested_keys.intersection(actual_nested_keys)) / len(expected_nested_keys)
                format_adherence *= nested_coverage
        elif isinstance(expected_format, list) and isinstance(actual_value, list):
            # Liste yapısını kontrol et
            format_adherence *= 1.0  # Liste formatını kolayca kontrol edemez
        elif type(expected_format) != type(actual_value):
            # Tür uyuşmazlığı
            format_adherence *= 0.5
    
    # Puanları birleştir
    output_match = (key_coverage * 0.7) + (format_adherence * 0.3)
    
    return output_match

def _extract_protocol_output(protocol: Any) -> Dict[str, Any]:
    """Bir protokol nesnesinden veya tanımından çıktı şemasını çıkarır."""
    if isinstance(protocol, dict):
        # Protokol bir sözlüktür
        return protocol.get("output", {})
    else:
        # Protokol özniteliklerine erişmeyi dene
        try:
            return protocol.output_schema
        except AttributeError:
            try:
                return protocol.output
            except AttributeError:
                return {}

def _extract_structured_output(response: str) -> Dict[str, Any]:
    """
    Bir yanıttan yapılandırılmış çıktıyı çıkarır.
    """
    # JSON çıktısını bulmayı dene
    json_pattern = r'```(?:json)?\s*({[\s\S]*?})\s*```'
    json_matches = re.findall(json_pattern, response)
    
    if json_matches:
        try:
            return json.loads(json_matches[0])
        except json.JSONDecodeError:
            pass
    
    # Anahtar-değer çiftlerini bulmayı dene
    output = {}
    
    # "Çıktı:" veya "Sonuç:" bölümünü ara
    output_section_pattern = r'(?:Çıktı|Sonuç):\s*\n([\s\S]*?)(?:\n\n|\Z)'
    section_matches = re.findall(output_section_pattern, response)
    
    if section_matches:
        section = section_matches[0]
        
        # Anahtar-değer çiftlerini çıkar
        for line in section.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                output[key.strip()] = value.strip()
    
    return output

# ------------------------------------------------------------------------------
# Kapsamlı Puanlama
# ------------------------------------------------------------------------------

def score_response(response: str, query: str, context: Optional[Dict[str, Any]] = None, 
                 reference: Optional[str] = None, field: Optional[Any] = None,
                 protocol: Optional[Any] = None) -> Dict[str, float]:
    """
    Bir model yanıtının kapsamlı puanlaması.
    
    Args:
        response: Model yanıtı
        query: Orijinal sorgu
        context: İsteğe bağlı bağlam sözlüğü
        reference: İsteğe bağlı referans yanıtı
        field: İsteğe bağlı nöral alan
        protocol: İsteğe bağlı protokol
        
    Returns:
        Puanlar sözlüğü
    """
    scores = {}
    
    # Temel puanlar
    scores["relevance"] = score_relevance(response, query)
    scores["coherence"] = score_coherence(response)
    scores["comprehensiveness"] = score_comprehensiveness(response, reference)
    scores["conciseness"] = score_conciseness(response, reference)
    scores["accuracy"] = score_accuracy(response, reference)
    scores["token_efficiency"] = score_token_efficiency(response)
    
    # Alan sağlanmışsa alan puanları
    if field:
        scores["field_resonance"] = score_field_resonance(response, field)
        scores["field_coherence"] = score_field_coherence(response, field)
    
    # Protokol sağlanmışsa protokol puanları
    if protocol:
        scores["protocol_adherence"] = score_protocol_adherence(response, protocol)
        scores["protocol_output_match"] = score_protocol_output_match(response, protocol)
    
    # Genel puanı hesapla
    # Önem derecesine göre farklı yönler için farklı ağırlıklar
    weights = {
        "relevance": 0.20,
        "coherence": 0.15,
        "comprehensiveness": 0.15,
        "conciseness": 0.10,
        "accuracy": 0.20,
        "token_efficiency": 0.10,
        "field_resonance": 0.05,
        "field_coherence": 0.05,
        "protocol_adherence": 0.05,
        "protocol_output_match": 0.05
    }
    
    # Yalnızca var olan puanları kullan
    overall_score = 0.0
    total_weight = 0.0
    
    for metric, score in scores.items():
        if metric in weights:
            overall_score += score * weights[metric]
            total_weight += weights[metric]
    
    if total_weight > 0:
        scores["overall"] = overall_score / total_weight
    else:
        scores["overall"] = 0.0
    
    return scores

# ------------------------------------------------------------------------------
# Kullanım Örnekleri
# ------------------------------------------------------------------------------

def basic_scoring_example():
    """Temel puanlama fonksiyonları örneği."""
    query = "Nöral ağların basit terimlerle nasıl çalıştığını açıklayın."
    
    response = """
    Nöral ağlar, insan beyninden esinlenen hesaplama modelleridir. 
    Katmanlar halinde düzenlenmiş nöron adı verilen birbirine bağlı düğümlerden oluşurlar.
    Her nöron girdi alır, bir dönüşüm uygular ve çıktıyı bir sonraki katmana iletir.
    Verilerle eğitim yoluyla, nöral ağlar desenleri tanımayı ve tahminlerde bulunmayı öğrenir.
    Nöronlar arasındaki bağlantıların gücü, hataları en aza indirmek için eğitim sırasında ayarlanır.
    Geri yayılım adı verilen bu süreç, nöral ağların örneklerden öğrenmesini sağlar.
    """
    
    reference = """
    Nöral ağlar, insan beyninin yapısından esinlenen hesaplama sistemleridir.
    Bilgiyi işleyen düğüm katmanlarından (nöronlar) oluşurlar.
    Bilgi, girdi katmanlarından gizli katmanlar aracılığıyla çıktı katmanlarına akar.
    Nöronlar arasındaki her bağlantının eğitim sırasında ayarlanan bir ağırlığı vardır.
    Nöral ağlar, örnekleri işleyerek ve hataları azaltmak için ağırlıkları ayarlayarak öğrenir.
    Bu eğitim süreci, yeni veriler üzerinde desenleri tanımalarını ve tahminlerde bulunmalarını sağlar.
    Uygulamalar arasında görüntü tanıma, dil işleme ve oyun oynama yer alır.
    """
    
    # Alaka düzeyini puanla
    relevance = score_relevance(response, query)
    print(f"Alaka düzeyi puanı: {relevance:.2f}")
    
    # Tutarlılığı puanla
    coherence = score_coherence(response)
    print(f"Tutarlılık puanı: {coherence:.2f}")
    
    # Kapsamlılığı puanla
    comprehensiveness = score_comprehensiveness(response, reference)
    print(f"Kapsamlılık puanı: {comprehensiveness:.2f}")
    
    # Özlülüğü puanla
    conciseness = score_conciseness(response, reference)
    print(f"Özlülük puanı: {conciseness:.2f}")
    
    # Doğruluğu puanla
    accuracy = score_accuracy(response, reference)
    print(f"Doğruluk puanı: {accuracy:.2f}")
    
    # Jeton verimliliğini puanla
    token_efficiency = score_token_efficiency(response)
    print(f"Jeton verimliliği puanı: {token_efficiency:.2f}")
    
    # Kapsamlı puanlama
    scores = score_response(response, query, reference=reference)
    print("\nKapsamlı puanlar:")
    for metric, score in scores.items():
        print(f"- {metric}: {score:.2f}")

if __name__ == "__main__":
    # Örnek kullanım
    basic_scoring_example()
