from utils.scrape_topics import scrape_topics
from utils.scrape_links import scrape_repository_links
from utils.scrape_readme_parallel import scrape_readme_files_parallel


def main():
    start_page=1
    end_page=6
    topics_file='topics.json'
    base_url='https://github.com'

    scrape_topics(start_page, end_page, topics_file, base_url)

    links_file='links_git.json'
    request_delay=0.01
    number_of_page=6

    scrape_repository_links(topics_file, links_file, base_url, request_delay, number_of_page)

    input_file='links_git.json'
    data_file='github_scrap.json'
    max_workers=32

    scrape_readme_files_parallel(links_file, data_file, max_workers)


if __name__ == "__main__":
    main()