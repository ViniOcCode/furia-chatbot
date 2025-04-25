import requests
from bs4 import BeautifulSoup
from utils import *

def main():
    print(get_players())

# gets players
def get_players():
    soup = url_players(URLT, HEADERS)
    return players(soup)

def url_players(url, headers):
    url = f'{url}tab-rosterBox' 
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, 'html.parser')

# search for players
def players(soup):
    lineup = {
        'players': [],
        'coach': None
    }

    # Get coach
    coach_row = soup.find('table', class_='coach-table').find('div', class_='text-ellipsis')
    coach = extract_text(coach_row)
    if coach:
        lineup['coach'] = coach

    table = soup.find('table', class_='players-table')
    rows = table.find_all('tr')

    for row in rows:
        
        player = extract_text(row.find('div', class_='text-ellipsis'))
        if player:
            if row.find('div', class_='player-benched'):
                player = f'{player} - (Reserva)'
            lineup['players'].append(player)

    
    return lineup

if __name__ == '__main__':
    main()