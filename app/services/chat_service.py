"""Chat service for handling chatbot conversations."""
import logging
from typing import Dict, Any, Optional
from flask import current_app

from app.services.nlp_service import NLPService, IntentResult
from app.models.utils import TEAMS


class ChatService:
    """Service for handling chat conversations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.nlp_service = NLPService(
            confidence_threshold=current_app.config.get('DEFAULT_CONFIDENCE_THRESHOLD', 65)
        )
        self._intent_handlers = self._build_intent_handlers()
    
    def _build_intent_handlers(self) -> Dict[str, callable]:
        """Build mapping of intents to handler functions."""
        from app.models.chatresponses import (
            madebywho, format_hello_response, format_funfact_response,
            format_goobye_response, format_about_response, format_watch_response,
            format_lastResults_response, format_match_response, format_events_response,
            format_lineup_response, format_ranking_response, default_response
        )
        from app.models.matches import get_soon_matches, get_last_matches
        from app.models.lineup import get_players
        from app.models.events import get_events
        from app.models.ranking import get_ranking
        
        return {
            'madebywho': lambda team, entities: madebywho(),
            'cumprimento': lambda team, entities: format_hello_response(),
            'funfact': lambda team, entities: format_funfact_response(),
            'despedida': lambda team, entities: format_goobye_response(),
            'about': lambda team, entities: format_about_response(),
            'assistir': lambda team, entities: format_watch_response(),
            'resultados': lambda team, entities: self._handle_results(team),
            'proximo_jogo': lambda team, entities: self._handle_next_match(team),
            'eventos': lambda team, entities: self._handle_events(team),
            'elenco': lambda team, entities: self._handle_lineup(team),
            'ranking': lambda team, entities: self._handle_ranking(team)
        }
    
    def _handle_results(self, team: Dict[str, Any]) -> str:
        """Handle results request with error handling."""
        try:
            from app.models.matches import get_last_matches
            from app.models.chatresponses import format_lastResults_response
            matches = get_last_matches(team['url'])
            return format_lastResults_response(matches, team['name'])
        except Exception as e:
            self.logger.error(f"Error getting results for {team['name']}: {e}")
            return f"Desculpe, não consegui buscar os resultados da {team['name']} no momento. Tente novamente mais tarde."
    
    def _handle_next_match(self, team: Dict[str, Any]) -> str:
        """Handle next match request with error handling."""
        try:
            from app.models.matches import get_soon_matches
            from app.models.chatresponses import format_match_response
            matches = get_soon_matches(team['url'])
            return format_match_response(matches, team['name'])
        except Exception as e:
            self.logger.error(f"Error getting next match for {team['name']}: {e}")
            return f"Desculpe, não consegui buscar o próximo jogo da {team['name']} no momento. Tente novamente mais tarde."
    
    def _handle_events(self, team: Dict[str, Any]) -> str:
        """Handle events request with error handling."""
        try:
            from app.models.events import get_events
            from app.models.chatresponses import format_events_response
            events = get_events(team['url'])
            return format_events_response(events, team['name'])
        except Exception as e:
            self.logger.error(f"Error getting events for {team['name']}: {e}")
            return f"Desculpe, não consegui buscar os eventos da {team['name']} no momento. Tente novamente mais tarde."
    
    def _handle_lineup(self, team: Dict[str, Any]) -> str:
        """Handle lineup request with error handling."""
        try:
            from app.models.lineup import get_players
            from app.models.chatresponses import format_lineup_response
            players = get_players(team['url'])
            return format_lineup_response(players, team['name'])
        except Exception as e:
            self.logger.error(f"Error getting lineup for {team['name']}: {e}")
            return f"Desculpe, não consegui buscar o elenco da {team['name']} no momento. Tente novamente mais tarde."
    
    def _handle_ranking(self, team: Dict[str, Any]) -> str:
        """Handle ranking request with error handling."""
        try:
            from app.models.ranking import get_ranking
            from app.models.chatresponses import format_ranking_response
            ranking = get_ranking(team['url'], team['name'])
            return format_ranking_response(ranking, team['name'])
        except Exception as e:
            self.logger.error(f"Error getting ranking for {team['name']}: {e}")
            return f"Desculpe, não consegui buscar o ranking da {team['name']} no momento. Tente novamente mais tarde."
    
    def _get_team_from_entities(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Get team data from extracted entities."""
        team_id = entities.get('team', 'main')
        return TEAMS.get(team_id, TEAMS['main'])
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process a chat message and return response."""
        try:
            # Validate message
            is_valid, validation_msg = self.nlp_service.validate_message(
                message, 
                current_app.config.get('MAX_MESSAGE_LENGTH', 500)
            )
            
            if not is_valid:
                self.logger.warning(f"Invalid message: {validation_msg}")
                return {
                    'response': f"❌ {validation_msg}",
                    'error': True,
                    'intent': None,
                    'confidence': 0
                }
            
            # Classify intent
            intent_result: IntentResult = self.nlp_service.classify_intent(message)
            
            # Get team from entities
            team = self._get_team_from_entities(intent_result.entities)
            
            # Generate response
            if intent_result.intent and intent_result.intent in self._intent_handlers:
                try:
                    response = self._intent_handlers[intent_result.intent](team, intent_result.entities)
                    
                    self.logger.info(f"Generated response for intent '{intent_result.intent}' with confidence {intent_result.confidence:.1f}%")
                    
                    return {
                        'response': response,
                        'error': False,
                        'intent': intent_result.intent,
                        'confidence': intent_result.confidence,
                        'team': team['name'],
                        'matched_keywords': intent_result.matched_keywords
                    }
                    
                except Exception as e:
                    self.logger.error(f"Error executing handler for intent '{intent_result.intent}': {e}")
                    from app.models.chatresponses import default_response
                    return {
                        'response': default_response(),
                        'error': True,
                        'intent': intent_result.intent,
                        'confidence': intent_result.confidence
                    }
            else:
                # No intent found or low confidence
                self.logger.info(f"No suitable intent found. Confidence: {intent_result.confidence:.1f}%")
                from app.models.chatresponses import default_response
                return {
                    'response': default_response(),
                    'error': False,
                    'intent': None,
                    'confidence': intent_result.confidence,
                    'team': team['name']
                }
                
        except Exception as e:
            self.logger.error(f"Unexpected error processing message: {e}")
            return {
                'response': "😅 Ops! Algo deu errado. Tente novamente em alguns segundos.",
                'error': True,
                'intent': None,
                'confidence': 0
            }
    
    def get_welcome_message(self) -> Dict[str, Any]:
        """Get welcome message for new conversations."""
        try:
            from app.models.chatresponses import format_hello_response
            response = format_hello_response()
            
            return {
                'welcome': response,
                'error': False
            }
        except Exception as e:
            self.logger.error(f"Error generating welcome message: {e}")
            return {
                'welcome': "Olá! Bem-vindo ao chatbot da FURIA! 🐾",
                'error': True
            }