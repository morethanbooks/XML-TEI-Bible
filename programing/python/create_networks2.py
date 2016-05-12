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

# 0. Pasamos por argumentos a la función: con qué libros queremos trabajar; el modo de definición de las relaciones (por ahora solo tenemos uno realmente)

# 1. Borramos los libros de la Biblia que no son los que se ha señalado por el parámetro con los que se quiere trabajar (estaría bien dar la posibilidad de trabajar con varios)
# 2. Borramos el teiHeader y aquello que no sean versículos
# 3. Ponemos cada versículo en una lista
#   3.1. Borramos texto, elementos y atributos, dejando exclusivamente los valores de los atributos
#   3.2. Por cada elemento de la lista, creamos una sublista donde cada valor del atributo es un elemento
#   3.3. Hacemos un doble bucle con cada lista, colocando las relaciones en una tabla


def main2(inputcsv,inputtei, output, border, book):
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
    #print(dfontolgy)

    persons = dfontolgy['id'].tolist()
    #print(persons)
    
    # Abrimos el archivo. Borramos el front y el back. Borramos también todo el texto.

    networks = {}
    oldPersons = []
    #print(inputtei)
    #beta-metadata=["author-text-relation","group-text","protagonist-age","protagonist-name","protagonist-profession","protagonist-social-level","representation","setting-continent","setting-country","setting-name","setting-territory","subgenre-lithist","text-movement","time-period","time-span","type-end"]
    for doc in glob.glob(inputtei+"*.xml"):
        # It takes the base name of the html file, it cuts its ending and keeps a new xml name
        basenamedoc,extesiondoc= os.path.basename(doc).split(".")
        #print("Va el docu!: "+basenamedoc)
    
        documento_xml = etree.parse(doc)
        #print(documento_xml)
        #print(etree.tostring(documento_xml, pretty_print=True, encoding="unicode"))
        #Definimos los namespaces
        namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}

        # Borramos todos los elementos que no sean el libro que queremos        
        for non_wanted_book in documento_xml.xpath('//tei:div[@type="book"][not(@xml:id="b.'+book+'")]', namespaces=namespaces_concretos):
            non_wanted_book.getparent().remove(non_wanted_book)

        # Borramos teiHeader, front y back
        etree.strip_elements(documento_xml, "{http://www.tei-c.org/ns/1.0}teiHeader", with_tail=False)
        etree.strip_elements(documento_xml, "{http://www.tei-c.org/ns/1.0}front",  with_tail=False)
        etree.strip_elements(documento_xml, "{http://www.tei-c.org/ns/1.0}back",  with_tail=False)
        etree.strip_tags(documento_xml, "{http://www.tei-c.org/ns/1.0}TEI", "{http://www.tei-c.org/ns/1.0}text","{http://www.tei-c.org/ns/1.0}teiCorpus","{http://www.tei-c.org/ns/1.0}body")

        
        print(etree.tostring(documento_xml, pretty_print=True, encoding="unicode"))

        ab_list = documento_xml.xpath('//tei:rs', namespaces=namespaces_concretos,  with_tail=False)

        for ab in ab_list:
            print("rs!: ", type(ab))
            print(etree.tostring(ab, pretty_print=True, encoding="unicode"))
            attribute_list = ab.xpath('/@who|/@key|/@corresp', namespaces=namespaces_concretos)
            for attribute in attribute_list:
                #print("atributo!: ", type(attribute))
                #print(etree.tostring(attribute, pretty_print=True, encoding="unicode"))

                attribute = attribute.split(" ")
                #print(attribute)

            #print(etree.tostring(ab, pretty_print=True, encoding="unicode"))
        #print(ab_list)
        
        """
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
    """

main2(
    inputcsv = "/home/jose/Dropbox/biblia/tb/ontology.csv",
    inputtei = "/home/jose/Dropbox/biblia/tb/programing/python/input/TEIBible", 
    output = "/home/jose/Dropbox/biblia/tb/programing/python/output/",
    border = "ab",
    book = "MAT"
    )
