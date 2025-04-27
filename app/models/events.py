import requests
from bs4 import BeautifulSoup
from app.models.utils import *

def main():
    print(get_events())

# gets players
def get_events(url):
    """Gets the name of events in events tab in hltv

    Args:
        url (str): Recieves an hltvs url to get events tab from requested team in hltv

    Returns:
        dict: Returns a dict with 2 keys: 
            - event (str): Events name
            - date (str): Events date
    """
    soup = url_events(url, HEADERS)
    return events(soup)

def url_events(url, headers):
    """Define the url for BeautifulSoup using request

    Args:
        url (str): Build the url using the hltvs events tab
        headers (str): Headers for HTTP requests

    Returns:
        Class: BeautifulSoup Object with parsed html
    """
    url = f'{url}tab-eventBox' 
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, 'html.parser')

# search for players
def events(soup):
    """Webscrap hltvs events tab to get soon events

    Args:
        soup (Class): BeautifulSoup Object getting website data

    Returns:
        list: Return a list of events dict
    """
    events_cell = soup.find('div', class_='upcoming-events-holder')
    if not events_cell:
        return []
    
    events = []
    
    for event_rows in events_cell.find_all('div', class_='eventbox-info'):
        # get the event name
        event_name_elem = event_rows.find('div', class_='eventbox-eventname')
        event_name = event_name_elem.get_text(strip=True) if event_name_elem else None
        
        # get the event date
        date_elem = event_rows.find('div', class_='eventbox-date')
        if date_elem:
            spans = date_elem.find_all('span', {'data-unix': True})
            if len(spans) >= 2:
                try:
                    start_unix = int(spans[0]['data-unix'])
                    end_unix = int(spans[1]['data-unix'])
                    date = format_unix_dates(start_unix, end_unix)
                except (KeyError, ValueError):
                    pass
        
        if event_name and date:
            events.append({
                'event': event_name,
                'date': date
            })  
    return events

if __name__ == '__main__':
    main()