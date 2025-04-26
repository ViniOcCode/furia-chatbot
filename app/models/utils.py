from datetime import datetime, timezone
from zoneinfo import ZoneInfo

DOMAIN = 'https://www.hltv.org/'
URL = f'{DOMAIN}team/8297/furia#' 
URLT = f'{DOMAIN}team/12774/flyquest#'
HEADERS = {'User-Agent': 'Mozzila/5.0'}

# this could be smaller and more smart but this will work
WORDS = [
    {"name": "madebywho", 
    "keywords": [
        "feito", "criado", "desenvolvido", "por", "quem", "fez", "vinicius",
        "programador", "autor", "criador", "responsável", "engenheiro",
        "construiu", "idealizador", "sabe", "de", "que", "teve", "ideia",
        "construção", "mentor", "designer", "arquiteto","dev", "coder", 
        "codou", "isso", "bot", "aqui", 
    ]},

    {"name": "proximo_jogo", 
    "keywords": [
        "quando", "próximo", "jogo", "partida", "game", "data", "horário",
        "adversário", "calendário", "agenda", "dia", "mês", "ano", "hora",
        "confronto", "oponente", "duelo", "match", "contra", "times", "time",
        "disputar", "jogar", "competir" 
    ]},

    {"name": "eventos",
    "keywords": [
        "evento", "organização", "agenda", "calendário", "datas", 
        "horário", "participação", "campeonato", "jogos", "próximos", 
        "competições", "torneio", "resultados", "vitórias", "derrotas", 
        "títulos", "liga", "valve", "csgo", "cs2", "esports", "cenário", 
        "competitivo", "campeonatos", "eventos"
    ]},

    {"name": "resultados",
    "keywords": [
        "último","ultimo", "jogo", "resultados", "placar", "score", "como", 
        "terminou","foi", "vitória", "derrota",  "resultado","final", 
        "aconteceu", "histórico", "recente","detalhes", "resumo", 
        "quem", "ganhou", "perdeu", "empatou", "competição", "torneio", 
        "campeonato","partidas", "jogaram"
    ]},

    {"name": "elenco", 
    "keywords": [
        "quem", "joga", "jogadores", "time", "equipe", "titulares", "reservas",
        "lineup", "formação", "escalação", "membros", "integrantes", "nomes",
        "lista", "convocados", "presentes", "participantes", "atuais",
        "atletas", "seleção", "grupo"
    ]},

    {"name": "assistir", 
    "keywords": [
        "onde", "assistir", "ver", "transmissão", "stream", "live", "vivo",
        "canal", "plataforma", "aovivo", "online", "tv", "emissora", "site",
        "link", "grátis", "pago", "youtube", "twitch", "app", "serviço",
        "acessar", "encontrar", "encontro", "achar", "procurar"
    ]},

    {"name": "despedida",
    "keywords": [
        "tchau", "falou", "até", "adeus", "flw", "vou", "vazei", "bye", "logo",
        "breve", "mais", "depois", "inté", "partiu", "fui", "nessa", "xau", "valeu",
        "obrigado", "obrigada", "nos", "vemos", "próxima", "tarde", "sair", "eu",
        "você", "já", "era", "fora", "cansei", "chega", "basta", "parar", "agora",
        "ok", "tudo", "bem", "então", "né", "vamos", "combinado", "depois"
    ]},

    {"name": "cumprimento",
    "keywords": [
        "oi", "olá", "eae", "salve", "fala", "bom", "dia", "boa", "tarde", "noite",
        "tudo", "bem", "vai", "tranquilo", "boa", "suave", "está",
        "estou", "você", "aí", "coé", "hey", "hello", "hi", "certo", "jóia",
        "beleza", "tá", "ce", "tá", "em", "cima", "tranquilo", "tudo", "joia"
    ]},

    {"name": "about",
    "keywords": [
        "instagram", "twitter", "x", "tiktok", "redes", "sociais", "facebook",
        "youtube", "linkedin", "discord", "perfil", "conta", "seguir", "seguidores",
        "oficial", "link", "url", "handle", "@", "hashtag", "post", "feed", "stories",
        "vídeos", "fotos", "mídia", "digital", "online", "encontrar",
        "achar", "procurar", "acessar", "ver", "saber", "sobre", 
         "contato", "canal", "site", "aplicativo", "app", "web"
    ]},

    {"name": "funfact",
    "keywords": [
        "curiosidade", "fato", "interessante", "engraçado", "incrível", "sabia",
        "que", "você", "sabia", "me", "conta", "diga", "algo", "conte", "revelação",
        "segredo", "história", "anecdota", "trivia", "informação", "dado", "raro",
        "inexplicável", "surpreendente", "maneiro", "legal", "show", "uau", "como"
    ]}
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
    """Formata timestamps UNIX para o formato '<dia> às <horário>'"""
    timestamp = int(timestamp)
    # data-unix form hltv comes in ms
    dt_utc = datetime.fromtimestamp(timestamp / 1000 , tz=timezone.utc)

    dt_br = dt_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
    
    return dt_br.strftime("%d/%m às %Hh")

def format_unix_dates(start_unix, end_unix):
    """Formata timestamps UNIX para o formato 'dos dias <data1> até <data2>'"""
    tz = ZoneInfo("America/Sao_Paulo")  

    meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]

    # data-unix form hltv comes in ms
    start_dt = datetime.fromtimestamp(start_unix / 1000, tz=tz)
    end_dt = datetime.fromtimestamp(end_unix / 1000, tz=tz)
    
    start_str = f"{start_dt.day} de {meses[start_dt.month - 1]}"
    end_str = f"{end_dt.day} de {meses[end_dt.month - 1]}"
    
    return f"dos dias {start_str} até {end_str}"
