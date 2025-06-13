import requests
from bs4 import BeautifulSoup
from tqdm import tqdm 
import json


def scrape_topics(
        start_page=1, 
        end_page=6, 
        output_file='topics.json',
        base_url='https://github.com'
    ):
    """
    Сохраняет список GitHub-топиков в JSON-файл
    
    Параметры:
    start_page (int): начальная страница
    end_page (int): конечная страница
    output_file (str): имя выходного файла
    base_url (str): базовый URL GitHub
    """
    topics = []
    
    for i in tqdm(range(start_page, end_page + 1), desc="Сбор топиков"):
        url = f'{base_url}/topics?page={i}'
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"\nОшибка при загрузке страницы {i}: {e}")
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for a_tag in soup.find_all('a', class_='no-underline flex-1 d-flex flex-column'):
            if 'href' in a_tag.attrs:
                topics.append(a_tag['href'])
    

    with open(output_file, 'w') as file:
        json.dump(topics, file)
        
    print(f"Успешно. Результаты сохранены в {output_file}")




    