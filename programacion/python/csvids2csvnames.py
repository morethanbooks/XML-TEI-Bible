# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:35:08 2016

@author: jose
"""
import pandas as pd
import os


def csvids2csvnames(inputcsv,inputontology,outputfolder,columns):
    """
    It adds a regularized name to a list of csv ids. The user have to give where the csv with the ids is, where the ontology is, where does he want the output file and how are the ids columns called
    For example:
    df = csvids2csvnames(
    "/home/jose/Dropbox/Biblia/TEIBibel/programacion/xslt/output/rs-ids-b.MAT.csv",
    "/home/jose/Dropbox/Biblia/TEIBibel/ontology.csv",
    "/home/jose/Dropbox/Biblia/TEIBibel/programacion/python/output/",
    ["id"],
    )
    """
    """
    inputcsv = "/home/jose/Dropbox/Biblia/TEIBibel/programacion/xslt/output/rs-ids-b.APO.csv"
    inputontology = "/home/jose/Dropbox/Biblia/TEIBibel/ontology.csv"
    outputfolder = "/home/jose/Dropbox/Biblia/TEIBibel/programacion/python/output/"
    columns= ["id"]
    """
    # Lets open the text file
    basenamedoc = os.path.basename(inputcsv)[:-4]
    
    #Lets open the csv ontology file
    dfOntology=pd.read_csv(inputontology, encoding="utf-8", sep="\t")
    #print(dfOntology)
    # NaN is sustitued with zeros
    dfOntology=dfOntology.fillna(value=" ")
    
    #Lets open the csv file
    df=pd.read_csv(inputcsv, encoding="utf-8")
    # NaN is sustitued with zeros
    df=df.fillna(value="0")
    
    # For each column, create another
    for column in columns:
        df[column+"_name"] = " "
        #print(column)
    
        for index, row in df.iterrows():
            #print(row[column])
        
            # The line of the ontology is extracted and saved
            dfontologyrow = dfOntology[dfOntology.id == row[column]]
        
            df.at[index,column+"_name"] = ''.join(dfontologyrow["normalizedName"].get_values())

    print(df)
    
    df.to_csv(outputfolder+basenamedoc+'.csv', sep=';', encoding='utf-8')