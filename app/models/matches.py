import requests
from bs4 import BeautifulSoup
from app.models.utils import *

def main():
    get_soon_matches(TEAMS['main']['url'])
    get_last_matches(TEAMS['female']['url'])
    
# get the matches
def get_soon_matches(url):
    """Gets the soon matches

    Args:
        url (str): Recieves an hltvs url to get matches tab from requested team in hltv

    Returns:
        dict: Returns a dict with 2 keys: 
            - event (str): Events name
            - date (str): Events date
            - enemy (str): Enemys team name
            - livestream (str): Hltvs streams
            - score (str): Matchs result
    """
    # check for not schedule going inside the main matchesbox, then searching only
    # empty-states there
    # probably a team with no recent results would broke this, but idk
    soup = url_soon_matches(url, HEADERS)
    tables = soup.find_all('table', class_='match-table')
    for table in tables:
        heading = table.find_previous('h2', class_='standard-headline')
        title = extract_text(heading).lower()
        if 'matches' in title:
            rows = table.find_all('tr')
            return matches(rows)
    return []

def get_last_matches(url):
    """Gets the last 3 matches

    Args:
        url (str): Recieves an hltv's url to get matches tab from requested team in hltv

    Returns:
        dict: Returns a dict with 2 keys: 
            - event (str): Events name
            - date (str): Events date
            - enemy (str): Enemys team name
            - livestream (str): Hltvs streams
            - score (str): Matchs result
    """
    soup = url_last_matches(url, HEADERS)
    tables = soup.find_all('table', class_='match-table')
    for table in tables:
        heading = table.find_previous('h2', class_='standard-headline')
        title = extract_text(heading).lower()
        if 'results' in title:
            rows = table.find_all('tr')
            return matches(rows)[:3]
    return []

# url functions
def url_soon_matches(url, headers):
    """Define the url for BeautifulSoup using request

    Args:
        url (str): Build the url using the hltvs matches tab
        headers (str): Headers for HTTP requests

    Returns:
        Class: BeautifulSoup Object with parsed html
    """
    url = f'{url}tab-matchesBox'
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, 'html.parser')
 

def url_last_matches(url, headers):
    """Define the url for BeautifulSoup using request

    Args:
        url (str): Build the url using the hltvs matches tab
        headers (str): Headers for HTTP requests

    Returns:
        Class: BeautifulSoup Object with parsed html
    """
    url = f'{url}tab-matchesBox'
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, 'html.parser')

# get all the data for matches
def matches(rows):
    """Webscrap hltvs matches tab to get all related data

    Args:
        soup (Class): BeautifulSoup Object getting website data

    Returns:
        list: Return a list of matches dict
    """
    matches = []
    current_event = None

    for row in rows:

        if 'event-header-cell' in row.get('class', []):
            event = row.find('a', class_='a-reset')
            if event:
                current_event = extract_text(event)
            continue

        if 'team-row' in row.get('class', []):
            match = {
                'event': current_event,
                'date': None,
                'enemy': None,
                'livestreams': None,
                'score': None,
            }

            # Get hltv streams
            livestream = row.find('a', class_='matchpage-button') or row.find('a', class_='stats-button')
            if livestream != None:
                match['livestreams'] = f'{DOMAIN}{livestream['href']}'

            # Get matches date
            date = row.find('td', class_='date-cell')
            if date:
                date_unix = date.find('span', {'data-unix': True})
                if date_unix:
                    match['date'] = date_format(date_unix['data-unix'])


            # Check for matches 
            # <a> seems to be defined matches
            # <span> seems to be for undefined matches
            team = row.find('a', class_='team-2') or row.find('span', class_='team-2')
            if team:
                match['enemy'] = team.get_text(strip=True) if 'team-2' in team.get('class', []) else 'A definir'
                print(match['enemy'])

            score_cell = row.find('div', class_='score-cell')
            if score_cell:
                score = score_cell.get_text(strip=True).split(":")
                if score[0] > score[1]:
                    match['score']= f" #GOFURIA {score[0]}x{score[1]} <a href='{DOMAIN}{team['href']}' target='_blank'>{match['enemy']}</a>"
                else:
                    match['score']= f"{score[0]}x{score[1]} <a href='{DOMAIN}{team['href']}' target='_blank'>{match['enemy']}</a>"

            # catches all matches
            if match['date'] and match['enemy']:
                matches.append(match)
    return matches
    

if __name__ == '__main__':
    main()