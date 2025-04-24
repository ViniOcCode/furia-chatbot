import requests
from bs4 import BeautifulSoup
from utils import *

def main():
    print(get_players(URLT, HEADERS))

# gets players
def get_players(url, headers):
    url = f'{url}tab-rosterBox' 
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    return players(soup) 

# search for players
def players(soup):
    elenco = []

    # Get coach
    coach_row = soup.find('table', class_='coach-table').find('div', class_='text-ellipsis')
    coach = extract_text(coach_row)
    player = {
        'coach': coach
    }
    elenco.append(player)

    table = soup.find('table', class_='players-table')
    rows = table.find_all('tr')

    for row in rows:
        
        players = extract_text(row.find('div', class_='text-ellipsis'))
        if row.find('div', class_='player-benched'):
            players = f'{players} - (Reserva)'

        player = {
            'player': players
        }
        if players != None:
            elenco.append(player)
    
    return elenco

if __name__ == '__main__':
    main()