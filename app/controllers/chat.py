from flask import Blueprint, render_template, jsonify, request
from app.models.chatresponses import match_response, format_hello_response
from app.templates import *

chat = Blueprint('chat', __name__, static_folder='statics')

@chat.route('/')
def index():
    return render_template('index.html')

@chat.route('/chat', methods=['POST'])
def chatBot():
    message = request.json.get('message', '')
    reply = match_response(message)

    return jsonify({'response': reply})

@chat.route('/welcome')
def welcome():
    welcome = format_hello_response()

    return jsonify({'welcome': welcome})
