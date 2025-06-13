import json
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import markdown
import time
import re


def scrape_readme_files(
        input_file='links_git.json',
        output_base='github_scrap',
        chunk_size=1000,
        request_delay=0.5,
        max_retries=3
    ):
    """
    Собирает README файлы из GitHub репозиториев и сохраняет их чанками
    
    Параметры:
    input_file (str): файл с JSON-списком ссылок на репозитории
    output_base (str): базовое имя для выходных файлов
    chunk_size (int): размер чанка для сохранения (по умолчанию 1000)
    request_timeout (int): таймаут для HTTP запросов в секундах
    request_delay (float): задержка между запросами для избежания блокировки
    max_retries (int): максимальное количество попыток для каждого запроса
    """
    
    # Загрузка списка ссылок
    try:
        with open(input_file, 'r') as file:
            links = json.load(file)
    except Exception as e:
        print(f"Ошибка загрузки файла ссылок: {e}")
        return False


    def remove_markdown(text):
        """
        Удаляет из текста все символы, которые могут интерпретироваться как Markdown разметка.
        Включает: # * _ ` ~ > - + | [ ] ! ( ) : \ " ' { } и обратные кавычки
        """
        html = markdown.markdown(text)
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a'):
            a.replace_with(a.get('href', ''))
        text = soup.get_text()
        markdown_chars = r'\#\*\_\`\~\>\-\+\|\!\[\]\:\"\'\{\}\\\‹›«»“”"'
        pattern = f'[{re.escape(markdown_chars)}]'
        return re.sub(pattern, '', text)


    def process_repository(link):
        url_variants = [
            f'https://raw.githubusercontent.com{link}/main/README.md',
            f'https://raw.githubusercontent.com{link}/main/readme.md',
            f'https://raw.githubusercontent.com{link}/master/README.md',
            f'https://raw.githubusercontent.com{link}/master/readme.md',
        ]
        
        
        for url in url_variants:
            for attempt in range(max_retries):
                try:
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        markdown_text = response.text
                        plain_text = remove_markdown(markdown_text)
                        return {
                            "link": link,
                            "raw_text": plain_text,
                            "encoded_text": markdown_text
                        }
                        
                except requests.exceptions.RequestException as e:
                    continue
                
                time.sleep(request_delay)
                break
        
        return {
            "link": link,
            "raw_text": "",
            "encoded_text": ""
        }


    result = []
    processed_count = 0
    success_count = 0
    
    progress_bar = tqdm(links, desc="Обработка репозиториев")
    
    for i, link in enumerate(progress_bar):
        item = process_repository(link)
        if item["raw_text"]:
            result.append(item)
            success_count += 1
            
        processed_count += 1
        
        if (i + 1) % chunk_size == 0:
            output_file = f"{output_base}_{i+1}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            result.clear()
            progress_bar.set_postfix(
                {"success": success_count, "total": processed_count}
            )
    
    if result:
        output_file = f"{output_base}_final_{processed_count}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\nОбработка завершена. Успешно: {success_count}/{processed_count}")

        

