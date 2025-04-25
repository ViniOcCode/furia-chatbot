import requests
from bs4 import BeautifulSoup
from utils import *

def main():
    print(get_last_matches())
    print(get_soon_matches())
    
# get the matches
def get_soon_matches():
    # check for not schedule going inside the main matchesbox, then searching only
    # empty-states there
    # probably a team with no recent results would broke this, but idk
    soup = url_soon_matches(URLT, HEADERS)
    tables = soup.find_all('table', class_='match-table')
    for table in tables:
        heading = table.find_previous('h2', class_='standard-headline')
        title = heading.get_text(strip=True).lower()
        if 'matches' in title:
            rows = table.find_all('tr')
            return matches(rows)
    return []

def get_last_matches():
    soup = url_last_matches(URLT, HEADERS)
    tables = soup.find_all('table', class_='match-table')
    for table in tables:
        heading = table.find_previous('h2', class_='standard-headline')
        title = heading.get_text(strip=True).lower()
        if 'results' in title:
            rows = table.find_all('tr')
            return matches(rows)[:3]
    return []

# url functions
def url_soon_matches(url, headers):
    url = f'{url}tab-matchesBox'
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, 'html.parser')
 

def url_last_matches(url, headers):
    url = f'{url}tab-matchesBox'
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, 'html.parser')

def matches(rows):
    matches = []
    event = date = team = watch = score = None 
    for row in rows:
        # Get event name
        livestream = row.find('a', class_='matchpage-button') or watch
        if livestream != None:
            watch = livestream['href']

        event = extract_text(row.find('a', class_='a-reset')) or event

        # Get matches date
        date = row.find('td', class_='date-cell')
        if date != None:
            date_unix = date.find('span')
            date = date_format(date_unix['data-unix'])
            

        # Check for TBD matches
        TBD = row.find('span', class_='team-2')
        if TBD != None:
            team = 'A definir' # this span is whenever got a TBD match
        else:
            team = extract_text(row.find('a', class_='team-2')) or team 
            # this a is when they have a defined team to play

        result = row.find('div', class_='score-cell')
        score_cell = result.get_text(strip=True) if result else None
        if score_cell != None:
            score = score_cell.split(":")
            score = f'{team} {score[0]} x {score[1]}'
        # catches all matches
        if all([event,date, team]):
            match = {
                'event': event,
                'date': date,
                'enemy': team,
                'livestreams': watch,
                'score': score
            }
            matches.append(match)
            event = date = team = watch = score = None 
    return matches
    

if __name__ == '__main__':
    main()