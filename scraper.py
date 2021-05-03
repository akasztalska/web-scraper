import requests
import string
import os


from bs4 import BeautifulSoup


def get_articles(page_number):
    url = f'https://www.nature.com/nature/articles?page={page_number}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all('article')
    return articles



def get_article_title(article):
    title = article.find('a', {'data-track-action': 'view article'}).text
    table = str.maketrans(string.punctuation, len(string.punctuation) * ' ')
    edited_title = title.translate(table).replace("  ", " ").strip().replace(" ", "_")
    return edited_title


def get_article_text(article):
    article_url = f'https://www.nature.com' + article.find('a', {'data-track-action':'view article'}).get('href')
    article_r = requests.get(article_url)
    article_soup = BeautifulSoup(article_r.content, "html.parser")
    if article_soup.find('div', {'class': 'article-item__body'}) is None:
        text = article_soup.find('div', {'class': 'article__body'}).text
    else:
        text = article_soup.find('div', {'class': 'article-item__body'}).text
    return text


def scraper(pages, type_of_article):
    for page in range(1, pages + 1):
        articles = get_articles(page)
        dir_name = f'Page_{page}'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        project_directory = os.getcwd()
        os.chdir(dir_name)
        for article in articles:
            if article.find('span', {'data-test': 'article.type'}).find('span').text == type_of_article:
                title = get_article_title(article)
                text = get_article_text(article)
                with open(f'{title}.txt', 'w', encoding='utf-8') as f:
                    f.write(text)
        os.chdir(project_directory)

def check_url(pages):
    url = f'https://www.nature.com/nature/articles?page={pages}'
    r = requests.get(url)
    if r.status_code == 200:
        return True
    return False

def main():
    pages = int(input("How many pages you want to scrap? \n"))
    if check_url(pages):
        article_type = input("What type of articles are you looking for")
        scraper(pages, article_type)
    else:
        print("It seems there aren't that many pages!")


