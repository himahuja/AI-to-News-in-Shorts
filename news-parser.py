from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import os

###################
# works on Python 3
###################

url = 'file:///Applications/XAMPP/xamppfiles/htdocs/NIS/AI-to-News-in-Shorts/data/2_inshorts.html'
page = urllib.request.urlopen(url)
content = page.read()

soup = BeautifulSoup(content, 'html.parser')
heads = soup.find_all('span', {'itemprop': 'headline'})
articles = soup.find_all('div', {'itemprop': 'articleBody'})
authors = soup.find_all('span', {'class': 'author'})
dates = soup.find_all('span', {'clas':'date'})
sources = soup.find_all('a', {'class':'source'})
images = soup.find_all('div', {'class': 'news-card-image'})
data = zip(heads, articles, authors, dates, sources, images)
stored = []
cols = ['headline', 'article', 'author', 'date', 'source', 'image']
for head, article, author, date, source, image in data:
    stored.append([head.get_text(), article.get_text(), author.get_text(), date.get_text(), source['href'], image])
df = pd.DataFrame(stored, columns = cols)
df.to_csv('data/2.csv')
