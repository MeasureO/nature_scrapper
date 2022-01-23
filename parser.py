import json
import requests
from bs4 import BeautifulSoup
import string
import os

url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
max_page_number = int(input())
article_type = input()
main_dir = os.getcwd()

for page_number in range(1, max_page_number + 1):
    os.mkdir(f'Page_{page_number}')
    os.chdir(f'{main_dir}/Page_{page_number}')
    r = requests.get(f'{url}&page={page_number}')
    soup = BeautifulSoup(r.content, 'html.parser')
    saved_articles = []
    articles = soup.find_all('article')
    saved_articles = []
    for article in articles:
        if article.find('span', "c-meta__type").text == article_type:
            article_name = article.find('a', {"data-track-label": "link"}).text.strip().replace(' ', '_')
            for char in article_name:
                if char != '_' and char in string.punctuation:
                    article_name = article_name.replace(char, '')
            article_url = f"https://nature.com{article.find('a').get('href')}"
            saved_articles.append(article_name + '.txt')
            article_r = requests.get(article_url)
            article_soup = BeautifulSoup(article_r.content, 'html.parser')
            with open(article_name + '.txt', 'wb') as output:
                output.write(article_soup.find('div', attrs={"class": "c-article-body"}).text.strip().encode('utf-8'))
    os.chdir(f'{main_dir}')   
print("Saved articles:  ", saved_articles)
print("Saved all articles.")


