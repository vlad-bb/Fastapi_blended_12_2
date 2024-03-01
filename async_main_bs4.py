import json
import asyncio
import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import time

ua = UserAgent()


async def get_quotes_data(client, pages: list):
    tasks = []
    for url in pages:
        tasks.append(get_quotes_page(client, url))
    return await asyncio.gather(*tasks)


async def get_quotes_page(client, url):
    r = await client.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    authors = soup.find_all('div', attrs={'class': 'quote'})
    quotes = []
    for author in authors:
        quotes.append({
            'tags': author.find('meta', attrs={'class': 'keywords'})['content'].split(','),
            'author': author.find('small', attrs={'class': 'author'}).text,
            'quote': author.find('span', attrs={'class': 'text'}).text
        })
    return quotes


async def get_authors_data(client, authors_urls: set):
    tasks = []
    for author in authors_urls:
        tasks.append(get_author_data(client, author))
    return await asyncio.gather(*tasks)


async def get_author_data(client, author_url):
    r = await client.get(author_url)
    soup = BeautifulSoup(r.content, 'lxml')
    return {
        'fullname': soup.find('h3', attrs={'class': 'author-title'}).text,
        'born_date': soup.find('span', attrs={'class': 'author-born-date'}).text,
        'born_location': soup.find('span', attrs={'class': 'author-born-location'}).text,
        'description': soup.find('div', attrs={'class': 'author-description'}).text.strip()
    }


async def get_authors_urls(client, pages: list, base_url: str) -> set:
    tasks = []
    for url in pages:
        tasks.append(get_authors_urls_from_page(client, url, base_url))
    results = await asyncio.gather(*tasks)
    return set([url for urls in results for url in urls])


async def get_authors_urls_from_page(client, url, base_url):
    r = await client.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    authors = soup.find_all('div', attrs={'class': 'quote'})
    return [f"{base_url[:-1]}{author.find('a')['href']}/" for author in authors]


async def get_pages(client, url: str, p=None, c=1) -> list:
    if p is None:
        p = []
    new_url = f'{url}/page/{c}/'
    r = await client.get(new_url)
    soup = BeautifulSoup(r.content, 'lxml')
    p.append(new_url)
    if soup.find('li', attrs={'class': 'next'}):
        await get_pages(client, url, p, c + 1)
    return p


async def main():
    url = 'https://quotes.toscrape.com/'
    headers = {'User-Agent': ua.random}
    async with httpx.AsyncClient(headers=headers) as client:
        pages = await get_pages(client, url)
        authors_urls = await get_authors_urls(client, pages, url)
        quotes = await get_quotes_data(client, pages)
        authors = await get_authors_data(client, authors_urls)

        combined_quotes = []
        for quote in quotes:
            combined_quotes.extend(quote)

        save_data(combined_quotes, authors)


def save_data(quotes, authors):
    with open('storage/authors.json', 'w', encoding="utf-8") as file:
        json.dump(authors, file, indent=4, ensure_ascii=False)
    with open('storage/quotes.json', 'w', encoding="utf-8") as file:
        json.dump(quotes, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    start = time()
    asyncio.run(main())
    print(time() - start)
