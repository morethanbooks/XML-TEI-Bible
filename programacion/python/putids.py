# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:35:08 2016

@author: jose
"""
import pandas as pd
import re
import glob
import os

def put_ids(inputcsv,inputtei, outputtei,):
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

    """
    for doc in glob.glob(wdir+txtFolder+"*"):
        
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()

            #We create a list for the names
            names=[]
            # We search for any word that starts with capital letter and that before didn't have anything that looks like an starting of a sentence
            names = re.findall(r'(?<=[a-zá-úñüç,;] )([A-ZÁ-ÚÜÑ][a-zá-úñüç]+)', content)

            # We delete the duplicated items in the list            
            names=list(set(names))
            #print(names)
            
            # Now we put the list in a data frame
            df=pd.DataFrame(names,columns=["name"])
            #print(df)
            #And we add a new column for the frequency and we fill it with zeros
            df["frequency"]=0
            #print(df)

            # Now, for every row, we take the indexes and the other columns with the real values (names and frequency)            
            for index, row in df.iterrows():
                # For each, we fill the frecuency with the the amount (len) of a times that the name appears in the text with something 
                df.at[index,"frequency"] = len(re.findall(r'[^a-zá-úçñüA-ZÁ-ÚÜÑ\-]'+ re.escape(row["name"]) + r'[^a-zá-úçñüA-ZÁ-ÚÜÑ\-]', content))
            df=df.sort(["frequency"], ascending=True)
            print(df)
            df.to_csv(wdir+'out.csv')
    return df
    """