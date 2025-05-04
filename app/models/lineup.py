import requests
from bs4 import BeautifulSoup
from app.models.utils import *

def main():
    print(get_players())

# gets players
def get_players(url):
    """Gets the requested teams lineup

    Args:
        url (str): Recieves an hltvs url to teams lineup

    Returns:
        dict: Returns a dict with 2 keys: 
            - players (list): Players name
            - coach (str): Teams coach
    """
    soup = url_players(url, HEADERS)
    return players(soup)

def url_players(url, headers):
    """Define the url for BeautifulSoup using request

    Args:
        url (str): Build the url using the hltvs roster box
        headers (str): Headers for HTTP requests

    Returns:
        Class: BeautifulSoup Object with parsed html
    """
    url = f'{url}tab-rosterBox' 
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, 'html.parser')

# search for players
def players(soup):
    """Webscrap hltvs roster box tab to entire lineup if possible 

    Args:
        soup (Class): BeautifulSoup Object getting website data

    Returns:
        dict: Return a dict with players list and coach name 
            - players (list): All player's name
            - coach (str): Coach's name
    """
    lineup = {
        'players': [],
        'coach': None
    }

    # Get coach
    coach_row = soup.find('table', class_='coach-table')
    if coach_row != None:
        coach = extract_text(coach_row.find('div', class_='text-ellipsis'))
        if coach:
            lineup['coach'] = coach 
    else:
        lineup['coach'] = 'Desconhecido'

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