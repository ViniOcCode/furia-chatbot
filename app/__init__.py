from flask import Flask

def create_app():
    app = Flask(__name__) 

    from app.controllers.chat import chatbot
    app.register_blueprint(chatbot, url_prefix='/')

    return app

