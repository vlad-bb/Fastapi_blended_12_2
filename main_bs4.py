import json
import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import time

ua = UserAgent()


def get_quotes_data(client, pages: list) -> list:
    authors_inf = []
    for url in pages:
        r = client.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        authors = soup.find_all('div', attrs={'class': 'quote'})
        for author in authors:
            authors_inf.append({
                'tags': author.find('meta', attrs={'class': 'keywords'})['content'].split(','),
                'author': author.find('small', attrs={'class': 'author'}).text,
                'quote': author.find('span', attrs={'class': 'text'}).text
            })
    return authors_inf


def get_authors_data(client, authors_urls: set) -> list:
    authors_desc = []
    for author in authors_urls:
        r = client.get(author)
        soup = BeautifulSoup(r.content, 'lxml')
        authors_desc.append({
            'fullname': soup.find('h3', attrs={'class': 'author-title'}).text,
            'born_date': soup.find('span', attrs={'class': 'author-born-date'}).text,
            'born_location': soup.find('span', attrs={'class': 'author-born-location'}).text,
            'description': soup.find('div', attrs={'class': 'author-description'}).text.strip()
        })
    return authors_desc


def get_authors_urls(client, pages: list, base_url: str) -> set:
    unique_authors = []
    for url in pages:
        r = client.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        authors = soup.find_all('div', attrs={'class': 'quote'})
        unique_authors.extend([f"{base_url[:-1]}{author.find('a')['href']}/" for author in authors])
    return set(unique_authors)


def get_pages(client, url: str, p=None, c=1) -> list:
    if p is None:
        p = []
    new_url = f'{url}/page/{c}/'
    r = client.get(new_url)
    soup = BeautifulSoup(r.content, 'lxml')
    p.append(new_url)
    if soup.find('li', attrs={'class': 'next'}):
        return get_pages(client, url, p, c + 1)
    return p


def main():
    url = 'https://quotes.toscrape.com/'
    headers = {'User-Agent': f'{ua.random}'}
    with httpx.Client(headers=headers) as client:
        pages = get_pages(client, url)
        authors_urls = get_authors_urls(client, pages, url)
        save_data(
            get_quotes_data(client, pages),
            get_authors_data(client, authors_urls)
        )


def save_data(quotes: list, authors: list):
    with open('storage/authors.json', 'w', encoding="utf-8") as file:
        json.dump(authors, file, indent=4, ensure_ascii=False)
    with open('storage/quotes.json', 'w', encoding="utf-8") as file:
        json.dump(quotes, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    start = time()
    main()
    print(time() - start)
