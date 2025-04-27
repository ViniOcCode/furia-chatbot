import requests
from bs4 import BeautifulSoup
from app.models.utils import *

def main():
    print(get_ranking(TEAMS['main']['url'], TEAMS['main']['name']))

# gets players
def get_ranking(url, team_name):
    """Gets the position in leaderboard on hltv

    Args:
        url (str): Recieves an hltv's url to leaderboard of all teams positions

    Returns:
        dict: Returns a dict with 2 keys: 
            - world (str): World ranking position 
            - regional (str): Regional ranking position
    """
    soup = url_world_ranking(url, HEADERS)
    return ranking(soup, team_name)

def url_world_ranking(url, headers):
    """Define the url for BeautifulSoup using request

    Args:
        url (str): Build the url using the hltv's team page 
        headers (str): Headers for HTTP requests

    Returns:
        Class: BeautifulSoup Object with parsed html
    """
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, 'html.parser')
    
def url_regional_ranking():
    """Define the url for BeautifulSoup using request

    Args:
        url (str): Build the url using the hltv's leaderboard page 
        headers (str): Headers for HTTP requests

    Returns:
        Class: BeautifulSoup Object with parsed html
    """
    url = f'{DOMAIN}ranking/teams/2025/april/21/country/Brazil'
    response = requests.get(url, headers=HEADERS).text
    return BeautifulSoup(response, 'html.parser')

# search for players
def ranking(soup, team_name):
    """Webscrap hltv's events tab to get soon events

    Args:
        soup (Class): BeautifulSoup Object getting website data

    Returns:
        dict: Return a dict with position values
    """
    rankings = {
          'world': None,
          'regional': None,
    }
    #:- selects the fist div that haves world in it, this is beautifulsoup feature
    # when find it, selects a section
    world_rank = soup.select_one('div.profile-team-stat:-soup-contains("World") a')
    if world_rank:
        rankings['world'] = extract_text(world_rank) if world_rank else 'Desconhecido'

        
    soup = url_regional_ranking()
    ranking_cell = soup.find('div', class_='ranking')
    tables = ranking_cell.find_all('div', class_='ranked-team')
    for table in tables:
        ranking_header = table.find('div', class_='ranking-header')
        ranking = ranking_header.find('span', class_='position')

        heading = table.find('div', class_='relative')
        team_row = heading.find('span', class_='name')
        team = extract_text(team_row).upper()
        if team == team_name.upper():
            rankings['regional'] = extract_text(ranking) if ranking else 'Desconhecido'

    return rankings

if __name__ == '__main__':
    main()