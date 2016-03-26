# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:35:08 2016

@author: jose
"""
import pandas as pd
import os


def csvids2csvnames(inputcsv,inputontology,outputfolder,columns):

    """
    inputcsv = "/home/jose/Dropbox/TEIBibel/datos/mateo-grafo-q-who-q-corresp.csv"
    inputontology = "/home/jose/Dropbox/TEIBibel/ontology.csv"
    outputfolder = "/home/jose/Dropbox/TEIBibel/programacion/python/output/"
    """
    """
    It adds a regularized name to a list of csv ids.
    df = csvids2csvnames("/home/jose/Dropbox/Biblia/TEIBibel/datos/apocalipsis-ids.txt",
    "/home/jose/Dropbox/Biblia/TEIBibel/ontology.csv",
    "/home/jose/Dropbox/Biblia/TEIBibel/programacion/python/output/",
    ["whoid", "correspid"]
    )
    """
    #Lets open the csv file
    df=pd.read_csv(inputcsv, encoding="utf-8")
    # NaN is sustitued with zeros
    df=df.fillna(value="0")
    df["whoname"] = " "
    df["correspname"] = " "
    print(df)
    
    # Lets open the text file
    basenamedoc = os.path.basename(inputcsv)[:-4]
    
    
    #Lets open the csv ontology file
    dfOntology=pd.read_csv(inputontology, encoding="utf-8", sep=";")
    
    print(dfOntology)

    # NaN is sustitued with zeros
    dfOntology=dfOntology.fillna(value=" ")
    
    
    # It goes row by row
    for index, row in df.iterrows():
    
        # The line of the ontology is extracted and saved
        dfontologyrow = dfOntology[dfOntology.id == row["whoid"]]
    
        df.at[index,"whoname"] = ''.join(dfontologyrow["normalizedName"].get_values())
    
        dfontologyrow = dfOntology[dfOntology.id == row["correspid"]]
    
        df.at[index,"correspname"] = ''.join(dfontologyrow["normalizedName"].get_values())
    
    print(df)
    
    df.to_csv(outputfolder+basenamedoc+'.csv', sep=';', encoding='utf-8')

