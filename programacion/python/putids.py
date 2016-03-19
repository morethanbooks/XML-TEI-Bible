# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:35:08 2016

@author: jose
"""
import pandas as pd
import re
import glob
import os

def put_ids(inputcsv,inputtei, outputtei):
    """
    get the names from a csv table and place ids as xml elements of rs in a TEI document
    df = put_ids("/home/jose/Dropbox/TEIBibel/datos/personas-ids-apocalipsis.csv", "/home/jose/Dropbox/TEIBibel/apocalipsis.xml","/home/jose/Dropbox/TEIBibel/programacion/python/output/")
    """
    #Lets open the csv file
    df=pd.read_csv(inputcsv, encoding="utf-8")
    df=df.fillna(value="0")
    print(df)

    # Lets open the text file
    basenamedoc = os.path.basename(inputtei)[:-4]  
    docFormatOut=basenamedoc+".xml"
    with open(inputtei, "r", errors="replace", encoding="utf-8") as fin:
        content = fin.read()
    
        #print(df)
    
        for index, row in df.iterrows():
            print(row["name"])
            idvalue=re.escape(row["id"])
            content = re.sub(r'(\W)('+ re.escape(row["name"]) +r')(\W)', r'\1<rs key="'+idvalue+r'">\2</rs>\3', content, flags=re.DOTALL|re.MULTILINE|re.UNICODE)
        with open (os.path.join(outputtei+docFormatOut), "w", encoding="utf-8") as fout:
            fout.write(content)
    return df