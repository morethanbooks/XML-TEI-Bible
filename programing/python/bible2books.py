# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 14:33:27 2018

@author: jose
"""

import pandas as pd
import re
import os
import glob 

metadata = pd.read_csv("/home/jose/Dropbox/biblia/tb/documentation/libros.csv", sep="\t")

for doc in glob.glob("/home/jose/Dropbox/biblia/datos/origen/rv95.txt"):
    #print("aquí va doc!!!: ",doc)
    input_name  = os.path.splitext(os.path.split(doc)[1])[0]
    #print(input_name)
    with open(doc, "r", errors="replace", encoding="utf-8") as fin:
        biblia = fin.read()
        for index, row in metadata.iterrows():
            print(row[["id","codebook"]])
            if row["id"] < 66:
                book = re.findall(r"(\n\|"+str(row["id"])+"\|.*?)\n\|"+str(int(row["id"])+1)+"\|", biblia, flags=re.DOTALL)[0]
            else:
                book = re.findall(r"(\n\|"+str(row["id"])+"\|.*?)\Z", biblia, flags=re.DOTALL|re.MULTILINE)[0]
                
            #print(book[0:100])
            with open ("/home/jose/Dropbox/biblia/datos/origen/"+ row["codebook"]+".txt", "w", encoding="utf-8") as fout:
                fout.write(book)
    fin.close() 
