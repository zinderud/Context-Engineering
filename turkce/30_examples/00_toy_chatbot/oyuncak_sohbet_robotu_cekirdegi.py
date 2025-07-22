# `oyuncak_sohbet_robotu_cekirdegi.py`: Alan Operasyonları ile Çekirdek Uygulama

Bu modül, oyuncak sohbet robotumuzun temel işlevselliğini uygular ve basit komut-yanıt desenlerinden karmaşık alan operasyonlarına ve meta-özyineli yeteneklere kadar olan ilerlemeyi gösterir.

## Kavramsal Genel Bakış

Uygulamamız, bağlam mühendisliğinin biyolojik metaforunu takip eder:

```
┌─────────────────────────────────────────────────────────┐
│             BAĞLAM MÜHENDİSLİĞİ KATMANLARI                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│    ╭───────────╮                                        │
│    │   Meta    │    Kendi kendini iyileştirme ve uyarlama │
│    │ Özyineli  │                                        │
│    ╰───────────╯                                        │
│          ▲                                              │
│          │                                              │
│    ╭───────────╮                                        │
│    │   Alan    │    Bağlam, çekiciler ve rezonans ile     │
│    │Operasyonları│    sürekli bir ortam olarak            │
│    ╰───────────╯                                        │
│          ▲                                              │
│          │                                              │
│    ╭───────────╮                                        │
│    │  Organlar │    Özelleşmiş fonksiyonlara sahip        │
│    │ (Sistemler)│    koordineli sistemler                │
│    ╰───────────╯                                        │
│          ▲                                              │
│          │                                              │
│    ╭───────────╮                                        │
│    │  Hücreler │    Hafıza ve durum ile bağlam            │
│    │ (Hafıza)  │                                        │
│    ╰───────────╯                                        │
│          ▲                                              │
│          │                                              │
│    ╭───────────╮                                        │
│    │ Moleküller│    Örneklerle talimatlar               │
│    │ (Bağlam)  │                                        │
│    ╰───────────╯                                        │
│          ▲                                              │
│          │                                              │
│    ╭───────────╮                                        │
│    │  Atomlar  │    Basit talimatlar                    │
│    │ (Komutlar)│                                        │
│    ╰───────────╯                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Uygulama

Sohbet robotumuzu, atomik katmandan başlayıp daha karmaşık operasyonlara doğru ilerleyerek adım adım oluşturalım.

```python
import json
import time
import uuid
import math
import random
from typing import Dict, List, Any, Optional, Union, Tuple

# Bu modülleri daha sonra uyguladıktan sonra içe aktaracağız
# from protocol_shells import AttractorCoEmerge, FieldResonanceScaffold, RecursiveMemoryAttractor, FieldSelfRepair
# from context_field import ContextField

