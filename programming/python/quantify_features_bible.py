# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 17:15:59 2018

@author: jose
"""

from lxml import etree
import pandas as pd
from collections import Counter
import os
import glob
import re
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from numpy import array


wdir = "/home/jose/Dropbox/biblia/tb/"
file = "TEIBible" # "*.xml"
outdir = "/home/jose/Dropbox/biblia/tb/resulting data/"

books_df = pd.ExcelFile(wdir + "documentation/books.xlsx",  index_col=0).parse('Sheet1').iloc[0:66,:]

parser = etree.XMLParser(encoding='utf-8')
documento_xml = etree.parse(wdir+file+".xml", parser)
documento_root = documento_xml.getroot()
namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}
books_names = [title for book in documento_root.xpath('//tei:TEI', namespaces=namespaces_concretos, with_tail=True) for title in book.xpath('.//tei:title[1]/text()', namespaces=namespaces_concretos, with_tail=True) ]

dict_bible = {}

type_unit = "books"

if type_unit == "books":
    content = documento_root.xpath('//tei:TEI', namespaces=namespaces_concretos, with_tail=True)
elif type_unit == "verses":
    content = documento_root.xpath('.//tei:ab[@type="verse"]', namespaces=namespaces_concretos, with_tail=True)
else:
    print("error!")

for n, book in enumerate(content):
   
    dict_unit = {}
    dict_unit["n"] = n+1

    if type_unit == "books":        
        id_unit = book.xpath('.//tei:title/tei:idno[@type="string"]/text()', namespaces=namespaces_concretos, with_tail=True)[0]
        dict_unit["id"] = id_unit
        dict_unit["id_book"] = id_unit
        title = book.xpath('.//tei:title[1]/text()', namespaces=namespaces_concretos, with_tail=True)[0]
        dict_unit["title"] = title
        dict_unit["viaf"] = book.xpath('.//tei:title/tei:idno[@type="viaf"]/text()', namespaces=namespaces_concretos, with_tail=True)[0]
        verses = book.xpath('.//tei:ab[@type="verse"]', namespaces=namespaces_concretos, with_tail=True)
        dict_unit["verses"] = len(verses)
        dict_unit["number verses"] = len(book.xpath('.//tei:ab[@type="verse"]', namespaces=namespaces_concretos, with_tail=True))
        dict_unit["number chapters"] = len(book.xpath('.//tei:div[@type="chapter"]', namespaces=namespaces_concretos, with_tail=True))
        dict_unit["number pericopes"] = len(book.xpath('.//tei:div[@type="pericope"]', namespaces=namespaces_concretos, with_tail=True))

        print(id_unit, len(verses))

        q_in_verses = []
        rss_in_verses = []
        for verse in verses:
            q_in_verses.append(len(verse.xpath('.//tei:q', namespaces=namespaces_concretos, with_tail=True)))
            rss_in_verses.append(len(verse.xpath('.//tei:rs', namespaces=namespaces_concretos, with_tail=True)))
        
        q_in_verses = np.sort(array(q_in_verses))
        rss_in_verses = np.sort(array(rss_in_verses))
        
        for key, list_ in {"quotations" : q_in_verses, "references" : rss_in_verses}.items():
            
            dict_unit["number of " + key] = len(list_)
            if type_unit == "books":  
                dict_unit["mean number " + key] = list_.mean()
                dict_unit["median number " + key] = np.median(list_)
                dict_unit["std of number of " + key] = np.std(list_, ddof=1)
                dict_unit["1st perc of number of " + key] = list_[0]
                dict_unit["100th perc of number of " + key] = list_[-1]
        
    

    elif type_unit == "verses":        
        id_unit = book.xpath('./@xml:id', namespaces=namespaces_concretos, with_tail=True)[0]
        print(id_unit)
        dict_unit["id"] = id_unit
        dict_unit["id_book"] = re.sub(r"b\.(.*?)\.\d+\.\d+", r"\1", id_unit)
        dict_unit["id_chapter"] = re.sub(r"b\.(.*?\.\d+)\.\d+", r"\1", id_unit)
        verses = book.xpath('.', namespaces=namespaces_concretos, with_tail=True)
        dict_unit["verses"] = len(verses)
        
    
    grouped_referenced_entities = book.xpath('.//tei:rs/@key', namespaces=namespaces_concretos, with_tail=True)
    entities_referenced = [entity for group_entities in grouped_referenced_entities for entity in group_entities.split(" ") ]
    dict_unit["number of entities referred"] =  len(entities_referenced)
    dict_unit["number of different entities referred"] =  len(set(entities_referenced))
    try:
        dict_unit["most common entity id"] =  Counter(entities_referenced).most_common(1)[0][0]
    except:
        dict_unit["most common entity id"] = ""
    try:
        dict_unit["most common entity frecuency"] =  Counter(entities_referenced).most_common(1)[0][1]
    except:
        dict_unit["most common entity frecuency"] = 0
    try:
        dict_unit["second most common entity id"] =  Counter(entities_referenced).most_common(2)[1][0]
    except:
        dict_unit["second most common entity id"] = ""
    try:
        dict_unit["second most common entitity frequency"] =  Counter(entities_referenced).most_common(2)[1][1]
    except:
        dict_unit["second most common entitity frequency"] = 0 
        
    people_referenced = [entity for entity in entities_referenced if "per" in entity]
    groups_referenced = [entity for entity in entities_referenced if "org" in entity]
    places_referenced = [entity for entity in entities_referenced if "pla" in entity]
    times_referenced = [entity for entity in entities_referenced if "tim" in entity]
    works_referenced = [entity for entity in entities_referenced if "wor" in entity]
    for key, list_ in {"people" : people_referenced, "groups" : groups_referenced, "places" : places_referenced,"times" : times_referenced ,"works" : works_referenced }.items():
        if list_ == []:
            dict_unit["most frequent entitiy id "+key] = "-"
            dict_unit["most frequenct entity frequency "+key] = 0
        else:
            dict_unit["most frequent entity id "+key] = Counter(list_).most_common(1)[0][0]
            dict_unit["most frequenct entity frequency "+key] = Counter(list_).most_common(1)[0][1]
            
        dict_unit[key] = len(list_)
        dict_unit["number of different " + key] = len(set(list_))
    if type_unit == "books":
        dict_unit["number of 1st level quotations"] = len(book.xpath('.//tei:ab[@type="verse"]/tei:q', namespaces=namespaces_concretos, with_tail=True))
        dict_unit["number of 2nd level quotations"] = len(book.xpath('.//tei:ab[@type="verse"]/tei:q/tei:q', namespaces=namespaces_concretos, with_tail=True))
        dict_unit["number of 3rd level quotations"] = len(book.xpath('.//tei:ab[@type="verse"]/tei:q/tei:q/tei:q', namespaces=namespaces_concretos, with_tail=True))
        dict_unit["number of 4th level quotations"] = len(book.xpath('.//tei:ab[@type="verse"]/tei:q/tei:q/tei:q/tei:q', namespaces=namespaces_concretos, with_tail=True))
        dict_unit["number of 5th level quotations"] = len(book.xpath('.//tei:ab[@type="verse"]/tei:q/tei:q/tei:q/tei:q/tei:q', namespaces=namespaces_concretos, with_tail=True))
    elif type_unit == "verses":
        dict_unit["number of quotations"] = len(book.xpath('.//tei:q', namespaces=namespaces_concretos, with_tail=True))
        
    
    grouped_who = book.xpath('.//tei:q/@who', namespaces=namespaces_concretos, with_tail=True)
    who_entities = [entity for group_who in grouped_who for entity in group_who.split(" ") ]
    dict_unit["number of entities communicating"] = len(who_entities)
    dict_unit["number of different entities communicating"] = len(set(who_entities))
    
    grouped_toWohm = book.xpath('.//tei:q/@toWhom', namespaces=namespaces_concretos, with_tail=True)
    toWhom_entities = [entity for group_toWohm in grouped_toWohm for entity in group_toWohm.split(" ") ]
    dict_unit["number of entities receiving communication"] = len(toWhom_entities)
    dict_unit["number of different entities receiving communication"] = len(set(toWhom_entities))

    dict_unit["number of oral quotations"] = len(book.xpath('.//tei:q[@type="oral"]', namespaces=namespaces_concretos, with_tail=True))
    dict_unit["number of dream quotations"] = len(book.xpath('.//tei:q[@type="dream"]', namespaces=namespaces_concretos, with_tail=True))
    dict_unit["number of praying quotations"] = len(book.xpath('.//tei:q[@type="prayer"]', namespaces=namespaces_concretos, with_tail=True))
    dict_unit["number of oath quotations"] = len(book.xpath('.//tei:q[@type="oath"]', namespaces=namespaces_concretos, with_tail=True))
    dict_unit["number of written quotations"] = len(book.xpath('.//tei:q[@type="written"]', namespaces=namespaces_concretos, with_tail=True))
    dict_unit["number of song quotations"] = len(book.xpath('.//tei:q[@type="song"]', namespaces=namespaces_concretos, with_tail=True))
    dict_unit["number of soCalled quotations"] = len(book.xpath('.//tei:q[@type="soCalled"]', namespaces=namespaces_concretos, with_tail=True))
    dict_unit["number of idea quotations"] = len(book.xpath('.//tei:q[@type="idea"]', namespaces=namespaces_concretos, with_tail=True))
    

    dict_bible[id_unit] =  dict_unit

    
dataframe_bible = pd.DataFrame(dict_bible).T
dataframe_bible = dataframe_bible[[keys for keys, values in dict_bible[id_unit].items()]]
dataframe_bible = dataframe_bible.sort_values(by=["n"])

dataframe_bible["genre"] = dataframe_bible["id_book"].map(books_df.set_index('codebook')['genre']).fillna("")

dataframe_bible = dataframe_bible[dataframe_bible.columns.tolist()[-1:] + dataframe_bible.columns.tolist()[:-1]]

dataframe_bible.to_csv("/home/jose/Dropbox/biblia/tb/resulting data/quantitative_data_" + type_unit + ".csv", sep="\t")
