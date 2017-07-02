# BOILERPIPE extracts the main Article out of a source page
from boilerpipe.extract import Extractor

# TO MAKE A DATAFRAME
import pandas as pd

# TO GET THE ENTITIES FROM THE TEXT
from dandelion import DataTXT

# TO COUNT THE OCCURENCES in WEIGHTED TOTAL
from collections import Counter
#################################################
#Personal API for using Dandelion-EU
datatxt = DataTXT(app_id='7a313081ecd24154bb78b048090cf45e', app_key='7a313081ecd24154bb78b048090cf45e')

#################################################
cols = ['iid','headline', 'articleBody', 'author', 'date', 'source', 'image', 'counter', 'bookmark', 'readmore']
df = pd.read_csv('data/day3.csv', names = cols)
##################################################

def extract_entities(df):
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
                    external = Extractor(extractor='ArticleExtractor', url=row["source"]).getText()
                except:
                    external = ''
                text = text + " " + external
        #### GENERATING response from Dandelion-EU
        response = datatxt.nex(text)
        entity = []
        for annotation in response.annotations:
            entity.append(annotation["spot"])
        ### entity list for an iid
        w_entity = entity * row["counter"]
        entites.append(entity)
        total.extend(w_entity)

    return entites, total

######################################################

entites, total = extract_entities(df)
print(entites)
print(Counter(total))
