# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:35:08 2016

@author: jose
"""
import pandas as pd
import re
import glob
import os
from lxml import etree

"""
def findverse4ids(inputontology,inputtei, outputtei):
"""
"""
get the names from a csv table and place ids as xml elements of rs in a TEI document
df = findverse4ids(
"/home/jose/Dropbox/biblia/tb/ontology.csv",
"/home/jose/Dropbox/biblia/tb/TEIBible.xml",
"/home/jose/Dropbox/biblia/tb/programing/python/output/"
)
"""
"""
get the names from a csv table and place ids as xml elements of rs in a TEI document
df = findverse4ids(
inputontology= "/home/jose/Dropbox/biblia/tb/ontology.csv",
inputtei="/home/jose/Dropbox/biblia/tb/TEIBible.xml",
outputtei"/home/jose/Dropbox/biblia/tb/programing/python/output/"
)
"""
inputontology = "/home/jose/Dropbox/biblia/tb/ontology.csv"
inputtei = "/home/jose/Dropbox/biblia/tb/TEIBible.xml"
outputtei = "/home/jose/Dropbox/biblia/tb/programing/python/output/"


#Lets open the ontology
df=pd.read_csv(inputontology, encoding = "utf-8", sep = ",")
#print(df)

# Lets open the text file
basenamedoc = os.path.basename(inputtei)[:-4]
# The name of the file is saved
docFormatOut=basenamedoc+".xml"
with open(inputtei, "r", errors="replace", encoding="utf-8") as fin:
    content = fin.read()
    df["firstVerse"] =""
    print(df)

    xml = etree.parse(inputtei)
    print(xml)
    namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}


    # It goes row by row
    for index, row in df.iterrows():
        #print(row["normalizedName"])

        if row["normalizedName"] is not "":

            xp_bodytext = "(//body//rs[@key='"+row["id"]+"'])[1]/parent::ab/@xml:id"
            verse=xml.xpath(xp_bodytext, namespaces=namespaces)
            
            print(verse)
            #print(xp_bodytext)
            #print(type(xml.xpath(xp_bodytext, namespaces=namespaces)))

    """
            
        
        # The id is saved in a variable
        idvalue=re.escape(row["id"])
        # The names of the persons are surrounded witht the <rs key="id">
        content = re.sub(r'(\W)('+ re.escape(row["name"]) +r')(\W)', r'\1<rs key="'+idvalue+r'">\2</rs>\3', content, flags=re.DOTALL|re.MULTILINE|re.UNICODE)
    with open (os.path.join(outputtei+docFormatOut), "w", encoding="utf-8") as fout:
        fout.write(content)
return df
            """
