"""Enhanced NLP service for intent recognition and text processing."""
import re
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from rapidfuzz import fuzz, process
import unidecode

from app.models.utils import WORDS


@dataclass
class IntentResult:
    """Result of intent classification."""
    intent: Optional[str] = None
    confidence: float = 0.0
    matched_keywords: List[str] = None
    entities: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.matched_keywords is None:
            self.matched_keywords = []
        if self.entities is None:
            self.entities = {}


class NLPService:
    """Enhanced Natural Language Processing service."""
    
    def __init__(self, confidence_threshold: float = 65):
        self.confidence_threshold = confidence_threshold
        self.logger = logging.getLogger(__name__)
        self._keyword_to_intent = self._build_keyword_mapping()
        self._intent_patterns = self._build_intent_patterns()
    
    def _build_keyword_mapping(self) -> Dict[str, str]:
        """Build mapping from normalized keywords to intents."""
        mapping = {}
        for intent_data in WORDS:
            intent_name = intent_data['name']
            for keyword in intent_data['keywords']:
                normalized = self._normalize_text(keyword)
                mapping[normalized] = intent_name
        return mapping
    
    def _build_intent_patterns(self) -> Dict[str, List[str]]:
        """Build regex patterns for each intent."""
        patterns = {}
        for intent_data in WORDS:
            intent_name = intent_data['name']
            # Create regex patterns for better matching
            intent_patterns = []
            for keyword in intent_data['keywords']:
                # Create pattern that allows partial matches
                escaped = re.escape(keyword.lower())
                pattern = rf'\b{escaped}\b'
                intent_patterns.append(pattern)
            patterns[intent_name] = intent_patterns
        return patterns
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for better matching."""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove accents
        text = unidecode.unidecode(text)
        
        # Remove special characters except spaces and numbers
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _extract_team_entities(self, text: str) -> Dict[str, str]:
        """Extract team-related entities from text."""
        from app.models.utils import TEAMS
        
        entities = {}
        normalized_text = self._normalize_text(text)
        
        for team_id, team_data in TEAMS.items():
            for keyword in team_data['keywords']:
                if self._normalize_text(keyword) in normalized_text:
                    entities['team'] = team_id
                    entities['team_name'] = team_data['name']
                    break
            if 'team' in entities:
                break
        
        # Default to main team if no specific team mentioned
        if 'team' not in entities:
            entities['team'] = 'main'
            entities['team_name'] = TEAMS['main']['name']
        
        return entities
    
    def _fuzzy_match_intent(self, text: str) -> Tuple[Optional[str], float, List[str]]:
        """Use fuzzy matching to find best intent."""
        if not text:
            return None, 0.0, []
        
        # Try exact pattern matching first
        for intent_name, patterns in self._intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    self.logger.debug(f"Pattern match found for intent '{intent_name}': {pattern}")
                    return intent_name, 95.0, [pattern]
        
        # Fall back to fuzzy matching
        keywords = list(self._keyword_to_intent.keys())
        if not keywords:
            return None, 0.0, []
        
        try:
            result = process.extractOne(
                text,
                keywords,
                scorer=fuzz.token_set_ratio
            )
            
            if result:
                best_keyword, score, _ = result
                if score >= self.confidence_threshold:
                    intent = self._keyword_to_intent[best_keyword]
                    self.logger.debug(f"Fuzzy match found: intent='{intent}', score={score}")
                    return intent, float(score), [best_keyword]
        
        except Exception as e:
            self.logger.error(f"Error in fuzzy matching: {e}")
        
        return None, 0.0, []
    
    def _enhance_confidence(self, intent: str, text: str, base_confidence: float) -> float:
        """Enhance confidence based on additional factors."""
        enhanced_score = base_confidence
        
        # Boost confidence if multiple keywords from same intent are found
        intent_keywords = []
        for intent_data in WORDS:
            if intent_data['name'] == intent:
                intent_keywords = intent_data['keywords']
                break
        
        keyword_matches = 0
        for keyword in intent_keywords:
            if self._normalize_text(keyword) in self._normalize_text(text):
                keyword_matches += 1
        
        if keyword_matches > 1:
            # Boost by 5 points per additional keyword, max 20 points
            boost = min(20, (keyword_matches - 1) * 5)
            enhanced_score = min(100, enhanced_score + boost)
            self.logger.debug(f"Confidence boosted by {boost} for {keyword_matches} keyword matches")
        
        # Reduce confidence for very short messages
        if len(text.strip()) < 3:
            enhanced_score *= 0.8
            self.logger.debug("Confidence reduced for short message")
        
        return enhanced_score
    
    def classify_intent(self, message: str) -> IntentResult:
        """Classify the intent of a message with enhanced NLP."""
        if not message or not message.strip():
            return IntentResult()
        
        try:
            # Normalize the input
            normalized_text = self._normalize_text(message)
            self.logger.info(f"Classifying intent for: '{message[:50]}...'")
            
            # Extract entities
            entities = self._extract_team_entities(message)
            
            # Find best intent match
            intent, confidence, matched_keywords = self._fuzzy_match_intent(normalized_text)
            
            if intent:
                # Enhance confidence with additional factors
                enhanced_confidence = self._enhance_confidence(intent, normalized_text, confidence)
                
                result = IntentResult(
                    intent=intent,
                    confidence=enhanced_confidence,
                    matched_keywords=matched_keywords,
                    entities=entities
                )
                
                self.logger.info(f"Intent classified: {intent} (confidence: {enhanced_confidence:.1f}%)")
                return result
            
            else:
                self.logger.info("No intent found above threshold")
                return IntentResult(entities=entities)
                
        except Exception as e:
            self.logger.error(f"Error classifying intent: {e}")
            return IntentResult()
    
    def validate_message(self, message: str, max_length: int = 500) -> Tuple[bool, str]:
        """Validate input message."""
        if not message:
            return False, "Mensagem vazia"
        
        if not message.strip():
            return False, "Mensagem contém apenas espaços"
        
        if len(message) > max_length:
            return False, f"Mensagem muito longa (máximo {max_length} caracteres)"
        
        # Check for potentially harmful content
        harmful_patterns = [
            r'<script',
            r'javascript:',
            r'data:text/html'
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return False, "Conteúdo não permitido"
        
        return True, "Válida"
    
    def set_confidence_threshold(self, threshold: float) -> None:
        """Update confidence threshold."""
        if 0 <= threshold <= 100:
            self.confidence_threshold = threshold
            self.logger.info(f"Confidence threshold updated to {threshold}")
        else:
            raise ValueError("Threshold must be between 0 and 100")