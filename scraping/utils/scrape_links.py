import json
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import time

def scrape_repository_links(
        topics_file='topics.json',
        output_file='links_git.json',
        base_url='https://github.com',
        request_delay=0.01,
        number_of_page=6
    ):
    """
    Собирает ссылки на репозитории из GitHub-топиков и сохраняет в JSON-файл
    
    Параметры:
    topics_file (str): файл с JSON-списком топиков
    output_file (str): выходной файл для ссылок
    start_page (int): начальная страница пагинации (по умолчанию 1)
    end_page (int): конечная страница пагинации (по умолчанию 6)
    base_url (str): базовый URL GitHub
    request_delay (float): задержка между запросами в секундах
    num_page (int): число страниц для каждого топика, с которых берутся ссылки на репозитории
    """
    try:
        with open(topics_file, 'r') as file:
            topics = json.load(file)
    except Exception as e:
        print(f"Ошибка загрузки файла топиков: {e}")
        return False


    links_to_readme = []


    for topic in tqdm(topics, desc="Обработка топиков"):
        for page_num in range(number_of_page):
            url = f'{base_url}{topic}?page={page_num}'
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                repo_links = soup.find_all('a', class_='Link text-bold wb-break-word')
                
                for a_tag in repo_links:
                    if 'href' in a_tag.attrs:
                        links_to_readme.append(a_tag['href'])
                
                time.sleep(request_delay)
            
            except requests.exceptions.RequestException as e:
                print(f"\nОшибка при запросе {url}: {e}")
                continue
    

    with open(output_file, 'w') as file:
        json.dump(links_to_readme, file)
    
    print(f"\nУспешно собрано {len(links_to_readme)} ссылок. Результаты сохранены в {output_file}")
    return True
    