from datetime import datetime, timezone
from zoneinfo import ZoneInfo

DOMAIN = 'https://www.hltv.org/'
URL = f'{DOMAIN}team/8297/furia#' 
URLT = f'{DOMAIN}team/12774/flyquest#'
HEADERS = {'User-Agent': 'Mozzila/5.0'}

WORDS = [
    {"name": "madebywho", 
    "keywords": ["feito", "por", "quem", "fez", "vinicius"
                 "programador", "furia", "bonito", "legal", "trabalhador",
                 "esforçado", "made", "by", "who"
                 ]},


    {"name": "proximo_jogo", 
    "keywords": ["quando", "proximo", "jogo", 
                 "qual", "data", "partida", "game",
                 "games", "jogos", "vão", "quais"]},
                 

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

    {"name": "cumprimento",
    "keywords": [
        "eae", "oi", "salve", "olá",
        "tudo bem", "de boa", "como vai",
        ]},

    {"name": "about",
    "keywords": [
            "instagram", "twitter", "x", "tiktok", "redes", "sociais",
            "furia no insta", "furia no twitter", "furia no x",
            "furia nas redes", "onde seguir", "link da rede",
            "conta oficial", "canal da furia", "conta da furia",
            "social", "perfil", "perfil oficial"]},

 {"name": "funfact",
    "keywords": ["curiosidade", "me", "da", "dá",
                 "uma", "alguma", "quero", "funfact"
                 "curioso", "fato"]}
]

FUNFACT = {
    "sabia": [
        "A FURIA já participou de mais de 550 partidas desde sua estreia em 2018, mantendo uma taxa de vitória de aproximadamente 60%.",
        "A organização já conquistou 19 títulos de primeiro lugar em torneios, mostrando sua consistência no cenário competitivo.",
        "A FURIA é uma das poucas equipes brasileiras que frequentemente recebe convites diretos para torneios internacionais de alto nível.",
        "Drop foi um dos jogadores mais jovens a jogar um Major, se classificando com a FURIA num momento difícil e qualificando com uma performance impecável! Com 18 anos e 114 dias, a Pantera jogou o PGL Major Stockholm 2021!",
        "Yuurih, no último mapa da série contra a Entropiq valendo vaga nos playoffs, fez uma das jogadas mais icônicas (e que jogada bonita) do Major de 2021."
    ],
    "lembra": [
        "No IEM Rio Major 2022, a FURIA arrastou uma multidão absurda: mais de 1.4 milhão de pessoas assistindo. Foi uma das maiores audiências que um time BR já teve no CS.",
        "Desde que subiu pro cenário em 2017, a FURIA não para. Já marcou presença em vários Majors pesados, tipo Katowice 2019, DreamHack Dallas e ECS Season 7.",
        "A Red Bull até lançou um documentário deles, chamado 'FURIA: Road to Legends'. Mostra os bastidores da equipe, treinos, pressão... vale muito a pena assistir se curte CS de verdade.",
        "Em 2024, a equipe competiu no IEM Rio, mas foi eliminada nas semifinais pelos alemães da MOUZ, mesmo com o apoio fervoroso da torcida brasileira.",
        "Durante o PGL Major Stockholm 2021, a FURIA foi a equipe mais bem colocada da região das Américas, chegando até as quartas de final."
    ]
}

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
