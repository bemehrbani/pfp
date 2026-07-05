import requests
from bs4 import BeautifulSoup

def scrape_wbw_events():
    """
    Scrape World BEYOND War's events calendar for anti-war events.
    """
    url = "https://events.worldbeyondwar.org/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    events = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        event_nodes = soup.find_all('div', class_='type-tribe_events')
        
        for node in event_nodes[:10]:
            title_tag = node.find('h3', class_='tribe-events-calendar-list__event-title')
            title = title_tag.get_text(strip=True) if title_tag else "Unknown Event"
            
            link_tag = title_tag.find('a') if title_tag else None
            link = link_tag['href'] if link_tag else ""
            
            events.append({
                'title': title[:250],
                'source_url': link[:499],
                'topic': 'anti_war',
                'description': f"Sourced from World BEYOND War.",
                'city': 'Global Web/Unknown',
            })
            
    except Exception as e:
        print(f"Error scraping WBW: {e}")
        
    return events
