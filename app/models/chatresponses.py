from app.models.matches import get_soon_matches, get_last_matches
from app.models.lineup import get_players
from app.models.utils import WORDS, FUNFACT
import random

# if the check for words is equal one of this, lambda formates the response
intent_router = {
    'madebywho': lambda: madebywho(),
    'cumprimento': lambda: format_hello_response(),
    'funfact': lambda: format_funfact_response(),
    'despedida': lambda: format_goobye_response(),
    'about': lambda: format_about_response(),
    'assistir': lambda: format_watch_response(),
    'resultados': lambda: format_lastResults_response(get_last_matches()),
    'proximo_jogo': lambda: format_match_response(get_soon_matches()),
    'elenco': lambda: format_lineup_response(get_players())
}

def main():
    format_hello_response()

def match_response(message):
    intent = check_response(message)
    if intent in intent_router:
        return intent_router[intent]()
    return 'Não entendi.'

def check_response(message):
    message = message.lower()
    for word in WORDS:
        matches = [kw for kw in word['keywords'] if kw in message]
        if len(matches) >= 1:
            if word['name'] == 'despedida':
                return word['name']
            elif word['name'] == 'cumprimento':
                return word['name']

        if len(matches) >= 2:
            return word['name']
    return None

def madebywho():
    return (
        "Feito por Vinícius, com muito esforço e pouca dignidade.<br>"
        "FURIA, me contrata por favor... eu sei fazer uns ifs bem legais :)"
    )

def format_hello_response():
    greetings = [
        'Fala, Pantera! 🐾 Tudo certo?',
        'Salve! Pronto pra saber tudo da FURIA? 🔥',
        'E aí! Bora acompanhar os jogos da FURIA? 💣',
        'Bem-vindo ao radar das panteras! 🖤',
        'Chegou o torcedor fiel! 💪 Bora ver o que tem de novo?',
        'Fala aí! Preparado pro próximo stomp da FURIA? 😎',
        'Seja bem-vindo! Vamos ver o que tá rolando com a FURIA! 🎮',
        'Opa! Quer saber quando vai ser o próximo jogo? 😉',
        'Tá na hora do CS! Vamos de FURIA? 🐍',
        'Ei! Pronto pra conferir o lineup e os placares? 🏆'
    ]
    return (f'{random.choice(greetings)}<br><br>'
            f'Me pergunte algo como: "Qual vai ser o próximo jogo da Furia?" 🗓️<br><br>'
            f'Ou se quiser ouvir uma curiosidade: "Me fale uma curioisdade" 🧠<br><br>'
            f'Posso te falar também, placares: "Como foram os últimos jogos?" 🕹️'
        )

def format_goobye_response():
    despedidas = [
        '💣 Desarmando por aqui. Até a próxima!',
        '🔫 Tô saindo no strafe... até mais, lenda!',
        '🧢 Partiu base! Volta sempre, hein?',
        '🎯 Headshot de informação, missão cumprida. Até logo!',
        '🚀 Flashbang na despedida! Te vejo no próximo round.',
        '🥇 MVP da conversa! Volta quando quiser.',
        '🐾 A selva te espera, pantera! Até a próxima.',
        '🐆 Valeu, FURIOSO! A torcida nunca para.',
        '🔥 A FURIA não dorme... e a gente se fala logo!',
        '🖤 Segue o rugido! Até a próxima batalha.',
        '🐾 Fé na call e orgulho na camisa. Até mais!',
        '✌️ Falou, parceiro! Até daqui a pouco.',
        '👋 É isso, tamo junto! Volta sempre.',
        '🫡 Missão dada, missão cumprida. Até mais, guerreiro!',
        '🍻 Valeu pela resenha! Te espero no próximo drop.'
    ]
    return (f'{random.choice(despedidas)}<br>'
            f'E não se esqueça!<br>'
            f'{format_about_response()}'
        )

def format_about_response():
    return ('Para saber mais da galera Furiosa, cola com a gente! 🐾<br>'
            '#️⃣ X: https://x.com/FURIA<br>'
            '📷 Instagram: https://www.instagram.com/furiagg/<br>'
            '📺 Twitch: https://www.twitch.tv/furiatv<br>'
    )
def format_funfact_response():
    kw = random.choice(list(FUNFACT.keys()))
    if kw == 'sabia':
        return (f'Você sabia? 🔎<br>'
                f'{random.choice(FUNFACT["sabia"])} 🔮'
            )
    else:
        return (f'Você lembra? 🧠<br>'
                f'{random.choice(FUNFACT["lembra"])} 🐾'
            )

def format_watch_response():
    return (
        '🔎 Quer saber onde assistir? É só me perguntar: "Qual o próximo jogo?" que eu te ajudo! ✅<br><br>'
        '🌐 E se ainda ficar na dúvida, dá uma conferida no imenso da galera: <a href="https://www.twitch.tv/gaules" target="_blank">O Gaules</a>;<br>'
        'Ou dá uma olhadinha nas transmissões oficiais do evento. Pode ter coisa boa rolando por lá!'
    )


def format_match_response(matches):
    if not matches:
        return 'As panteras não têm um jogo recente marcado :('
    match = matches[0]
    return (
        f'🏆 Próximo jogo da FURIA: {match["event"]}<br>'
        f'🆚 Adversário: {match["enemy"]}<br>'
        f'📅 Data prevista: {match["date"]}<br>'
        f'📺 Onde assistir: Confira todos os lugares para assistir '
        f'<a href="{match['livestreams']}" target="_blank"> aqui </a>'
    )

def format_lastResults_response(matches):
    if not matches:
        return 'As panteras não saíram da toca faz um tempo...'
    
    response = '📜 Últimos jogos da FURIA:<br>'
    for match in matches:
        response += (
            f'🏆 Evento: {match["event"]}<br>'
            f'🆚 Adversário: {match["enemy"]}<br>'
            f'📅 Data: {match["date"]}<br>'
            f'🔢 Resultado: {match.get("score", "N/A")}'
            f'{'-'*30}\n'
        )
    return response.strip()


def format_lineup_response(lineup):
    players = lineup.get('players', [])
    coach = lineup.get('coach', 'Desconhecido')

    response = '👥 Elenco da FURIA:<br>'
    response += '🎮 Jogadores: ' + ', '.join(players) + '<br>'
    response += f'🧠 Coach: {coach}'

    return response

if __name__ == '__main__':
    main()