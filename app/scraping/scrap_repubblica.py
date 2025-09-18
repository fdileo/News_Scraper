import requests
from bs4 import BeautifulSoup
import lxml
from pandas import DataFrame


def convert_date(date : str):
    """ 
    Converte la data del tipo 17 Settembre 2025 in 17.09.2025
    """
    
    data = date.split()
    
    mapping = {
        "Gennaio": "01",
        "Febbraio": "02",
        "Marzo": "03",
        "Aprile": "04",
        "Maggio": "05",
        "Giugno": "06",
        "Luglio": "07",
        "Agosto": "08",
        "Settembre": "09",
        "Ottobre": "10",
        "Novembre": "11",
        "Dicembre": "12"
    }
    
    data[1] = mapping[data[1].strip().capitalize()]
    
    return '.'.join(data)
    
    
def repubblica_scrap(topic : str = "cronaca"):
    
    """
    PARAMETRI IN INPUT
    - topic --> stringa che permette il web scraping degli articoli di quel topic. 
                Di default è cronaca
    """
    
    df = {'id' : [], 'topic' : [], 'day_published' : [], 'abstract' : [], 'link' : []}
    
    url = f"https://www.repubblica.it/{topic}/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return DataFrame([{"error": str(e)}])

    
    html = response.text 
    repubblica = BeautifulSoup(html, 'lxml')
    news = repubblica.find_all('div', class_ = "entry__content")

    for new in news:
        
        abstract = new.find('a').text.strip() if new.find('a') is not None else ''
        day_published = convert_date(new.find('time').text.strip()) if new.find('time') is not None else ''
        link = new.find('a').get('href')
        id = link[-10:-1]
        
        df['id'].append(id)
        df['topic'].append(topic)
        df['day_published'].append(day_published)
        df['abstract'].append(abstract)
        df['link'].append(link)
        
    return DataFrame(df)
