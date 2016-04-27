# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 18:56:20 2016

@author: jose
"""

import glob
import os
import re
from lxml import etree
import pandas as pd

def main2(inputcsv,inputtei, output, border):
    """
    main2(
    inputcsv = "/home/jose/Dropbox/MTB/proyectos/LiteraturaLab/LotR/basic-data/ontology.csv",
    inputtei = "/home/jose/Dropbox/MTB/proyectos/LiteraturaLab/LotR/text/Tolkien_LotR_processed-rs", 
    output = "/home/jose/Dropbox/MTB/proyectos/LiteraturaLab/LotR/output/",
    border = "p"
    )
    
    """
    # Abrimos la tabla de los nombres y sacamos los nombres

    #Lets open the csv file
    dfontolgy = pd.read_csv(inputcsv, encoding = "utf-8", sep = "\t")
    # NaN is sustitued with zeros
    dfontolgy = dfontolgy.fillna(value="0")
    print(dfontolgy)

    persons = dfontolgy['id'].tolist()
    print(persons)
    
    # Abrimos el archivo. Borramos el front y el back. Borramos también todo el texto.

    networks = {}
    oldPersons = []
    print(inputtei)
    #beta-metadata=["author-text-relation","group-text","protagonist-age","protagonist-name","protagonist-profession","protagonist-social-level","representation","setting-continent","setting-country","setting-name","setting-territory","subgenre-lithist","text-movement","time-period","time-span","type-end"]
    for doc in glob.glob(inputtei+"*.xml"):
        # It takes the base name of the html file, it cuts its ending and keeps a new xml name
        basenamedoc,extesiondoc= os.path.basename(doc).split(".")
        #print("Va el docu!: "+basenamedoc)
    
        with open(doc, "r", errors="replace", encoding="utf-8") as text:           
            text = text.read()

            text = re.sub(r'<teiHeader>.*?</teiHeader>', r'', text)
            text = re.sub(r'<front>.*?</front>', r'', text)
            text = re.sub(r'<back>.*?</back>', r'', text)
            text = re.sub(r'(>)[^<>]*?(<)', r'\1\2', text)
                
            

            ab_text = re.split("(<" + re.escape(border) + r"[^>]*?>.*?</" + re.escape(border) + r">)",text, flags=re.DOTALL)
            #print(ab_text)
            #print(type(text))
            ipersons=0
            for person1 in persons:
                oldPersons.append(person1)
                for person2 in persons:
                    if person2 not in oldPersons:
                        icount=0
                        networks[person1,person2]= [icount]
                        ipersons+=1
                        for ab in ab_text:
                            searchperson1=re.findall("(\"| )"+person1+"(\"| )",ab)
                            searchperson2=re.findall("(\"| )"+person2+"(\"| )",ab)
                            if searchperson1 and searchperson2:
                                networks[person1,person2][0] = networks[person1,person2][0]+1

    
    print(sorted(networks.items(), key=lambda x:x[1]))   
    print(type(networks))
    
    # Creamos un dataframe a partir de ello
    dfnetworks = pd.DataFrame(networks)
    # Le damos la vuelta
    dfnetworks = dfnetworks.T
    # Le ponemos unos títulos chulos a las columnas
    print(dfnetworks)

    dfnetworks.to_csv(output+'networks-id.csv', sep='\t', encoding='utf-8')

    return networks

main2(
    inputcsv = "/home/jose/Dropbox/biblia/tb/ontology.csv",
    inputtei = "/home/jose/Dropbox/biblia/tb/apocalipsis", 
    output = "/home/jose/Dropbox/biblia/tb/programing/python/output/",
    border = "ab"
    )
