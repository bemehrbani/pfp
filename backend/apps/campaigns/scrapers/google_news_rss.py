import feedparser
import urllib.parse

def scrape_google_news_events():
    """
    Search Google News for emerging protests and rallies.
    Returns internally structured data.
    """
    base_url = "https://news.google.com/rss/search?q="
    queries = [
        '"anti-war" AND protest AND "this weekend"',
        '"pro-palestine" AND rally',
        '"palestine" AND protest AND "this weekend"'
    ]

    events = []
    
    for query in queries:
        encoded_query = urllib.parse.quote(query)
        feed = feedparser.parse(base_url + encoded_query)
        
        for entry in feed.entries[:5]:
            title = entry.title
            link = entry.link
            
            topic = 'other'
            if 'palestine' in title.lower():
                topic = 'palestine'
            elif 'anti-war' in title.lower() or 'peace' in title.lower():
                topic = 'anti_war'
                
            events.append({
                'title': title[:250],
                'source_url': link[:499],
                'topic': topic,
                'description': entry.description,
            })
            
    return events