class OyuncakBaglamSohbetRobotu:
    """
    Atomlardan meta-özyineli operasyonlara kadar bağlam mühendisliği ilkelerini gösteren bir oyuncak sohbet robotu.
    
    Bu sohbet robotu şu aşamalardan geçer:
    - Atomlar: Temel komutlar ve yanıtlar
    - Moleküler: Bağlam kombinasyonları ve örnekler
    - Hücreler: Hafıza ve durum yönetimi
    - Organlar: Koordineli sistem davranışları
    - Alanlar: Sürekli anlamsal operasyonlar
    - Meta-Özyineli: Kendi kendini geliştirme yetenekleri
    """
    
    def __init__(self, name: str = "BaglamBot", field_params: Dict[str, Any] = None):
        """Sohbet robotunu yapılandırılabilir alan parametreleriyle başlatır."""
        self.name = name
        self.field_params = field_params or {
            "decay_rate": 0.05,
            "boundary_permeability": 0.8,
            "resonance_bandwidth": 0.6,
            "attractor_threshold": 0.7
        }
        
        # Katmanları atomlardan meta-özyineliye kadar başlat
        self._init_atomic_layer()
        self._init_molecular_layer()
        self._init_cellular_layer()
        self._init_organ_layer()
        self._init_field_layer()
        self._init_meta_recursive_layer()
        
        # Metrikler ve durum
        self.conversation_count = 0
        self.metrics = {
            "resonance_score": 0.0,
            "coherence_score": 0.0,
            "self_improvement_count": 0,
            "emergence_detected": False
        }
    
    def _init_atomic_layer(self):
        """Atomik katmanı başlatır: temel komut-yanıt desenleri."""
        self.basic_responses = {
            "greeting": [
                "Merhaba! Bugün size nasıl yardımcı olabilirim?",
                "Selam! Sizin için ne yapabilirim?",
                "Hoş geldiniz! Nasıl yardımcı olabilirim?"
            ],
            "farewell": [
                "Hoşça kalın! İyi günler!",
                "Görüşmek üzere! Tekrar bekleriz.",
                "Bir dahaki sefere kadar!"
            ],
            "thanks": [
                "Rica ederim!",
                "Memnuniyetle!",
                "Yardımcı olabildiğime sevindim!"
            ],
            "unknown": [
                "Anladığımdan emin değilim. Tekrar ifade edebilir misiniz?",
                "Bu konuda henüz bilgim yok.",
                "Hala öğreniyorum ve bu konuda bilgim yok."
            ]
        }
    
    def _init_molecular_layer(self):
        """Moleküler katmanı başlatır: bağlam kombinasyonları ve örnekler."""
        # Yaygın konuşma desenleri için az sayıda örnek tanımla
        self.examples = {
            "question_answering": [
                {"input": "Adın ne?", "output": f"Benim adım {self.name}."},
                {"input": "Ne yapabilirsin?", "output": "Sohbet edebilir ve bağlam mühendisliği ilkelerini gösterebilirim."},
                {"input": "Nasıl çalışıyorsun?", "output": "Temel yanıtlardan alan operasyonlarına kadar aşamalı bağlam mühendisliği katmanları aracılığıyla çalışıyorum."}
            ],
            "clarification": [
                {"input": "Bana bundan daha fazla bahset", "output": "Memnuniyetle ayrıntılandırırım. Hangi özel yönü ilginizi çekiyor?"},
                {"input": "Anlamadım", "output": "Farklı bir şekilde açıklamama izin verin. Hangi kısım kafa karıştırıcı?"}
            ]
        }
    
    def _init_cellular_layer(self):
        """Hücresel katmanı başlatır: hafıza ve durum yönetimi."""
        # Konuşma hafızası
        self.memory = {
            "short_term": [],  # Son mesajlar
            "long_term": [],   # Hatırlamaya değer önemli bilgiler
            "user_info": {},   # Kullanıcı hakkında bilgi
            "conversation_state": "greeting"  # Mevcut konuşma aşaması
        }
        
        # Hafıza parametreleri
        self.memory_params = {
            "short_term_capacity": 10,  # Hatırlanacak maksimum son mesaj sayısı
            "long_term_threshold": 0.7  # Uzun süreli hafıza için önem eşiği
        }
    
    def _init_organ_layer(self):
        """Organ katmanını başlatır: koordineli sistem davranışları."""
        # Uzmanlaşmış alt sistemler
        self.subsystems = {
            "intent_classifier": self._classify_intent,
            "response_generator": self._generate_response,
            "memory_manager": self._manage_memory,
            "conversation_flow": self._manage_conversation_flow
        }
        
        # Alt sistem düzenleme ayarları
        self.orchestration = {
            "sequence": ["intent_classifier", "memory_manager", "conversation_flow", "response_generator"],
            "feedback_loops": True,
            "parallel_processing": False
        }
    
    def _init_field_layer(self):
        """Alan katmanını başlatır: sürekli anlamsal operasyonlar."""
        # Çekici dinamikleri için bağlam alanı
        self.context_field = None  # Bunu daha sonra ContextField ile başlatacağız
        
        # Protokol kabukları
        self.protocols = {
            "attractor_co_emerge": None,        # AttractorCoEmerge örneği olacak
            "field_resonance": None,            # FieldResonanceScaffold örneği olacak
            "memory_attractor": None,           # RecursiveMemoryAttractor örneği olacak
            "field_repair": None                # FieldSelfRepair örneği olacak
        }
        
        # Alan operasyonları parametreleri
        self.field_ops = {
            "attractor_formation_enabled": True,
            "resonance_amplification": 0.3,
            "memory_persistence_strength": 0.6,
            "self_repair_threshold": 0.4
        }
    
    def _init_meta_recursive_layer(self):
        """Meta-özyineli katmanı başlatır: kendi kendini geliştirme yetenekleri."""
        # Kendi kendini geliştirme mekanizmaları
        self.meta_recursive = {
            "self_monitoring": True,
            "improvement_strategies": [
                "response_quality_enhancement",
                "memory_optimization",
                "conversation_flow_refinement",
                "attractor_tuning"
            ],
            "evolution_history": [],
            "improvement_threshold": 0.5
        }
    
    def chat(self, message: str) -> str:
        """
        Bir kullanıcı mesajını işler ve tüm katmanları kullanarak bir yanıt üretir.
        
        Args:
            message: Kullanıcının girdi mesajı
            
        Returns:
            str: Sohbet robotunun yanıtı
        """
        # Konuşma sayısını güncelle
        self.conversation_count += 1
        
        # Her katmandan geçirerek işle
        # 1. Atomik katman: Temel anlama
        intent = self._classify_intent(message)
        
        # 2. Moleküler katman: Bağlam uygula
        context_enriched_message = self._apply_context(message, intent)
        
        # 3. Hücresel katman: Hafızayı güncelle
        self._update_memory(message, intent)
        
        # 4. Organ katmanı: Alt sistemleri koordine et
        subsystem_result = self._coordinate_subsystems(context_enriched_message, intent)
        
        # 5. Alan katmanı: Alan operasyonlarını uygula
        field_result = self._apply_field_operations(subsystem_result, intent)
        
        # 6. Meta-özyineli katman: Kendi kendini geliştirme
        if self.conversation_count % 5 == 0:  # Her 5 konuşmada bir meta-özyineli uygula
            self._apply_meta_recursion()
        
        # Son yanıtı oluştur
        response = field_result if field_result else subsystem_result
        
        # Etkileşimle hafızayı güncelle
        self._update_memory_with_interaction(message, response, intent)
        
        return response
    
    def _classify_intent(self, message: str) -> str:
        """Kullanıcının mesajının niyetini sınıflandırır (atomik operasyon)."""
        message_lower = message.lower()
        
        # Basit kural tabanlı niyet sınıflandırması
        if any(word in message_lower for word in ["merhaba", "selam", "hey"]):
            return "greeting"
        elif any(word in message_lower for word in ["güle güle", "hoşça kal", "görüşürüz"]):
            return "farewell"
        elif any(word in message_lower for word in ["teşekkürler", "teşekkür ederim"]):
            return "thanks"
        elif "?" in message:
            return "question"
        elif message_lower.startswith(("ne", "kim", "nerede", "ne zaman", "neden", "nasıl")):
            return "question"
        elif any(word in message_lower for word in ["açıkla", "bana anlat", "tanımla"]):
            return "information_request"
        else:
            return "statement"
    
    def _apply_context(self, message: str, intent: str) -> str:
        """Mesaja bağlamsal bilgi uygular (moleküler operasyon)."""
        # Mesajı örneklerden gelen bağlamla zenginleştir
        context_enriched = message
        
        # Varsa ilgili örnekleri ekle
        if intent == "question" and "question_answering" in self.examples:
            # Burada sadece kavramı gösteriyoruz - gerçek bir sistemde,
            # mesajı örnek bağlamla değiştirebiliriz
            context_enriched = f"{message} [Bağlam: {intent} örneklerine benzer]"
        
        return context_enriched
    
    def _update_memory(self, message: str, intent: str) -> None:
        """Hafızayı yeni bilgilerle günceller (hücresel operasyon)."""
        # Kısa süreli hafızaya ekle
        self.memory["short_term"].append({
            "message": message,
            "intent": intent,
            "timestamp": time.time()
        })
        
        # Gerekirse kısa süreli hafızayı kırp
        if len(self.memory["short_term"]) > self.memory_params["short_term_capacity"]:
            self.memory["short_term"] = self.memory["short_term"][-self.memory_params["short_term_capacity"]:]
        
        # Varsa kullanıcı bilgilerini çıkar ve sakla
        if intent == "statement" and ("adım" in message.lower() or "ben" in message.lower()):
            # Çok basit kullanıcı bilgisi çıkarma
            if "adım" in message.lower():
                name = message.lower().split("adım")[1].strip()
                self.memory["user_info"]["name"] = name
            elif "ben" in message.lower():
                description = message.lower().split("ben")[1].strip()
                self.memory["user_info"]["description"] = description
    
    def _coordinate_subsystems(self, message: str, intent: str) -> str:
        """Mesajı işlemek için alt sistemleri koordine eder (organ operasyonu)."""
        result = message
        
        # Alt sistemleri belirtilen sırayla yürüt
        for system_name in self.orchestration["sequence"]:
            system_function = self.subsystems.get(system_name)
            if system_function:
                if system_name == "intent_classifier":
                    # Zaten çağrıldı, atla
                    continue
                elif system_name == "response_generator":
                    result = system_function(result, intent)
                elif system_name == "memory_manager":
                    system_function(result, intent)  # Hafızayı günceller, dönüş gerekmez
                elif system_name == "conversation_flow":
                    result = system_function(result, intent)  # Akışa göre mesajı değiştirebilir
        
        return result
    
    def _generate_response(self, message: str, intent: str) -> str:
        """Niyet ve bağlama göre bir yanıt üretir (organ operasyonu)."""
        # Bu niyet için temel bir yanıtımız olup olmadığını kontrol et
        if intent in self.basic_responses:
            responses = self.basic_responses[intent]
            return random.choice(responses)
        
        # Soruları ele al
        if intent == "question":
            # Sohbet robotu hakkında olup olmadığını kontrol et
            message_lower = message.lower()
            if "sen" in message_lower and any(word in message_lower for word in ["adın", "kimsin", "nesin"]):
                return f"Ben {self.name}, bağlam mühendisliği ilkelerini gösteren bir oyuncak sohbet robotuyum."
            elif "bağlam mühendisliği" in message_lower:
                return ("Bağlam mühendisliği, bir yapay zeka sisteminin gördüğü tüm bağlamı, temel komutlardan karmaşık alan operasyonlarına kadar tasarlama ve yönetme pratiğidir.")
            else:
                # Genel soru yanıtı
                return "Bu ilginç bir soru. Ben basit bir gösterim sohbet robotuyum, bu yüzden bilgim sınırlı."
        
        # Bilgi taleplerini ele al
        if intent == "information_request":
            message_lower = message.lower()
            if "bağlam mühendisliği" in message_lower:
                return ("Bağlam mühendisliği, atomlardan (temel komutlar) moleküllere (bağlam kombinasyonları), "
                        "hücrelere (hafıza), organlara (koordineli sistemler), alanlara (sürekli operasyonlar) ve meta-özyineli "
                        "(kendi kendini geliştirme) katmanlarına kadar ilerler.")
            elif any(word in message_lower for word in ["kendin", "yeteneklerin", "ne yapabilirsin"]):
                return ("Ben bağlam mühendisliği ilkelerinin bir gösterimiyim. Temel sohbetler yapabilirim, "
                        "bilgileri hatırlayabilir ve alan operasyonlarının ve meta-özyinelinin basit bir şekilde nasıl çalıştığını gösterebilirim.")
            else:
                return "Bunu açıklamaktan memnuniyet duyarım, ancak bir oyuncak sohbet robotu olarak sınırlı bilgim var."
        
        # Varsayılan olarak genel bir yanıt ver
        return "Bir ifade belirttiğinizi anlıyorum. Bağlam mühendisliği hakkında daha fazla bilgi edinmek ister misiniz?"
    
    def _manage_memory(self, message: str, intent: str) -> None:
        """Hafıza operasyonlarını yönetir (hücresel operasyon)."""
        # Uzun süreli hafıza için önemi değerlendir
        importance = 0.0
        
        # Basit önem sezgileri
        if intent in ["question", "information_request"]:
            importance += 0.3
        if "bağlam mühendisliği" in message.lower():
            importance += 0.4
        if intent == "greeting" and self.conversation_count == 1:
            importance += 0.5  # İlk selamlama biraz önemlidir
        
        # Yeterince önemliyse uzun süreli hafızada sakla
        if importance >= self.memory_params["long_term_threshold"]:
            self.memory["long_term"].append({
                "message": message,
                "intent": intent,
                "importance": importance,
                "timestamp": time.time()
            })
    
    def _manage_conversation_flow(self, message: str, intent: str) -> str:
        """Konuşma akışını yönetir (organ operasyonu)."""
        current_state = self.memory["conversation_state"]
        
        # Durum geçişleri
        if intent == "greeting":
            self.memory["conversation_state"] = "engaged"
            return message
        elif intent == "farewell":
            self.memory["conversation_state"] = "ended"
            return message
        elif current_state == "ended" and intent != "greeting":
            # Konuşma sona erdiyse ancak kullanıcı devam ederse
            self.memory["conversation_state"] = "engaged"
            return f"{message} [Not: Konuşma yeniden başlatılıyor]"
        
        # Akış değişikliği gerekmez
        return message
    
    def _apply_field_operations(self, message: str, intent: str) -> str:
        """Alan operasyonlarını uygular (alan katmanı)."""
        # Henüz tam alan operasyonlarını uygulamadığımız için,
        # etkilerini bazı yer tutucu davranışlarla simüle edeceğiz
        
        # Çekici dinamiklerini simüle et
        # Gerçek bir uygulamada, protokol kabuklarını kullanırdık
        if intent == "question" and random.random() > 0.7:
            # Çekici yakınsamasını simüle et - yanıtı derinleştir
            return self._enhance_response_with_field(message, intent)
        
        # Alan operasyonu uygulanmadı
        return message
    
    def _enhance_response_with_field(self, message: str, intent: str) -> str:
        """Simüle edilmiş alan operasyonlarını kullanarak bir yanıtı geliştirir."""
        # Bu, gerçek alan operasyonları için bir yer tutucudur
        # Tam bir uygulamada, alan protokollerini kullanırdık
        
        base_response = self._generate_response(message, intent)
        
        # Alan etkilerini simüle et
        field_enhancements = [
            "\n\nBuna bir alan perspektifinden bakıldığında, bağlam mühendisliğinin daha basit komut yaklaşımlarında bulunmayan ortaya çıkan özellikler yarattığını ekleyebilirim.",
            "\n\nBir çekici dinamikleri açısından, sorunuz doğal olarak bağlam alanlarında kararlı desenler oluşturan birkaç anahtar kavramla ilgilidir.",
            "\n\nRezonans operasyonları aracılığıyla, bu konunun yapay zeka sistemlerinin zamanla nasıl anlayış geliştirdiği gibi daha geniş bir temaya bağlandığını hissedebiliyorum."
        ]
        
        # Metrikleri güncelle
        self.metrics["resonance_score"] = min(1.0, self.metrics["resonance_score"] + 0.1)
        
        return base_response + random.choice(field_enhancements)
    
    def _apply_meta_recursion(self) -> None:
        """Meta-özyineli kendi kendini geliştirmeyi uygular (meta-özyineli katman)."""
        # Bu, gerçek meta-özyineli operasyonlar için bir yer tutucudur
        
        # Kendi kendini geliştirmeyi simüle et
        improvement_strategies = self.meta_recursive["improvement_strategies"]
        strategy = random.choice(improvement_strategies)
        
        if strategy == "response_quality_enhancement":
            # Yanıt kalitesini iyileştirmeyi simüle et
            for intent, responses in self.basic_responses.items():
                if random.random() > 0.7 and len(responses) < 10:
                    new_response = f"Bağlam duyarlı bir {self.name} olarak, {intent} yapmak isterim."
                    if new_response not in responses:
                        self.basic_responses[intent].append(new_response)
        
        elif strategy == "memory_optimization":
            # Hafıza optimizasyonunu simüle et
            self.memory_params["long_term_threshold"] = max(0.1, min(0.9, self.memory_params["long_term_threshold"] + random.uniform(-0.1, 0.1)))
        
        # İyileştirmeyi kaydet
        self.meta_recursive["evolution_history"].append({
            "strategy": strategy,
            "timestamp": time.time(),
            "conversation_count": self.conversation_count,
            "metrics_before": self.metrics.copy()
        })
        
        # Metrikleri güncelle
        self.metrics["self_improvement_count"] += 1
        
        # Ortaya çıkan davranışı kontrol et
        if self.metrics["self_improvement_count"] > 3 and random.random() > 0.8:
            self.metrics["emergence_detected"] = True
    
    def _update_memory_with_interaction(self, message: str, response: str, intent: str) -> None:
        """Hafızayı tam etkileşimle günceller."""
        interaction = {
            "user_message": message,
            "bot_response": response,
            "intent": intent,
            "timestamp": time.time()
        }
        
        # Kısa süreli hafızaya ekle
        self.memory["short_term"].append(interaction)
        
        # Gerekirse kırp
        if len(self.memory["short_term"]) > self.memory_params["short_term_capacity"]:
            self.memory["short_term"] = self.memory["short_term"][-self.memory_params["short_term_capacity"]:]
    
    def meta_improve(self) -> Dict[str, Any]:
        """
        Meta-özyineli kendi kendini geliştirmeyi manuel olarak tetikler.
        
        Returns:
            Dict[str, Any]: Yapılan iyileştirmeler hakkında bilgi
        """
        self._apply_meta_recursion()
        
        # İyileştirme hakkında bilgi döndür
        return {
            "improvement_count": self.metrics["self_improvement_count"],
            "last_strategy": self.meta_recursive["evolution_history"][-1]["strategy"],
            "emergence_detected": self.metrics["emergence_detected"],
            "metrics": self.metrics
        }
    
    def show_field_state(self) -> Dict[str, Any]:
        """
        Bağlam alanının mevcut durumunu gösterir.
        
        Returns:
            Dict[str, Any]: Mevcut alan durumu bilgisi
        """
        # Bu, gerçek alan durumu görselleştirmesi için bir yer tutucudur
        # Tam bir uygulamada, gerçek alan durumunu gösterirdik
        
        return {
            "attractors": [
                {"pattern": "bağlam mühendisliği kavramları", "strength": 0.8},
                {"pattern": "kullanıcı etkileşim desenleri", "strength": 0.6},
                {"pattern": "sohbet robotu yetenekleri", "strength": 0.7}
            ],
            "resonance_score": self.metrics["resonance_score"],
            "field_stability": 0.7 + (0.1 * self.metrics["self_improvement_count"]),
            "memory_integration": 0.5 + (0.1 * len(self.memory["long_term"]))
        }

