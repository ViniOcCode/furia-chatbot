"""Chat controller with improved error handling and validation."""
import logging
from flask import Blueprint, render_template, jsonify, request, current_app

from app.services.chat_service import ChatService

# Create blueprint
chat = Blueprint('chat', __name__, static_folder='static')
logger = logging.getLogger(__name__)


@chat.route('/')
def index():
    """Render the main chat interface."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {e}")
        return jsonify({
            'error': 'Erro ao carregar a página',
            'message': 'Tente recarregar a página'
        }), 500


@chat.route('/chat', methods=['POST'])
def chat_endpoint():
    """Handle chat messages with improved validation and error handling."""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'error': 'Formato inválido',
                'message': 'Requisição deve ser JSON'
            }), 400
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Dados não encontrados',
                'message': 'Corpo da requisição está vazio'
            }), 400
        
        message = data.get('message', '').strip()
        if not message:
            return jsonify({
                'error': 'Mensagem vazia',
                'message': 'Por favor, digite uma mensagem'
            }), 400
        
        # Process message with chat service
        chat_service = ChatService()
        result = chat_service.process_message(message)
        
        # Log the interaction
        logger.info(f"Chat interaction - Intent: {result.get('intent', 'none')}, "
                   f"Confidence: {result.get('confidence', 0):.1f}%, "
                   f"Message length: {len(message)}")
        
        # Return only the response for backward compatibility
        # but include debug info in development
        response_data = {'response': result['response']}
        
        if current_app.debug:
            response_data.update({
                'debug': {
                    'intent': result.get('intent'),
                    'confidence': result.get('confidence'),
                    'team': result.get('team'),
                    'matched_keywords': result.get('matched_keywords', []),
                    'error': result.get('error', False)
                }
            })
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        return jsonify({
            'response': '😅 Ops! Algo deu errado. Tente novamente em alguns segundos.',
            'error': True
        }), 500


@chat.route('/welcome')
def welcome():
    """Get welcome message for new conversations."""
    try:
        chat_service = ChatService()
        result = chat_service.get_welcome_message()
        
        return jsonify({
            'welcome': result['welcome']
        })
        
    except Exception as e:
        logger.error(f"Error getting welcome message: {e}")
        return jsonify({
            'welcome': 'Olá! Bem-vindo ao chatbot da FURIA! 🐾',
            'error': True
        }), 500


@chat.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'FURIA Chatbot',
        'version': '2.0'
    })
