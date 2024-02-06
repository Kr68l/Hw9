import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes(url):
    quotes = []
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for quote in soup.select('div.quote'):
            text = quote.select_one('span.text').get_text(strip=True)
            author = quote.select_one('small.author').get_text(strip=True)
            quotes.append({'text': text, 'author': author})

        next_page = soup.select_one('li.next > a')
        url = next_page['href'] if next_page else None

    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

def scrape_authors(url):
    authors = {}
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for author in soup.select('div.author'):
            name = author.select_one('h3.author-title').get_text(strip=True)
            born_date = author.select_one('span.author-born-date').get_text(strip=True)
            born_location = author.select_one('span.author-born-location').get_text(strip=True)
            authors[name] = {'born_date': born_date, 'born_location': born_location}

        next_page = soup.select_one('li.next > a')
        url = next_page['href'] if next_page else None

    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors, f, ensure_ascii=False, indent=2)

quotes_url = 'http://quotes.toscrape.com/page/1/'
authors_url = 'http://quotes.toscrape.com/authors/page/1/'

scrape_quotes(quotes_url)
scrape_authors(authors_url)
