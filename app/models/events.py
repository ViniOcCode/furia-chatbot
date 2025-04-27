import requests
from bs4 import BeautifulSoup
from app.models.utils import *

def main():
    print(get_events())

# gets players
def get_events(url):
    soup = url_events(url, HEADERS)
    return events(soup)

def url_events(url, headers):
    url = f'{url}tab-eventBox' 
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, 'html.parser')

# search for players
def events(soup):
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