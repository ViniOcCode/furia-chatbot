from bs4 import BeautifulSoup
from app.models.utils import *

def main():
    print(get_ranking(TEAMS['main']['url'], TEAMS['main']['name']))

def get_ranking(url, team_name):
    """Gets the position in leaderboard on HLTV

    Args:
        url (str): Receives an HLTV's URL to the leaderboard of all teams' positions
        team_name (str): Name of the team to search for in the regional ranking

    Returns:
        dict: Returns a dict with 2 keys: 
            - world (str): World ranking position 
            - regional (str): Regional ranking position
    """
    soup = url_world_ranking(url)
    return ranking(soup, team_name)

def url_world_ranking(url):
    """Defines the URL for BeautifulSoup using cloudscraper

    Args:
        url (str): Builds the URL using the HLTV's team page 

    Returns:
        BeautifulSoup: BeautifulSoup Object with parsed HTML
    """
    response = scraper.get(url).text
    return BeautifulSoup(response, 'html.parser')

def url_regional_ranking():
    """Defines the URL for BeautifulSoup using cloudscraper

    Returns:
        BeautifulSoup: BeautifulSoup Object with parsed HTML
    """
    url = f'{DOMAIN}ranking/teams/2025/april/21/country/Brazil'
    response = scraper.get(url).text
    return BeautifulSoup(response, 'html.parser')

def ranking(soup, team_name):
    """Webscrapes HLTV's ranking pages to get world and regional rankings

    Args:
        soup (BeautifulSoup): BeautifulSoup Object containing the world ranking page
        team_name (str): Name of the team to search for in the regional ranking

    Returns:
        dict: Returns a dict with position values
            - world (str): World ranking position
            - regional (str): Regional ranking position
    """
    rankings = {
        'world': None,
        'regional': None,
    }

    # Get world ranking
    world_rank = soup.select_one('div.profile-team-stat:-soup-contains("World") a')
    if world_rank:
        rankings['world'] = extract_text(world_rank) if world_rank else 'Unknown'

    # Get regional ranking
    soup = url_regional_ranking()
    ranking_cell = soup.find('div', class_='ranking')
    if ranking_cell:
        tables = ranking_cell.find_all('div', class_='ranked-team')
        for table in tables:
            ranking_header = table.find('div', class_='ranking-header')
            ranking_pos = ranking_header.find('span', class_='position') if ranking_header else None

            heading = table.find('div', class_='relative')
            team_row = heading.find('span', class_='name') if heading else None
            team = extract_text(team_row).upper() if team_row else ''
            if team == team_name.upper():
                rankings['regional'] = extract_text(ranking_pos) if ranking_pos else 'Unknown'
                break

    return rankings

if __name__ == '__main__':
    main()
