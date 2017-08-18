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

        print((documento_root.xpath('//tei:rs', namespaces=namespaces_concretos)))

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
        print(refs_ct)
        #refs_df = pd.DataFrame(list(refs_ct.items()), columns=['value1','value2'])
        return refs_ct
    
refs_ct = analyse_refs(
        inputtei = "/home/jose/Dropbox/biblia/tb/",
        file = "TEIBible", # "*.xml"
        output = "/home/jose/Dropbox/biblia/tb/resulting data/",
)
