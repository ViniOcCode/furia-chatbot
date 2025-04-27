from app.models.matches import get_soon_matches, get_last_matches
from app.models.lineup import get_players
from app.models.events import get_events
from app.models.ranking import get_ranking
from app.models.utils import WORDS, FUNFACT, TEAMS
import random

# if the check for words is equal one of this, lambda formates the response
intent_router = {
    'madebywho': lambda team: madebywho(),
    'cumprimento': lambda team: format_hello_response(),
    'funfact': lambda team: format_funfact_response(),
    'despedida': lambda team: format_goobye_response(),
    'about': lambda team: format_about_response(),
    'assistir': lambda team: format_watch_response(),
    'resultados': lambda team: format_lastResults_response(get_last_matches(team['url']), team['name']),
    'proximo_jogo': lambda team: format_match_response(get_soon_matches(team['url']), team['name']),
    'eventos': lambda team: format_events_response(get_events(team['url']), team['name']),
    'elenco': lambda team: format_lineup_response(get_players(team['url']), team['name']),
    'ranking': lambda team: format_ranking_response(get_ranking(team['url'], team['name']), team['name'])
}

def main():
    format_hello_response()

def detect_team(message):
    message = message.lower()
    # gets name and information about teams
    for team_id, team_data in TEAMS.items():
        for kw in team_data['keywords']:
            # if name of team and context kw in user message
            if kw and kw in message:
                return TEAMS[team_id]
    return TEAMS['main']


def match_response(message):
    team = detect_team(message)
    intent = check_response(message)

    # searchs for context in intent_router and team variable
    if intent and intent in intent_router:
        return intent_router[intent](team)

    return default_response()

def default_response():
    return (
        'Não consegui entender, foi mal!<br>'
        'Aqui vai uma lista do que você pode me perguntar:<br>'
        '<ul style="list-style: none; padding: 0;">'
            '<li>🤖 Quem criou o bot</li>'
            '<li>🎲 Curiosidade aleatória</li>'
            '<li>🐱‍👤 Sobre a FURIA</li>'
            '<li>📺 Onde assistir aos jogos</li>'
            f'<li>📊 Resultados recentes ({TEAMS["main"]["name"]} ou {TEAMS["female"]["name"]})</li>'
            f'<li>🥇 Ranqueamento global e nacional({TEAMS["main"]["name"]} ou {TEAMS["female"]["name"]})</li>'
            f'<li>🎯 Próximo jogo ({TEAMS["main"]["name"]} ou {TEAMS["female"]["name"]})</li>'
            f'<li>📅 Próximos eventos ({TEAMS["main"]["name"]} ou {TEAMS["female"]["name"]})</li>'
            f'<li>🧑‍🤝‍🧑 Elenco atual ({TEAMS["main"]["name"]} ou {TEAMS["female"]["name"]})</li>'
        '</ul>'
    )
def check_response(message):
    message = message.lower()
    
    # Ordem de prioridade dos intents
    priority_order = [
        'despedida', 'cumprimento',  # checks if bye or hello
        'proximo_jogo', 'resultados', # majors intents
        'ranking', 'elenco', 'eventos', 
        'assistir', 'about',
        'funfact', 'madebywho'       # less priority
    ]
    
    # checks priority order
    for intent_name in priority_order:
        word = next(w for w in WORDS if w['name'] == intent_name)
        if any(kw in message for kw in word['keywords']):
            return intent_name
    
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
            f'{default_response()}'
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
            f'E não se esqueça:<br>'
            f'{format_about_response()}'
        )

def format_about_response():
    return ('Para saber mais da galera Furiosa, cola com a gente! 🐾<br>'
            '#️⃣ <a href="https://x.com/FURIA" target="_blank">X</a><br>'
            '📷 <a href="https://www.instagram.com/furiagg/" target="_blank">Instagram</a><br>'
            '📺 <a href="https://www.twitch.tv/furiatv" target="_blank">Twitch</a><br>'
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

def format_ranking_response(ranking, team_name):
    return (
        f'Ranqueamento da {team_name}, '
        f'de acordo com <a href="https://www.hltv.org/ranking/teams/" target="_blank">hltv rank</a>:<br><br>'
        f'Posição Global 🌎: {ranking['world']}<br>'
        f'Posição Nacional 🇧🇷: {ranking['regional']}<br>'
    )
def format_match_response(matches, team_name):
    if not matches:
        return (
                f'As panteras da {team_name} não têm um jogo recente marcado 😔<br><br>'
                f'Mas vale dar uma conferida nos eventos que estão por vir, que tal? 🔎<br>'
                f'🔮 Me pergunta ai: "quais eventos estão por vir para o {team_name}?"'
                )
    match = matches[0]
    return (
        f'🏆 Próximo jogo da FURIA: {match["event"]}<br>'
        f'🆚 Adversário: {match["enemy"]}<br>'
        f'📅 Data prevista: {match["date"]}<br>'
        f'📺 Onde assistir: Confira todos os lugares para assistir '
        f'<a href="{match['livestreams']}" target="_blank"> aqui </a>'
    )

def format_lastResults_response(matches, team_name):
    if not matches:
        return (f'As panteras da {team_name} não saíram da toca faz um tempo...<br>')
    
    response = f'📜 Últimos jogos da {team_name}:<br><br>'
    for match in matches:
        response += (
            f'🏆 Evento: {match["event"]}<br>'
            f'🆚 Adversário: {match["enemy"]}<br>'
            f'📅 Data: {match["date"]}<br>'
            f'🔢 Resultado:<br>{team_name} {match.get("score", "N/A")}<br>'
            f'📺 Replays: '
            f'<a href="{match['livestreams']}" target="_blank">hltv.tv</a><br>'
            f'{'-'*29}<br>'
        )
    return response.strip()

def format_events_response(events, team_name):
    if not events:
        return f'As panteras da {team_name}parecem não ter nenhum atividade pela frente'

    response = 'As próximas aparições das panteras serão em:<br><br>'
    for event in events:
        response += (
            f'🕹️ {event['event']}<br>'
            f'📆 {event['date']}<br>'
            f'{'-'*29}<br>'
        )
    
    return response.strip()

def format_lineup_response(lineup, team_name):
    players = lineup.get('players', [])
    coach = lineup.get('coach', 'Desconhecido')

    response = f'👥 Elenco da {team_name}:<br>'
    response += '🎮 Jogadores: ' + ', '.join(players) + '<br>'
    response += f'🧠 Coach: {coach}'

    return response

if __name__ == '__main__':
    main()