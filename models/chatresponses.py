import requests

WORDS = [
        {"name": "proximo_jogo", "keywords":["quando", "proximo", "jogo", "data", "partida"]},
        {"name": "elenco", "keywords":["quem", "joga", "elenco", "jogar"]}
]

def main():
    furia_match = get_match()

    if furia_match:
        print(f"🏆 Próximo jogo da FURIA: {furia_match['event']['name']}")
        print(f"🆚 Adversário: {', '.join([t['name'] for t in furia_match['teams'] if 'furia' not in t['name'].lower()])}")
        print(f"📅 Data prevista: {furia_match['time']}")
    else:
        print("Nenhum jogo da FURIA encontrado.")

def get_match():
    matches = match_response("quando vai ser o próximo jogo da Furia?")

    for match in matches:
        teams = match.get("teams", [])
        if any("furia" in team["name"].lower() for team in teams):
            print(match)
            return match

    return None

def match_response(message, lang="pt"):
    message = message.lower()

    for word in WORDS[lang]:
        matches = [kw for kw in word["keywords"] if kw in message] 
        print(matches)
        if len(matches) >= 2:
            response = requests.get("https://hltv-api.vercel.app/api/matches.json")

            return response.json()

       # lineup = [kw for kw in word["pt"]["elenco"]["keywords"]]
       # if len(lineup) >= 2:
       #     return requests.get("https://hltv-api.vercel.app/api/matches.json")

if __name__ == '__main__':
    main()