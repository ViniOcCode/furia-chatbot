import requests
from bs4 import BeautifulSoup
from utils import *

def main():
    #print(get_soon_matches(URLT, HEADERS))
    print(get_last_matches(URLT, HEADERS))

# calls the get method of the functions
def get_soon_matches(url, headers):
    url = f'{url}tab-matchesBox'
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    return soon_matches(soup) 

def get_last_matches(url, headers):
    url = f'{url}tab-matchesBox'
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    return last_matches(soup)

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
    
# get the matches
def soon_matches(soup):
    # check for not schedule going inside the main matchesbox, then searching only
    # empty-states there
    # probably a team with no recent results would broke this, but idk
    tables = soup.find_all('table', class_='match-table')
    for table in tables:
        heading = table.find_previous('h2', class_='standard-headline')
        title = heading.get_text(strip=True).lower()
 
    if 'upcoming matches' in title:
        rows = table.find_all('tr')
        return matches(rows)
    return []

def last_matches(soup):
    tables = soup.find_all('table', class_='match-table')
    for table in tables:
        heading = table.find_previous('h2', class_='standard-headline')
        title = heading.get_text(strip=True).lower()
 
    if 'results' in title:
        rows = table.find_all('tr')
        return matches(rows)[:3]
    return []

if __name__ == '__main__':
    main()