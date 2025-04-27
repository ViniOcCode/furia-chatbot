import requests
from bs4 import BeautifulSoup
from app.models.utils import *

URL = f'{DOMAIN}team/8297/furia#' 
URLT = f'{DOMAIN}team/12774/flyquest#'
#URLT = f'{DOMAIN}team/10567/flyquest#'

def main():
    print(get_ranking(URLT,'FURIA'))

# gets players
def get_ranking(url, team_name):
    soup = url_world_ranking(url, HEADERS)
    return ranking(soup, team_name)

def url_world_ranking(url, headers):
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, 'html.parser')
    
def url_regional_ranking():
    url = f'{DOMAIN}ranking/teams/2025/april/21/country/Brazil'
    response = requests.get(url, headers=HEADERS).text
    return BeautifulSoup(response, 'html.parser')

# search for players
def ranking(soup, team_name):
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