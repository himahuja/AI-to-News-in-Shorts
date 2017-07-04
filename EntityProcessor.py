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
from Newsparser import newsparser
#################################################
#Personal API for using Dandelion-EU
datatxt = DataTXT(app_id='7a313081ecd24154bb78b048090cf45e', app_key='7a313081ecd24154bb78b048090cf45e')
#################################################
cols = ['iid','headline', 'articleBody', 'author', 'date', 'source', 'image', 'counter', 'bookmark', 'readmore']
##################################################
##################################################

def entity_extractor(text, weight = 1):
    """Use Dandelion-API to extract entities from text"""
    response = datatxt.nex(text)
    entity = []
    for annotation in response.annotations:
        entity.append(annotation["spot"])
        w_entity = entity * weight
    return entity, w_entity

def reader_processor(csv, cols):
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
            total.append(w_entity)

    return entites, total

######################################################
######################################################

def category_processor(url):
    df = newsparser(url, cols)
    entites = []
    text = ''
    for i, row in df.iterrows():
        text = text + row["articleBody"] + ' '

    entity, _ = entity_extractor(text)
    entities.extend(entity)
    return entites


entites, total = extract_entities('data/day3.csv', cols)
