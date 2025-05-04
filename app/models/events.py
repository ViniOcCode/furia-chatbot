import cloudscraper
from bs4 import BeautifulSoup
from app.models.utils import *

def main():
    print(get_events("https://www.hltv.org/team/6667/furia"))

# gets events
def get_events(url):
    """Gets the name of events in events tab in hltv

    Args:
        url (str): Receives an HLTV URL to get the events tab from the requested team

    Returns:
        list: Returns a list of event dictionaries with:
            - event (str): Event name
            - date (str): Event date
    """
    soup = url_events(url)
    return events(soup)

def url_events(url):
    """Defines the URL for BeautifulSoup using cloudscraper

    Args:
        url (str): Builds the URL using HLTV's events tab

    Returns:
        BeautifulSoup: BeautifulSoup object with parsed HTML
    """
    url = f'{url}#tab-eventsBox'
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url).text
    return BeautifulSoup(response, 'html.parser')

# search for events
def events(soup):
    """Webscrapes HLTV's events tab to get upcoming events

    Args:
        soup (BeautifulSoup): BeautifulSoup object with website data

    Returns:
        list: Returns a list of event dictionaries with:
            - event (str): Event name
            - date (str): Event date
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
        date = None
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
