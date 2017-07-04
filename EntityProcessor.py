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
    text = ''
    for i, row in df.iterrows():
        text = text + row["articleBody"] + ' '

    entity, _ = entity_extractor(text)
    print(entity)
    entities.extend(entity)
    return entities

#######################################################
#######################################################

def match_score(base, contestant):
    """
        Takes the list of entities of the category : base
        Takes the list of entities of article: contestant
    """

    base_count = Counter(base)
    print(base_count)
    contestant_count = Counter(contestant)
    print(contestant_count)
    intersect = base_count.keys() & contestant_count.keys()
    intersect_count = {k:v for k, v in contestant_count.items() if k in intersect}
    return( sum(intersect_count.values()) / sum(contestant_count.values()) )

# base = category_processor('file:///Applications/XAMPP/xamppfiles/htdocs/NIS/AI-to-News-in-Shorts/data/categories/politics20.html')
_,base = reader_processor('data/day3.csv')
text1 = 'A YouTube video shows automaker Tesla\'s Automatic Emergency Braking (AEB) system prevent a rear-end collision. Despite the Autopilot being not engaged, the car used sensors and radar to determine an accident was imminent before sounding the alarm and applying the brakes. The driver was able to move the vehicle towards the right to avoid the collision.'
text2 = 'Honda Motor had to shut down its Sayama plant in Japan on Monday after it was found that WannaCry ransomware had hit its computer network. The plant, which produces around 1,000 vehicles each day, resumed its production on Tuesday. The WannaCry ransomware exploits a Windows vulnerability and locks up files on computers until demanded ransom is paid in bitcoins.'
#entites, total = extract_entities('data/day3.csv', cols)

entity1, _ = entity_extractor(text1)
entity2, _ = entity_extractor(text2)

print(match_score(base, entity1))
print(match_score(base, entity2))
