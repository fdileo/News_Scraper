import requests
from bs4 import BeautifulSoup
import lxml
from pandas import DataFrame

df = {'id' : [], 'topic' : [], 'day_published' : [], 'abstract' : [], 'link' : []}

def euronews_scrap():
    
    url = "https://it.euronews.com/ultime-notizie"
    response = requests.get(url = url)

    if response.status_code == 200:
        
        html = response.text
        euronews = BeautifulSoup(html, "lxml")
        news = euronews.find_all('li', class_ = "tc-justin-timeline__item")
        global df
        
        for  new in news:
            
            try:
                id = new['id'].split('-')[-1]
                topic = new.find('a', class_ = "tc-justin-timeline__article__metas").text.strip()
                day_published = new.find('span', class_ = "tc-justin-timeline__article__day").text.strip()
                abstract = new.find('h2', class_ = "tc-justin-timeline__article__title").text.strip()
                link = new.find('a', class_ = "tc-justin-timeline__article__link", href = True)["href"]
        
                df['id'].append(id)
                df['topic'].append(topic)
                df['day_published'].append(day_published)
                df['abstract'].append(abstract)
                df['link'].append(link)
            except:
                continue
            
                
        return DataFrame(df)
        
    else:
        
        return f"{"error": response.status_code}"

df = euronews_scrap()
print(df['day_published'])