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
import numpy as np


wdir = "/home/jose/Dropbox/biblia/tb/"
file = "TEIBible" # "*.xml"
outdir = "/home/jose/Dropbox/biblia/tb/resulting data/"
import pandas as pd

parser = etree.XMLParser(encoding='utf-8')
documento_xml = etree.parse(wdir+file+".xml", parser)
documento_root = documento_xml.getroot()
namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}
books_names = [title for book in documento_root.xpath('//tei:TEI', namespaces=namespaces_concretos, with_tail=True) for title in book.xpath('.//tei:title[1]/text()', namespaces=namespaces_concretos, with_tail=True) ]

dict_bible = {}
for i, book in enumerate(documento_root.xpath('//tei:TEI', namespaces=namespaces_concretos, with_tail=True)):
    
    dict_book = {}
    dict_book["i"] = i+1
    book_code = book.xpath('.//tei:title/tei:idno[@type="string"]/text()', namespaces=namespaces_concretos, with_tail=True)[0]
    dict_book["code"] = book_code
    title = book.xpath('.//tei:title[1]/text()', namespaces=namespaces_concretos, with_tail=True)[0]
    dict_book["title"] = title
    dict_book["viaf"] = book.xpath('.//tei:title/tei:idno[@type="viaf"]/text()', namespaces=namespaces_concretos, with_tail=True)[0]
    verses = book.xpath('.//tei:ab[@type="verse"]', namespaces=namespaces_concretos, with_tail=True)
    dict_book["verses"] = len(verses)
    dict_book["verses"] = len(book.xpath('.//tei:ab[@type="verse"]', namespaces=namespaces_concretos, with_tail=True))
    dict_book["chapters"] = len(book.xpath('.//tei:div[@type="chapter"]', namespaces=namespaces_concretos, with_tail=True))
    dict_book["pericopes"] = len(book.xpath('.//tei:div[@type="pericope"]', namespaces=namespaces_concretos, with_tail=True))
    dict_bible[book_code] =  dict_book

    print(len(verses))
    q_in_verses = []
    rss_in_verses = []
    for verse in  verses:
        q_in_verses.append(len(verse.xpath('.//tei:q', namespaces=namespaces_concretos, with_tail=True)))
        rss_in_verses.append(len(verse.xpath('.//tei:rs', namespaces=namespaces_concretos, with_tail=True)))
    
    q_in_verses = np.sort(array(q_in_verses))
    rss_in_verses = np.sort(array(rss_in_verses))
    
    for key,list_ in {"q":q_in_verses,"rs":rss_in_verses}.items():
        
        dict_book[""+key] = len(list_)
        dict_book["mean of "+key] = list_.mean()
        dict_book["median of "+key] = np.median(list_)
        dict_book["std of "+key] = np.std(list_, ddof=1)
        dict_book["1st percentile "+key] = list_[0]
        dict_book["100th percentile "+key] = list_[-1]
    
    grouped_referenced_entities = book.xpath('.//tei:rs/@key', namespaces=namespaces_concretos, with_tail=True)
    print("references:", len(grouped_referenced_entities))
    entities_referenced = [entity for group_entities in grouped_referenced_entities for entity in group_entities.split(" ") ]
    print(len(grouped_referenced_entities))
    dict_book["entities referenced"] =  len(entities_referenced)
    dict_book["mq-ent-id-1"] =  Counter(entities_referenced).most_common(1)[0][0]
    dict_book["mq-ent-freq-1"] =  Counter(entities_referenced).most_common(1)[0][1]
    dict_book["mq-ent-id-2"] =  Counter(entities_referenced).most_common(2)[1][0]
    dict_book["mq-ent-freq-2"] =  Counter(entities_referenced).most_common(2)[1][1]
    
    people_referenced = [entity for entity in entities_referenced if "per" in entity]
    groups_referenced = [entity for entity in entities_referenced if "org" in entity]
    places_referenced = [entity for entity in entities_referenced if "pla" in entity]
    times_referenced = [entity for entity in entities_referenced if "tim" in entity]
    works_referenced = [entity for entity in entities_referenced if "wor" in entity]
    for key, list_ in {"pers" : people_referenced, "org" : groups_referenced, "pla" : places_referenced,"tim" : times_referenced ,"wor" : works_referenced }.items():
        if list_ == []:
            dict_book["mf-ent-id-"+key] = "-"
            dict_book["mf-ent-freq-"+key] = "-"
        else:
            dict_book["mf-ent-id-"+key] = Counter(list_).most_common(1)[0][0]
            dict_book["mf-ent-freq-"+key] = Counter(list_).most_common(1)[0][1]
            
        dict_book[key] = len(list_)
        dict_book["diff "+key] = len(set(list_))

    dict_book["1st-lev-q"] = len(book.xpath('.//tei:ab[@type="verse"]/tei:q', namespaces=namespaces_concretos, with_tail=True))
    dict_book["2nd-lev-q"] = len(book.xpath('.//tei:ab[@type="verse"]/tei:q/tei:q', namespaces=namespaces_concretos, with_tail=True))
    dict_book["3rd-lev-q"] = len(book.xpath('.//tei:ab[@type="verse"]/tei:q/tei:q/tei:q', namespaces=namespaces_concretos, with_tail=True))
    dict_book["4th-lev-q"] = len(book.xpath('.//tei:ab[@type="verse"]/tei:q/tei:q/tei:q/tei:q', namespaces=namespaces_concretos, with_tail=True))
    dict_book["5th-lev-q"] = len(book.xpath('.//tei:ab[@type="verse"]/tei:q/tei:q/tei:q/tei:q/tei:q', namespaces=namespaces_concretos, with_tail=True))
    
    grouped_who = book.xpath('.//tei:q/@who', namespaces=namespaces_concretos, with_tail=True)
    who_entities = [entity for group_who in grouped_who for entity in group_who.split(" ") ]
    dict_book["who ent"] = len(who_entities)
    dict_book["diff who ent"] = len(set(who_entities))
    
    grouped_toWohm = book.xpath('.//tei:q/@corresp', namespaces=namespaces_concretos, with_tail=True)
    toWhom_entities = [entity for group_toWohm in grouped_toWohm for entity in group_toWohm.split(" ") ]
    dict_book["toWhom ent"] = len(toWhom_entities)
    dict_book["diff toWhom ent"] = len(set(toWhom_entities))

    dict_book["q-oral"] = len(book.xpath('.//tei:q[@type="oral"]', namespaces=namespaces_concretos, with_tail=True))
    dict_book["q-dream"] = len(book.xpath('.//tei:q[@type="dream"]', namespaces=namespaces_concretos, with_tail=True))
    dict_book["q-prayer"] = len(book.xpath('.//tei:q[@type="prayer"]', namespaces=namespaces_concretos, with_tail=True))
    dict_book["q-oath"] = len(book.xpath('.//tei:q[@type="oath"]', namespaces=namespaces_concretos, with_tail=True))
    dict_book["q-written"] = len(book.xpath('.//tei:q[@type="written"]', namespaces=namespaces_concretos, with_tail=True))
    dict_book["q-song"] = len(book.xpath('.//tei:q[@type="song"]', namespaces=namespaces_concretos, with_tail=True))
    
    
