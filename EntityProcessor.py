# BOILERPIPE extracts the main Article out of a source page
from boilerpipe.extract import Extractor
# TO MAKE A DATAFRAME
import pandas as pd
# TO GET THE ENTITIES FROM THE TEXT
from dandelion import DataTXT
# TO COUNT THE OCCURENCES in WEIGHTED TOTAL
from collections import Counter
#To save the list of the elments
import pickle as pk
#To parse the news articles
import Newsparser
#To work in graphs
import Grapher
#################################################
#Personal API for using Dandelion-EU
datatxt = DataTXT(app_id='7a313081ecd24154bb78b048090cf45e', app_key='7a313081ecd24154bb78b048090cf45e')
#################################################
cols = ['iid','headline', 'articleBody', 'author', 'date', 'source', 'image', 'counter', 'bookmark', 'readmore']
##################################################
##################################################

def entity_extractor(text, weight = 1):
    """Using Dandelion-API to extract entities from text"""
    response = datatxt.nex(text)
    entity = []
    w_entity = []
    for annotation in response.annotations:
        entity.append(annotation["spot"])
        w_entity = entity * weight
    return entity, w_entity

def reader_processor(csv, cols = cols):
    """
    Takes input of a csv of the cross between
    stats.csv and articles.csv as 'day<date of experiment>.csv'

    entities: Returns the entity list of individual article.
    total: Returns the total of all the entities identified.

    """
    df = pd.read_csv(csv, names = cols)
    total = []
    entites = []
    for i, row in df.iterrows():
        #MINE ONLY SPECIFIC ARTICLES [>=6 (12 seconds)]
        if(row["counter"]>=6):
        ## FORM A NEW TEXT
            text = row["articleBody"] + " " + row["headline"]
            #### if readmore has been clicked
            if(row["readmore"] == 1):
                try:
                    #use of boilerpipe
                    external = Extractor(extractor='ArticleExtractor', url=row["source"]).getText()
                except:
                    external = ''
                text = text + " " + external
            entity, w_entity = entity_extractor(text, row["counter"])
            entites.append(entity)
            total.extend(w_entity)

    return entites, total

######################################################
######################################################

def category_processor(url):
    df = Newsparser.newsparser(url)
    entities = []
    document = []
    for i, row in df.iterrows():
        text = row["articleBody"] + row["headline"]
        entity, _ = entity_extractor(text)
        entities.append(entity)
    return entities

#######################################################
#######################################################

def match_score(G, contestant):
    """
        Takes the list of list entities of the category : base
        Takes the list of entities of article: contestant
    """
    score = 0
    for entity in contestant:
        try:
            neighbors = G[entity].values()
            score += G.node[entity]['relevance']

            """Since the graph is connected,
            There will always be neighbors,
            So the try statement is omitted."""

            for neighbor in neighbors:
                for k, v in neighbor:
                    score += v
        except:
            continue

    return score;

def category_finder(categories, url):
    clouds = {}
    for k, v in categories.items():
        clouds[k] = pk.load(open(v, 'rb'))

    articles = Newsparser.newsparser2(url)
    count = 0
    for article in articles:
        count = count + 1
        entity, _ = entity_extractor(article)
        max_score = 0
        old_max_score = 0
        label = None
        scores = {}
        for k, v in clouds.items():
            scores[k] = match_score(v, entity)
        print (article, count, scores)

def interest_finder(categories, stats):
    prin("Say Hello!")




#_,base = reader_processor('data/day3.csv')
# base = pk.load(open("data/categories/technology.p", "rb"))
# text1 = 'Indian women\'s cricket team spinner Ekta Bisht\'s father, Kundan Singh Bisht, a former Havaldar in the Indian Army, ran a tea stall to support her dream of playing cricket for India. Kundan had opened the tea stall in their hometown of Almora, with the income from the tea stall helping the family bear the expenses of her training.'
# text2 = 'Chinese officials on Thursday said that the atmosphere is not right for a bilateral meeting between Indian Prime Minister Narendra Modi and Chinese President Xi Jinping at the G20 summit in Germany. The armies of India and China are currently involved in a standoff on the India-China-Bhutan tri-junction and both governments have exchanged warnings over the situation.'
# text3 = 'What is the technology over which Qualcomm has sued Apple? Chipmaker Qualcomm on Friday announced it has filed a complaint with US International Trade Commission, accusing Apple of infringing six patents. Qualcomm said the technologies covered by the patents are central to the iPhone\'s performance. They cover aspects of extending a device\'s battery life in situations like transmitting video files over cellular network and playing games with rich graphics.'
#entites, total = extract_entities('data/day3.csv', cols)
#
#entity1, _ = entity_extractor(text1)
#entity2, _ = entity_extractor(text2)
# base = category_processor('file:///Applications/XAMPP/xamppfiles/htdocs/NIS/AI-to-News-in-Shorts/data/categories/world.html')
# pk.dump(base, open('data/categories/world.p', 'wb'))
# G = Grapher.category_grapher('data/categories/world.p', 'data/categories/worldG.p')
#print(match_score(G, entity1))
#print(match_score(G, entity2))
categories = {'sports': 'data/categories/sportsG.p', \
              'politics': 'data/categories/politicsG.p', \
              'entertainment': 'data/categories/entertainmentG.p',\
              'national': 'data/categories/nationalG.p',\
              'world': 'data/categories/worldG.p'
             }
url = 'file:///Applications/XAMPP/xamppfiles/htdocs/NIS/AI-to-News-in-Shorts/data/sample.html'
category_finder(categories, url)
