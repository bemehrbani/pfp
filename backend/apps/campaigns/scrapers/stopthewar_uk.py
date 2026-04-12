import requests
from bs4 import BeautifulSoup

def scrape_stopthewar_events():
    """
    Scrape Stop the War Coalition Events.
    """
    url = "https://www.stopwar.org.uk/events/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    events = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        event_nodes = soup.find_all('a', class_='event__container')
        
        for node in event_nodes[:15]:
            # title is in div.event__title
            title_div = node.find('div', class_='event__title')
            title = title_div.get_text(strip=True) if title_div else "Unknown STW Event"
            
            link = node.get('href', '')
            
            # city is in div.event__city
            city_div = node.find('div', class_='event__city')
            city = city_div.get_text(strip=True) if city_div else "UK / Network"
            
            topic = 'anti_war'
            if 'palestine' in title.lower() or 'gaza' in title.lower():
                topic = 'palestine'
            
            events.append({
                'title': title[:250],
                'source_url': link[:499],
                'topic': topic,
                'description': "Sourced from Stop the War Coalition UK",
                'city': city[:100],
            })
            
    except Exception as e:
        print(f"Error scraping STW: {e}")
        
    return events

if __name__ == "__main__":
    for p in scrape_stopthewar_events()[:3]:
        print(p)
