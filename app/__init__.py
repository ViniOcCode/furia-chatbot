from flask import Flask

def create_app():
    myapp = Flask(__name__) 

    from app.controllers.chat import chat
    myapp.register_blueprint(chat, url_prefix='/')

    return myapp

