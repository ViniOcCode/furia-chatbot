from datetime import datetime, timezone
from zoneinfo import ZoneInfo

DOMAIN = 'https://www.hltv.org/'
URL = f'{DOMAIN}team/8297/furia#' 
URLT = f'{DOMAIN}team/12774/flyquest#'
HEADERS = {'User-Agent': 'Mozzila/5.0'}

WORDS = [
    {"name": "proximo_jogo", 
    "keywords": ["quando", "proximo", "jogo", 
                 "qual", "data", "partida", "game",
                 "games"]},
                 

    {"name": "resultados",
    "keywords": [
        "último", "ultimos", "últimos", "jogos", "jogo", 
        "resultados", "placar", "resultado", 
        "aconteceu", "partidas", "aconteceram",
        "game", "games"]},

    {"name": "elenco", 
    "keywords": ["quem", "joga", "elenco", "jogar", "qual", 
                 "line", "lineup", "jogadores", "quais", "banco", 
                 "reserva"]},

    {"name": "assistir", 
    "keywords": ["onde", "assistir", "posso", "tem", "lugar",
                 "stream", "live", "ao vivo", "oficial", "canal",
                 "transmissão", "jogo", "game", "partida"]},

    {"name": "despedida",
    "keywords": [
        "tchau", "falou", "até", "valeu", "adeus",
        "fui", "flw", "vazei", "nos vemos", "see ya", "bye",
        "até mais", "partiu", "até logo", "abraço"
        ]},

    {"name": "about",
    "keywords": [
            "instagram", "twitter", "x", "tiktok", "redes", "sociais",
            "furia no insta", "furia no twitter", "furia no x",
            "furia nas redes", "onde seguir", "link da rede",
            "conta oficial", "canal da furia", "conta da furia",
            "social", "perfil", "perfil oficial"]}
]

# extensive use of get_text
def extract_text(row):
    return row.get_text(strip=True) if row else None

# formatting date
def date_format(timestamp):
    timestamp_ms = int(timestamp)
    timestamp = timestamp_ms // 1000
    dt_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)

    dt_br = dt_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
    
    return dt_br.strftime("%d/%m às %Hh")
