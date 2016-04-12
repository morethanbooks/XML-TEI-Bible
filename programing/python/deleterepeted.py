# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:35:08 2016

@author: jose
"""
import pandas as pd
import os
"""
def deleteRepeated(inputcsv,inputontology,outputfolder):
"""
"""
df = deleteRepeated(
"/home/jose/Dropbox/biblia/tb/genesis_ProperNames.csv",
"/home/jose/Dropbox/biblia/tb/ontology.csv",
"/home/jose/Dropbox/biblia/tb/"
)
"""
inputcsv = "/home/jose/Dropbox/biblia/tb/genesis_ProperNames.csv"
inputontology = "/home/jose/Dropbox/biblia/tb/ontology.csv"
outputfolder = "/home/jose/Dropbox/biblia/tb/"
# Lets open the text file
basenamedoc = os.path.basename(inputcsv)[:-4]

#Lets open the csv ontology file
dfOntology=pd.read_csv(inputontology, encoding="utf-8", sep="\t")
#print(dfOntology)
# NaN is sustitued with zeros
dfOntology = dfOntology.fillna(value=" ")

#Lets open the csv file
df = pd.read_csv(inputcsv, encoding="utf-8", sep="\t")
# NaN is sustitued with zeros
#print(df)
#print(type(dfOntology))

normalizedName = dfOntology["normalizedName"]

print(type(normalizedName))
print(normalizedName)

for index, row in df.iterrows():
    #print(row["name"])

    if row["name"] in normalizedName.any() == True:
        print("borrando!"+ row.loc(["name"]))
        #row = row.drop()


#print(df)  

df.to_csv(outputfolder+basenamedoc+'_cleaned.csv', sep=';', encoding='utf-8')    
