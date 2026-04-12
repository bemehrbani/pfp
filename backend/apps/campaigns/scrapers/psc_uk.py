import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from datetime import datetime

def scrape_psc_events():
    """
    Scrape Palestine Solidarity Campaign UK Events.
    Returns structurally identical dictionary as other scrapers.
    """
    url = "https://palestinecampaign.org/events/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    events = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        event_nodes = soup.find_all('div', class_='em-event')
        
        print(f"Found {len(event_nodes)} event nodes")
        
        for node in event_nodes[:15]:
            title_tag = node.find('a', class_='em-item-title') # wait maybe the class is not exactly this?
            # actually looking at the html: <h3 class="em-item-title"><a href="...">...</a></h3>
            title_tag = node.find('h3', class_='em-item-title')
            if title_tag:
                 title_tag = title_tag.find('a')

            if not title_tag:
                print("No title tag found")
                continue
            
            title = title_tag.get_text(strip=True)
            link = title_tag.get('href', '')
            
            # Extract date if possible (PSC format varies, usually in a span)
            # Usually .em-item-meta contains the location and date
            meta_div = node.find('div', class_='em-item-meta')
            city = ""
            desc = "Sourced from Palestine Solidarity Campaign"
            
            if meta_div:
                loc_icon = meta_div.find('span', class_='em-icon-location')
                if loc_icon and loc_icon.parent:
                    city = loc_icon.parent.get_text(strip=True)
            
            # Map standard fields
            events.append({
                'title': title[:250],
                'source_url': link[:499],
                'topic': 'palestine',
                'description': desc,
                'city': city[:100] if city else "UK / Various",
            })
            
    except Exception as e:
        print(f"Error scraping PSC: {e}")
        
    return events

# Local testing block
if __name__ == "__main__":
    events = scrape_psc_events()
    print(events[:3])
