from matches import get_soon_matches, get_last_matches
from lineup import get_players
from utils import WORDS
from random import randint

# if the check for words is equal one of this, lambda formates the response
intent_router = {
    "despedida": lambda: format_goobye_response(),
    "about": lambda: format_about_response(),
    "assistir": lambda: format_watch_response(),
    "resultados": lambda: format_lastResults_response(get_last_matches()),
    "proximo_jogo": lambda: format_match_response(get_soon_matches()),
    "elenco": lambda: format_lineup_response(get_players())
}

def main():
    message = 'valeu panterinha'
    response = match_response(message)
    print(response)

def match_response(message):
    intent = check_response(message)
    if intent in intent_router:
        return intent_router[intent]()
    return 'Não entendi.'

def check_response(message):
    message = message.lower()
    for word in WORDS:
        matches = [kw for kw in word["keywords"] if kw in message]
        if word['name'] == 'despedida' and len(matches) >= 1:
            return word['name']

        if len(matches) >= 2:
            return word["name"]
    return None

def format_goobye_response():
    despedidas = [
    "💣 Desarmando por aqui. Até a próxima!",
    "🔫 Tô saindo no strafe... até mais, lenda!",
    "🧢 Partiu base! Volta sempre, hein?",
    "🎯 Headshot de informação, missão cumprida. Até logo!",
    "🚀 Flashbang na despedida! Te vejo no próximo round.",
    "🥇 MVP da conversa! Volta quando quiser.",
    "🐾 A selva te espera, pantera! Até a próxima.",
    "🐆 Valeu, FURIOSO! A torcida nunca para.",
    "🔥 A FURIA não dorme... e a gente se fala logo!",
    "🖤 Segue o rugido! Até a próxima batalha.",
    "🐾 Fé na call e orgulho na camisa. Até mais!",
    "✌️ Falou, parceiro! Até daqui a pouco.",
    "👋 É isso, tamo junto! Volta sempre.",
    "🫡 Missão dada, missão cumprida. Até mais, guerreiro!",
    "🍻 Valeu pela resenha! Te espero no próximo drop."
    ]
    i = randint(0, len(despedidas) - 1)
    return (f"{despedidas[i]}\n"
            f"E não se esqueça! "
            f"{format_about_response()}")

    return
def format_about_response():
    return ("Para saber mais da galera Furiosa, cola com a gente! 🐾\n"
            "#️⃣ X: https://x.com/FURIA\n"
            "📷 Instagram: https://www.instagram.com/furiagg/\n"
            "📺 Twitch: https://www.twitch.tv/furiatv\n"
    )

def format_watch_response():
    return (
        "🔎 Quer saber onde assistir? É só me perguntar: 'Qual o próximo jogo?' que eu te ajudo! ✅\n"
        "🌐 E se ainda ficar na dúvida, dá uma conferida no imenso da galera: O Gaules (twitch.tv/gaules);\n"
        "Ou dá uma olhadinha nas transmissões oficiais do evento. Pode ter coisa boa rolando por lá!"
    )


def format_match_response(matches):
    if not matches:
        return 'As panteras não têm um jogo recente marcado :('
    match = matches[0]
    return (
        f"🏆 Próximo jogo da FURIA: {match['event']}\n"
        f"🆚 Adversário: {match['enemy']}\n"
        f"📅 Data prevista: {match['date']}\n"
        f"📺 Onde assistir: Confira todos os lugares para assistir aqui: {match['livestreams']}"
    )

def format_lastResults_response(matches):
    if not matches:
        return 'As panteras não saíram da toca faz um tempo...'
    
    response = "📜 Últimos jogos da FURIA:\n"
    for match in matches:
        response += (
            f"🏆 Evento: {match['event']}\n"
            f"🆚 Adversário: {match['enemy']}\n"
            f"📅 Data: {match['date']}\n"
            f"🔢 Resultado: {match.get('score', 'N/A')}\n"
            f"{'-'*30}\n"
        )
    return response.strip()


def format_lineup_response(lineup):
    players = lineup.get("players", [])
    coach = lineup.get("coach", "Desconhecido")

    response = "👥 Elenco da FURIA:\n"
    response += "🎮 Jogadores: " + ', '.join(players) + "\n"
    response += f"🧠 Coach: {coach}"

    return response

if __name__ == '__main__':
    main()
