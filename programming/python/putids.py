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
    df = put_ids(
    "/home/jose/Dropbox/biblia/tb/personas-ids-genesis.csv",
    "/home/jose/Dropbox/biblia/tb/genesis.xml",
    "/home/jose/Dropbox/biblia/tb/programming/python/output/"
    )
    """
    #Lets open the csv file
    df=pd.read_csv(inputcsv, encoding = "utf-8", sep = "\t")
    # NaN is sustitued with zeros
    df=df.fillna(value="0")
    print(df)

    # Lets open the text file
    basenamedoc = os.path.basename(inputtei)[:-4]
    # The name of the file is saved
    docFormatOut=basenamedoc+".xml"
    with open(inputtei, "r", errors="replace", encoding="utf-8") as fin:
        content = fin.read()
        #print(df)
        
        # It goes row by row
        for index, row in df.iterrows():
            print(row["name"])
            # The id is saved in a variable
            idvalue=re.escape(row["id"])
            # The names of the persons are surrounded witht the <rs key="id">
            content = re.sub(r'(\W)('+ re.escape(row["name"]) +r')(\W)', r'\1<rs key="'+idvalue+r'">\2</rs>\3', content, flags=re.DOTALL|re.MULTILINE|re.UNICODE)
        with open (os.path.join(outputtei+docFormatOut), "w", encoding="utf-8") as fout:
            fout.write(content)
    return df
