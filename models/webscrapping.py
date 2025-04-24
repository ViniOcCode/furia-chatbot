import requests
from bs4 import BeautifulSoup

URL = 'https://www.hltv.org/team/8297/furia#tab-matchesBox' 
URL_TESTE = 'https://www.hltv.org/team/9565/vitality#tab-matchesBox'
HEADERS = {'User-Agent': 'Mozzila/5.0'}

# Uses the url 
def fetch_html(url, headers):
    response = requests.get(url, headers=headers).text
    return  BeautifulSoup(response, 'html.parser')

# extensive use of get_text
def extract_text(row):
    return row.get_text(strip=True) if row else None

# get the matches
def parse_matches(soup):

    # check for not schedule
    if soup.find('div', class_='empty-state'):
        return 'As panteras não têm jogo marcado :('

    table = soup.find('table', class_='match-table')
    matches = []
    rows = table.find_all('tr')

    event = date = team = None 
    for row in rows:
        # Get event name
        event= extract_text(row.find('a', class_='a-reset')) or event


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
                'Enemy': team
            }
            matches.append(match)
            event = date = team = None 
    return matches

# return the dict to user
def find_matches(url, headers):
    soup = fetch_html(url, headers)
    return parse_matches(soup)

print(find_matches(URL_TESTE, HEADERS))
 