dataframe_bible = pd.DataFrame(dict_bible).T
dataframe_bible = dataframe_bible[['code', 'i', 'title','viaf', 'verses', 'chapters', 'pericopes', 
       'entities referenced',
       'mq-ent-id-1', 'mq-ent-freq-1',        'mq-ent-id-2',  'mq-ent-freq-2', 
       'pers', 'pla','org','wor', 'tim',
       'diff org', 'diff pers', 'diff pla',
       'diff tim', 'diff toWhom ent', 'diff who ent', 'diff wor',
       'rs', 
       'mean of rs', 'median of rs',       'std of rs',
       '1st percentile rs', '100th percentile rs', 
       'q',
       'mean of q',  'median of q','std of q',
       '1st percentile q', '100th percentile q',
       '1st-lev-q', '2nd-lev-q', '3rd-lev-q', '4th-lev-q', '5th-lev-q',
       'mf-ent-freq-org', 'mf-ent-freq-pers',
       'mf-ent-freq-pla', 'mf-ent-freq-tim', 'mf-ent-freq-wor',
       'mf-ent-id-org', 'mf-ent-id-pers', 'mf-ent-id-pla', 'mf-ent-id-tim',
       'mf-ent-id-wor',    'q-dream',
       'q-oath', 'q-oral', 'q-prayer', 'q-song', 'q-written', 
       'toWhom ent',  'who ent',
]]
dataframe_bible = dataframe_bible.sort_values(by=["i"])
dataframe_bible.to_csv("/home/jose/Dropbox/biblia/tb/resulting data/metadata_structuve.csv", sep="\t")

