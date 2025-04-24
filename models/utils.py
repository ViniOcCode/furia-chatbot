from datetime import datetime, timezone
from zoneinfo import ZoneInfo

DOMAIN = 'https://www.hltv.org/'
URL = f'{DOMAIN}team/8297/furia#' 
URLT = f'{DOMAIN}team/12774/flyquest#'
HEADERS = {'User-Agent': 'Mozzila/5.0'}

# extensive use of get_text
def extract_text(row):
    return row.get_text(strip=True) if row else None

# formatting date
def date_format(timestamp):
    timestamp_ms = int(timestamp)
    timestamp = timestamp_ms // 1000
    dt_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)

    dt_br = dt_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
    
    return dt_br.strftime("%d/%m às %Hh")
