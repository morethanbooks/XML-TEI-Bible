# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 08:10:22 2017

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


def analyse_refs(inputtei, file, output):
    
    for doc in glob.glob(inputtei+file+".xml"):

        inputtei_name  = os.path.splitext(os.path.split(doc)[1])[0]
        print(doc, inputtei_name)

        parser = etree.XMLParser(encoding='utf-8')

        # Parseamos el archivo xml-tei
        documento_xml = etree.parse(doc, parser)
        
        # Y lo convertimos en un tipo element
        documento_root = documento_xml.getroot()
        #print(type(documento_root))

        # Definimos el namespace del TEI con el que trabajamos
        namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}

        #print((documento_root.xpath('//tei:rs', namespaces=namespaces_concretos)))

        refs = []
        for ref in documento_root.xpath('//tei:rs', namespaces=namespaces_concretos, with_tail=False):
            if len(ref.xpath('./@key', namespaces=namespaces_concretos)) == 0:
                pass
            else:
                key = ref.xpath('./@key', namespaces=namespaces_concretos)
                #print(type(key[0]))
                text = ' '.join(ref.xpath('.//text()', namespaces=namespaces_concretos)) 
    
                refs.append((key[0],text))
        #print(etree.tostring(documento_root))
        refs_ct = Counter(refs)

        refs_ct = [[items[0], items[1], value] for items, value in refs_ct.items()]# for item1, item2 in items]        
        refs_df = pd.DataFrame(refs_ct, columns=['id','string','freq'])
        refs_df = refs_df.sort_values(by='freq', ascending=False)


        refs_df["number_entities"] = refs_df["id"].str.count(" ")

        #refs_df.loc[ refs_df["id"].str.count(" ", na=False),  "number"] = ">1"


        refs_df["low_string"] = refs_df["string"].str.lower()        
        refs_df["string_len"] = refs_df["string"].apply(lambda x: len(x))

        refs_df["type"] = ""
        refs_df['type'] = refs_df["id"].str[1:4]
                
        print(refs_df)

        refs_df.to_csv(output+file+"refs.csv", sep='\t', encoding='utf-8', index=False)
        refs_df["freq"].plot.hist(bins=100)
        plt.show()
        refs_df["number_entities"].plot.hist(bins=50)
        plt.show()
        refs_df["string_len"].plot.hist(bins=20)
        plt.show()

        return refs_df

def create_edges_coaparence_attribute(refs_df):
    refs_df2 = refs_df.loc[refs_df["number"] > 0]
    list_coaparences = sorted(refs_df2["id"].values.tolist())
    list_coaparences = [i.split(' ') for i in list_coaparences]
    edges = []

    for coaparences in list_coaparences:
        old_nodes = []
        for coaparence1 in (coaparences):
            old_nodes.append(coaparence1)
            for coaparence2 in (coaparences):
                print(coaparence1 ,coaparence2)
                if coaparence1 != coaparence2 and coaparence2 not in old_nodes:
                    edges.append((coaparence1,coaparence2))
    edges_counter = Counter(edges)
    
    edges_df = pd.DataFrame([ [tuple_[0], tuple_[1], value] for tuple_,value in list(edges_counter.items())], columns=["Source","Target","Weight"])
    edges_df = edges_df.sort_values(by='Weight')
    edges_df.to_csv("/home/jose/Dropbox/biblia/tb/resulting data/edges_coaparence_in_attribute_rs.csv", sep='\t', encoding='utf-8', index=True)
    
    return edges_df

    
def create_edges_shared_string(refs_df):
    refs_df2 = refs_df.copy()
    edges = []
    #refs_df2["id"] = refs_df2["id"].apply(lambda x: x.split(' '))
    duplicated_low_strings = refs_df2[refs_df2.duplicated(subset=["low_string"], keep="first")].groupby(('low_string')).min().index
    for duplicated_low_string in duplicated_low_strings:
        print("\n")
        print(duplicated_low_string)
        entities_column = refs_df2.loc[refs_df2["low_string"] == duplicated_low_string, ["id"]]
        plain_entities = []
        for multiple_entities in entities_column.items():
            #i=0
            for entities in multiple_entities[1]:
                for entity in entities.split(" "):
                    plain_entities.append(entity)
        plain_entities = list(set(plain_entities))
        old_entities = []
        if len(plain_entities) > 1:
            for entity1 in plain_entities:
                old_entities.append(entity1)
                for entity2 in plain_entities:
                    if entity1 != entity2 and entity2 not in old_entities:
                        print(entity1,entity2)
                        edges.append(tuple(sorted([entity1,entity2])))
    edges_counter = Counter(edges)
    edges_df = pd.DataFrame([ [tuple_[0], tuple_[1], value] for tuple_,value in list(edges_counter.items())], columns=["Source","Target","Weight"])
    edges_df = edges_df.sort_values(by='Weight')
    edges_df["Type"] = "Undirected"
    edges_df.to_csv("/home/jose/Dropbox/biblia/tb/resulting data/edges_shared_type_string.csv", sep='\t', encoding='utf-8', index=True)
    print(edges)
    #print(duplicated_low_strings["low_string"])
    """
    print(len(duplicated_strings))
    duplicated_strings = duplicated_strings[duplicated_strings== True]
    print(len(duplicated_strings))
    print(duplicated_strings)
    refs_df2
    #for duplicated_string in duplicated_strings.items():
        #print(duplicated_string[0])
        #print(refs_df2.iloc[duplicated_string[0]])
    #print(refs_df2)
    """
    return edges
    
# TODO: hacerlo por cada libro de la Biblia

refs_df = analyse_refs(
        inputtei = "/home/jose/Dropbox/biblia/tb/",
        file = "TEIBible", # "*.xml"
        output = "/home/jose/Dropbox/biblia/tb/resulting data/",
)
#edges_df = create_edges_coaparence_attribute(refs_df)
#edges = create_edges_shared_string(refs_df)

"""
# TODO:
* how many people is mentioned?
* who appears more?
* how much (raw and proportions)?
* who talks more?
* how much (raw and proportions)?
* how many degrees of embbed is the book (average and std)?
* who are the people or groups most talked to?
* how long is the book (in verses and chapters)?
* how much dialogue is there (in proportions to verses?)


* which place?

"""