import requests
from bs4 import BeautifulSoup

DOMAIN = 'https://www.hltv.org/'
HEADERS = {'User-Agent': 'Mozzila/5.0'}

def main():
    print(get_soon_matches(DOMAIN, HEADERS))
    print(get_players(DOMAIN, HEADERS))

# Uses the url 
def get_soon_matches(domain, headers):
    url = f'{domain}team/8297/furia#tab-matchesBox' 
    urlt = f'{domain}team/12774/liquid#tab-matchesBox'
    response = requests.get(urlt, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    return soon_matches(soup) 

def get_players(domain, headers):
    url = f'{domain}team/8297/furia#tab-rosterBox' 
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    return players(soup) 


# get the matches
def soon_matches(soup):
    # check for not schedule going inside the main matchesbox, then searching only
    # empty-states there
    # probably a team with no recent results would broke this, but idk
    if soup.find('div', id='matchesBox').find('div', class_='empty-state'):
        return 'As panteras não têm jogo marcado :('

    table = soup.find('table', class_='match-table')
    matches = []
    rows = table.find_all('tr')

    event = date = team = None 
    for row in rows:
        # Get event name
        livestream = row.find('a', class_='matchpage-button')
        if livestream != None:
            watch = livestream['href']

        event = extract_text(row.find('a', class_='a-reset')) or event

        # Get matches date
        date = extract_text(row.find('td', class_='date-cell')) or event

        # Check for TBD matches
        TBD = row.find('span', class_='team-2')
        if TBD != None:
            team = 'A definir' # this span is whenever got a TBD match
        else:
            team = extract_text(row.find('a', class_='team-2')) or team 
            # this a is when they have a defined team to play

        # catches all matches
        if all([event,date, team]):
            match = {
                'Event': event,
                'Date': date,
                'Enemy': team,
                'livestreams': watch
            }
            matches.append(match)
            event = date = team = None 
    return matches

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

# extensive use of get_text
def extract_text(row):
    return row.get_text(strip=True) if row else None

if __name__ == '__main__':
    main()