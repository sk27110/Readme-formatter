import json
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import markdown
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import re
import time



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


def process_item(link):
    urls = [
        f'https://raw.githubusercontent.com{link}/refs/heads/main/README.md',
        f'https://raw.githubusercontent.com{link}/refs/heads/main/readme.md',
        f'https://raw.githubusercontent.com{link}/refs/heads/master/README.md',
        f'https://raw.githubusercontent.com{link}/refs/heads/master/readme.md'
    ]
    
    response = None
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            continue

    if not response or response.status_code != 200:
        return {
            "link": link,
            "raw_text": "",
            "encoded_text": ""
        }

    try:
        markdown_text = response.text
        plain_text = remove_markdown(markdown_text)
        return {
            "link": link,
            "raw_text": plain_text,
            "encoded_text": markdown_text
        }
    except Exception as e:
        return {
            "link": link,
            "raw_text": "",
            "encoded_text": ""
        }

def save_results(data, lock, output_base):
    with lock:
        with open(output_base, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=2)


def scrape_readme_files_parallel(
        input_file='links_git.json',
        output_base='github_scrap.json',
        max_workers=32,
):
    
    lock = threading.Lock()  

    with open(input_file, 'r') as file:
        links = json.load(file)

    links = links[:10]

    result = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_item, link): link for link in links}
        for i, future in enumerate(tqdm(as_completed(futures), total=len(links))):
            item = future.result()
            if item["raw_text"]:
                result.append(item)

    if result:
        save_results(result, lock, output_base)