# Kullanım gösterimi
if __name__ == "__main__":
    # Sohbet robotunu başlat
    chatbot = OyuncakBaglamSohbetRobotu()
    
    # Basit bir sohbeti göster
    print("Kullanıcı: Merhaba!")
    print(f"{chatbot.name}: {chatbot.chat('Merhaba!')}")
    
    print("\nKullanıcı: Bağlam mühendisliği nedir?")
    print(f"{chatbot.name}: {chatbot.chat('Bağlam mühendisliği nedir?')}")
    
    print("\nKullanıcı: Bana çekiciler hakkında daha fazla bilgi verebilir misin?")
    print(f"{chatbot.name}: {chatbot.chat('Bana çekiciler hakkında daha fazla bilgi verebilir misin?')}")
    
    # Alan durumunu göster
    print("\nAlan Durumu:")
    field_state = chatbot.show_field_state()
    for key, value in field_state.items():
        print(f"{key}: {value}")
    
    # Meta-iyileştirmeyi tetikle
    print("\nMeta-iyileştirme tetikleniyor:")
    improvement_info = chatbot.meta_improve()
    print(f"İyileştirme sayısı: {improvement_info['improvement_count']}")
    print(f"Son strateji: {improvement_info['last_strategy']}")
    print(f"Ortaya çıkış tespit edildi: {improvement_info['emergence_detected']}")

```