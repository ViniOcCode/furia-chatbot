"""FURIA Chatbot Application Factory."""
import logging
import os
from flask import Flask

from config import config


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config.get(config_name, config['default']))
    config[config_name].init_app(app)
    
    # Configure logging
    if app.config.get('ENABLE_LOGGING', True):
        setup_logging(app)
    
    # Register blueprints
    from app.controllers.chat import chat
    app.register_blueprint(chat, url_prefix='/')
    
    # Register error handlers
    register_error_handlers(app)
    
    return app


def setup_logging(app):
    """Setup application logging."""
    if not app.debug and not app.testing:
        # Production logging setup
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = logging.FileHandler('logs/furia_chatbot.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('FURIA Chatbot startup')
    else:
        # Development logging setup
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )


def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        return {
            'error': 'Requisição inválida',
            'message': 'Verifique os dados enviados'
        }, 400
    
    @app.errorhandler(404)
    def not_found(error):
        return {
            'error': 'Recurso não encontrado',
            'message': 'A página solicitada não existe'
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {
            'error': 'Erro interno do servidor',
            'message': 'Algo deu errado. Tente novamente mais tarde.'
        }, 500

