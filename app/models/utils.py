from datetime import datetime, timezone
from zoneinfo import ZoneInfo

DOMAIN = 'https://www.hltv.org/'
HEADERS = {'User-Agent': 'Mozzila/5.0'}

TEAMS = {
    'main': {
        'name': 'FURIA',
        'url': f'{DOMAIN}team/8297/furia#',
        'keywords': [
            'masculino', 'principal', 'main', 'primary',
            'masculina', 'meninos', 'garotos', 'boys',
        ]
    },
    'female': {
        'name': 'FURIA Fe',
        'url': f'{DOMAIN}team/10976/furia-fe#',
        'keywords': [
            'feminino', 'female', 'fe', 'women', 'girls', 'meninas',
            'feminina','squad','panteras', 'garotas', 
        ]
    }
}

WORDS = [
    {   
        'name': 'madebywho', 
        'keywords': 
        [
            'criador', 'dev', 'vinicius', 'autor', 'desenvolvedor',
            'coder', 'engenheiro', 'construiu', 'idealizador', 'pai',
            'mentor', 'arquiteto', 'designer', 'responsável', 'cérebro',
            'bot', 'criou', 'fez', 'programou', 'construção'
        ]
    },
    {   'name': 'proximo_jogo', 
        'keywords': [
            'próximo', 'jogo', 'partida', 'match', 'confronto',
            'duelo', 'encontro', 'disputa', 'pega', 'jogão',
            'calendário', 'agenda', 'data', 'horário', 'quando',
            'próxima', 'schedule', 'fixture', 'opponent', 'adversário'
        ]
    },
    {   'name': 'eventos',
        'keywords': [
            'evento', 'campeonato', 'torneio', 'major', 'qualifier',
            'playoffs', 'final', 'etapa', 'fase', 'circuito',
            'liga', 'copa', 'championship', 'qualify', 'eliminatórias',
            'grupos', 'mata-mata', 'md3', 'bo3', 'md1', 'bo1', 'eventos'
        ]
    },
    {   'name': 'resultados',
        'keywords': [
            'resultado', 'placar', 'score', 'vitória', 'derrota',
            'empate', 'ganhou', 'perdeu', 'venceu', 'perdeu',
            'histórico', 'recente', 'último', 'desfecho', 'resumo',
            'detalhes', 'performance', 'stats', 'estatísticas', 'rounds',
            'ultimo', 'resultados'
        ]
    },
    {   'name': 'elenco', 
        'keywords': [
            'jogadores', 'players', 'lineup', 'roster', 'equipe',
            'time', 'titulares', 'reservas', 'banco', 'subs',
            'formação', 'escalação', 'membros', 'nomes', 'nick',
            'player', 'atletas', 'seleção', 'grupo', 'call', 'elenco', 'atual'
        ]
    },
    {   'name': 'assistir', 
        'keywords': [
            'assistir', 'ver', 'live', 'stream', 'twitch',
            'youtube', 'transmissão', 'aovivo', 'onde', 'link',
            'canal', 'plataforma', 'narração', 'cast', 'cobertura',
            'hl', 'tv', 'broadcast', 'watch', 'espectador', 'jogos'
        ]
    },
    {   'name': 'despedida',
        'keywords': [
            'tchau', 'adeus', 'flw', 'bye', 'vou',
            'até', 'logo', 'falou', 'partiu',
            'fui', 'xau', 'valeu', 'obrigado', 'obrigada',
            'abração', 'tmj', 'vamos', 'combina', 'depois'
        ]
    },
    {   'name': 'cumprimento',
        'keywords': [
            'oi', 'olá', 'eae', 'salve', 'fala',
            'bom', 'dia', 'tarde', 'noite', 'beleza',
            'suave', 'coé', 'opa', 'hello', 'hi',
            'tudo', 'bem', 'como', 'vai', 'firme'
        ]
    },
    {   'name': 'about',
        'keywords': [
            'redes', 'sociais', 'instagram', 'twitter', 'x',
            'tiktok', 'youtube', 'facebook', 'discord', 'site',
            'aplicativo', 'app', 'web', 'contato', 'link',
            'perfil', 'hashtag', 'seguir', 'oficial', 'info','sobre'
        ]
    },
    {   'name': 'funfact',
        'keywords': [
            'curiosidade', 'fato', 'dado', 'trivia', 'sabia',
            'interessante', 'engraçado', 'incrível', 'maneiro',
            'uau', 'surpreendente', 'revelação', 'segredo', 'info',
            'história', 'anecdota', 'conte', 'revela', 'chocante'
        ]
    },
    {   'name': 'ranking',
        'keywords': 
        [
            'posição', 'lugar', 'colocação', 'posto', 'ranking',
            'classificação', 'número', 'top', 'topzera', 'patente',
            'nível', 'categoria', 'divisão', 'chaveamento', 'seed',
            'cabeça de chave', 'tier', 'grupo', 'faixa', 'patamar',
            'brasil', 'mundo', 'mundial', 'mundialmente', 'brasileiro,'
            'local', 'nacional', 'ranqueamento', 'global'
        ]
    }
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
    """formats timestamps UNIX to format'<dia> às <horário>'"""
    timestamp = int(timestamp)
    # data-unix form hltv comes in ms
    dt_utc = datetime.fromtimestamp(timestamp / 1000 , tz=timezone.utc)

    dt_br = dt_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
    
    return dt_br.strftime("%d/%m às %Hh")

def format_unix_dates(start_unix, end_unix):
    """formats timestamps UNIX to format 'dos dias <data1> até <data2>'"""
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
