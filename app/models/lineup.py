import cloudscraper
from bs4 import BeautifulSoup
from app.models.utils import *

def main():
    print(get_players("https://www.hltv.org/team/6667/9z"))

def get_players(url):
    """Gets the requested team's lineup.

    Args:
        url (str): Receives an HLTV URL to the team's lineup.

    Returns:
        dict: Returns a dictionary with two keys:
            - players (list): List of player names.
            - coach (str): Team's coach name.
    """
    soup = url_players(url)
    return players(soup)

def url_players(url):
    """Defines the URL for BeautifulSoup using cloudscraper.

    Args:
        url (str): Builds the URL using the HLTV roster box.

    Returns:
        BeautifulSoup: BeautifulSoup object with parsed HTML.
    """
    full_url = f'{url}#tab-rosterBox'
    scraper = cloudscraper.create_scraper()
    response = scraper.get(full_url).text
    return BeautifulSoup(response, 'html.parser')

def players(soup):
    """Webscrapes HLTV's roster box tab to retrieve the entire lineup if possible.

    Args:
        soup (BeautifulSoup): BeautifulSoup object containing website data.

    Returns:
        dict: Returns a dictionary with players list and coach name:
            - players (list): All player names.
            - coach (str): Coach's name.
    """
    lineup = {
        'players': [],
        'coach': None
    }

    # Get coach
    coach_row = soup.find('table', class_='coach-table')
    if coach_row is not None:
        coach = extract_text(coach_row.find('div', class_='text-ellipsis'))
        if coach:
            lineup['coach'] = coach
    else:
        lineup['coach'] = 'Desconhecido'

    table = soup.find('table', class_='players-table')
    if table:
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
