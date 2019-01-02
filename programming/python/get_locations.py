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
import math


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

#books = get_locations_books(wdir, file, outdir)

def get_locations_people(wdir = "/home/jose/Dropbox/biblia/tb/", outdir = "/home/jose/Dropbox/biblia/tb/resulting data/"):
    # abrimos tabla de libros
    books_df = pd.ExcelFile(wdir+"/documentation/books.xlsx").parse('Sheet1').fillna("")
    
    metadata = pd.ExcelFile(wdir+"entities.xls").parse('Sheet1').fillna("")
    metadata.index = metadata["id"]


    books_people_df = pd.DataFrame(columns=books_df.loc[books_df["encoded"]==1]["codebook"].tolist(), index=metadata.loc[metadata["type"]!="place"].index.tolist()).fillna("")

    for book in books_df.loc[books_df["encoded"]==1]["codebook"]:
        print(book)
    
        matrix_units_entities = pd.read_csv(wdir + "/resulting data/TEIBible_"+book+"_q-rs@key-@toWhom-@who__matrix.csv", sep="\t", index_col=0)
            
        places = sorted([entity for entity in matrix_units_entities.index.tolist() if "pla" in entity])
        
        other_entities = sorted([entity for entity in matrix_units_entities.index.tolist() if "pla" not in entity])
        
        matrix_entities_places = pd.DataFrame([], index=other_entities, columns=places).fillna(0)
        
        
        for textual_unit in matrix_units_entities.columns.tolist():
            entities_in_textual_unit_lt = sorted(matrix_units_entities[textual_unit][matrix_units_entities[textual_unit] > 0].index)
            
            if any("pla" in entity for entity in entities_in_textual_unit_lt):
                places_in_textual_unit_lt = [entity for entity in entities_in_textual_unit_lt if "pla" in entity]
                other_entities_in_textual_unit_lt = [entity for entity in entities_in_textual_unit_lt if "pla" not in entity]
                
                for entity in other_entities_in_textual_unit_lt:
                    for place in places_in_textual_unit_lt:
                        matrix_entities_places.loc[entity][place] += 1

        matrix_entities_places.to_csv(outdir+"entities_places_"+book+".csv",sep="\t")
        
        matrix_long = matrix_entities_places.copy()
        for place in matrix_entities_places.columns.tolist():
            if len(metadata.loc[[place]].loc[metadata.loc[[place]]["geo_cert"].isin(["high","medium"])]) > 0:
                matrix_long.loc[ matrix_long[place] >= 1  , place] = str(metadata.loc[place]["latitude"]) +","+ str(metadata.loc[place]["longitude"])
        
        

        for entity in matrix_entities_places.index.tolist():
            latitude = np.array([float(item.split(",")[0]) for item in matrix_long.loc[entity].tolist() if type(item) is str ]).mean()
            longitude = np.array([float(item.split(",")[1]) for item in matrix_long.loc[entity].tolist() if type(item) is str ]).mean()
            if math.isnan(longitude):
                pass
            else:
                books_people_df.loc[entity,book] = str(round(latitude,5)) + "," + str(round(longitude,5))
        print(books_people_df.head())
    books_people_df.to_csv(outdir+"books_entities_latitude_longitude_mean.csv",sep="\t")

get_locations_people()        
# iteramos por libros
#   abrimos la matriz versículos-entidades
#   creamos matriz de coaparición entidad-entidad (columnas y filas entidades)
#   vemos con qué lugares coaparece la entidad
#   guardamos una tabla (por cada libro)
#   mapeamos los lugares con sus coordenadas
#   calculamos la media de longitud y latitud
#   calculamos la mediana de longitud y latitud
#   guardamos la tabla, siendo cada libro una columna y cada fila una entidad
