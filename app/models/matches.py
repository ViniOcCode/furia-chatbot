from bs4 import BeautifulSoup
from app.models.utils import *  

def main():
    print(get_last_matches(TEAMS['main']['url']))
    print(get_soon_matches(TEAMS['main']['url']))


def get_soon_matches(url):
    """
    Get upcoming matches for a team from HLTV.

    Args:
        url (str): The base URL of the team's HLTV page.

    Returns:
        list: A list of match dictionaries with details about upcoming matches.
    """
    soup = url_matches_soup(url)
    tables = soup.find_all('table', class_='match-table')
    for table in tables:
        heading = table.find_previous('h2', class_='standard-headline')
        title = extract_text(heading).lower()
        if 'matches' in title:
            return matches(table.find_all('tr'))
    return []


def get_last_matches(url):
    """
    Get the last 3 matches for a team from HLTV.

    Args:
        url (str): The base URL of the team's HLTV page.

    Returns:
        list: A list of dictionaries with details of the last three matches.
    """
    soup = url_matches_soup(url)
    tables = soup.find_all('table', class_='match-table')
    for table in tables:
        heading = table.find_previous('h2', class_='standard-headline')
        title = extract_text(heading).lower()
        if 'results' in title:
            return matches(table.find_all('tr'))[:3]
    return []


def url_matches_soup(base_url):
    """
    Fetch and parse the HLTV matches box using cloudscraper.

    Args:
        base_url (str): The base URL of the team's HLTV page.

    Returns:
        BeautifulSoup: Parsed HTML content of the matches box.
    
    Raises:
        RuntimeError: If the HTTP request to HLTV fails.
    """
    full_url = f"{base_url}tab-matchesBox"
    # Use cloudscraper to bypass Cloudflare IUAM
    response = scraper.get(full_url, headers=HEADERS)
    if response.status_code != 200:
        raise RuntimeError(f"HLTV request failed: {response.status_code}")
    html = response.text
    return BeautifulSoup(html, 'html.parser')


def matches(rows):
    """
    Parse match rows into structured dictionaries.

    Args:
        rows (list): A list of BeautifulSoup row elements representing matches.

    Returns:
        list: A list of dictionaries containing event, date, enemy, livestreams, and score.
    """
    results = []
    current_event = None
    for row in rows:
        cls = row.get('class', [])
        if 'event-header-cell' in cls:
            evt = row.find('a', class_='a-reset')
            if evt:
                current_event = extract_text(evt)
            continue
        if 'team-row' in cls:
            match = {'event': current_event, 'date': None, 'enemy': None, 'livestreams': None, 'score': None}
            # livestream
            live = row.find('a', class_='matchpage-button') or row.find('a', class_='stats-button')
            if live:
                match['livestreams'] = f"{DOMAIN}{live['href']}"
            # date
            date_cell = row.find('td', class_='date-cell')
            if date_cell:
                span = date_cell.find('span', {'data-unix': True})
                if span:
                    match['date'] = date_format(span['data-unix'])
            # enemy
            team2 = row.find('a', class_='team-2') or row.find('span', class_='team-2')
            if team2:
                match['enemy'] = team2.get_text(strip=True)
            # score
            score_div = row.find('div', class_='score-cell')
            if score_div:
                score_text = score_div.get_text(strip=True)
                if ':' in score_text:
                    s0, s1 = score_text.split(':')
                    try:
                        s0_int = int(s0)
                        s1_int = int(s1)
                        href = team2['href'] if team2 and team2.has_attr('href') else ''
                        if s0_int > s1_int:
                            match['score'] = f"#GOFURIA {s0}x{s1} <a href='{DOMAIN}{href}' target='_blank'>{match['enemy']}</a>"
                        else:
                            match['score'] = f"{s0}x{s1} <a href='{DOMAIN}{href}' target='_blank'>{match['enemy']}</a>"
                    except ValueError:
                        match['score'] = score_text  # ou outra lógica de tratamento
                else:
                    match['score'] = score_text  # ou outra lógica de tratamento

            if match['date'] and match['enemy']:
                results.append(match)
    return results


if __name__ == '__main__':
    main()
