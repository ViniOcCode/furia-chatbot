from flask import Blueprint, render_template, jsonify, request

chatbot = Blueprint('chatbot', __name__)

matches = ["partida", "jogo", "jogos",]

@chatbot.route('chat', method=['POST'])
def chat():
    message = request.json.get('message')

