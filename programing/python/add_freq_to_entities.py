# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 14:37:47 2018

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
import matplotlib.pyplot as plt



wdir = "/home/jose/Dropbox/biblia/tb/"
file = "TEIBible" # "*.xml"

xls = pd.ExcelFile(wdir+"entities.xls",  index_col=0)
entities_orig = xls.parse('Sheet1').fillna("")

entities = entities_orig.copy()

parser = etree.XMLParser(encoding='utf-8')
documento_xml = etree.parse(wdir+file+".xml", parser)
documento_root = documento_xml.getroot()
namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}

books_names = [title for book in documento_root.xpath('//tei:TEI', namespaces=namespaces_concretos, with_tail=True) for title in book.xpath('.//tei:title[1]/text()', namespaces=namespaces_concretos, with_tail=True) ]

referecend_entities = documento_root.xpath('.//tei:rs/@key', namespaces=namespaces_concretos, with_tail=True)

referecend_unique_entities = [character for sublist in referecend_entities for character in sublist.split(" ")]

entities_dict = dict(Counter(referecend_unique_entities).most_common())

df_freq_entities = pd.DataFrame(list(entities_dict.items()), columns=["id", "freq"]).sort_values(by="freq", ascending=False)

entities = pd.merge(entities,df_freq_entities, on="id", how="outer")

if entities.shape[0] == entities_orig.shape[0]:
    print("all good")
    writer = pd.ExcelWriter(wdir+"entities2.xls")
    entities.to_excel(writer,'Sheet1')
    writer.save()
else:
    print("not all good!", entities.head(), entities_orig.head())

print("done")

