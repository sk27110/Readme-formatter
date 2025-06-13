# Сбор данных

### Структура директории

scraping/  

├── utils/  
│   ├── __init__.py  
│   ├── scrape_topics.py  
│   ├── scrape_links.py  
│   ├── scrape_readme.py  
│   ├── scrape_readme_parallel.py  
├── main.py

### О сборе данных

Данные будем скрапить с сайта Github из открытых репозиториев
На странице https://github.com/topics можно найти топики по темам, в котрых собраны ссылки на открытые репозитории. 

### Описание функций

- __scrape_topics.py__ - файл с функцией для сбора ссылок на топики, которые есть на странице https://github.com/topics. Сохраняет ссылки на топики в выходной файл topics.json

- __scrape_links.py__ - файл с функцией для сбора ссылок на репозитории. По ссылкам из topics.json скрапит ссылки на репозитории __GitHub__ и сохраняет в links_git.json.

- __scrape_readme.py__ - файл с функцией для скрапа файлов README. По ссылкам из links_git.json скрапит README файлы репозиториев, удаляет из них код Markdown и записывает в файл github_scrap.json словари вида
```     
{"raw_text": ..., "formatted_text": ...}
```

- __scrape_readme_parallel.py__ - аналогичная scrape_readme.py функция, но с возможностью распаралелить запросы к __GitHub__.

- __main.py__ - основной файл, в котором реализовано последовательное выполнение выше указанных функций. По умолчанию используется паралельное исполнение сбора readme.

### Скрапинг

Установка зависимостей:
```
pip install requirements.txt
```

Для запуска скрапинга из директории /scraping исполним скрипт:
```
python main.py
```

Получаем три файла:
- topics.json
- links_git.json
- github_scrap.json

где github_scrap.json это данные для обучения.

В датасете получается около 10к пар сырых и форматированных текстов (при желании можно увеличить number_of_page в main.py до 11, тогда пар получится примерно в 2 раза больше).

### Ссылки на данные
- [topics.json](https://drive.google.com/file/d/19nKqX_EGkVdEXjMhC9duVGRck9YOGt75/view?usp=sharing)
- [links_git.json](https://drive.google.com/file/d/15pSRLdT19T8nLqmBMGFDN7M5LG42ehmq/view?usp=sharing)
- [github_scrap.json](https://drive.google.com/file/d/1qmDE3W-33pZ9-AhZtcSyb9LlDsITQW2E/view?usp=sharing)
