# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 11:33:50 2018

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


def get_locations_books(wdir, file, outdir):

    entities = pd.ExcelFile(wdir + "entities.xls",  index_col=0).parse('Sheet1').fillna("")
    
    secure_places = entities.loc[ (entities["type"]== "place" ) & (entities["latitude"]!="" ) & (entities["longitude"]!="") & (entities["geo_cert"].isin(["high","medium"]))]
    secure_places.shape
    
    books = pd.ExcelFile(wdir + "documentation/books.xlsx",  index_col=0).parse('Sheet1').fillna("")
    
    parser = etree.XMLParser(encoding='utf-8')
    
    documento_xml = etree.parse(wdir+file+".xml", parser)
    
    documento_root = documento_xml.getroot()
    
    namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}
    
    books["latitude"] = ""
    books["longitude"] = ""
    
    for book in documento_root.xpath('//tei:TEI', namespaces=namespaces_concretos, with_tail=True):
        title = book.xpath('.//tei:title[2]/tei:idno[@type="string"]/text()', namespaces=namespaces_concretos, with_tail=True)[0]
        rss = book.xpath('.//tei:rs[not(@cert)]/@key|.//tei:rs[@cert="medium"]/@key', namespaces=namespaces_concretos, with_tail=True)
        set_entities = list(set([entity for reference in rss for entity in reference.split(" ")]))
        print(title)
        print(len(rss))
        print(len(set_entities))
    
        longitude = secure_places.loc[secure_places["id"].isin(set_entities)]["longitude"].mean()
        latitude = secure_places.loc[secure_places["id"].isin(set_entities)]["latitude"].mean()
        
        books.loc[books["codebook"]==title, ["longitude"]] = longitude
        
        books.loc[books["codebook"]==title, ["latitude"]] = latitude
        print(longitude, latitude)
        
    
    books.to_excel(wdir+"documentation/books_2.xlsx", encoding="utf-8")
    return books

wdir = "/home/jose/Dropbox/biblia/tb/"
file = "TEIBible" # "*.xml"
outdir = "/home/jose/Dropbox/biblia/tb/resulting data/"

books = get_locations_books(wdir, file, outdir)

#def get_locations_people:

# abrimos la tabla de los libros
# iteramos por los libros
# abrimos la matriz
# por cada     