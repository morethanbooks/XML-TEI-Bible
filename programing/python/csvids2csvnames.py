# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:35:08 2016

@author: jose
"""
import pandas as pd
import os


def csvids2csvnames(inputcsv,inputontology,outputfolder,columns, languages):
    """
    It adds a regularized name to a list of csv ids. The user have to give where the csv with the ids is, where the ontology is, where does he want the output file and how are the ids columns called
    Supported languages are for now Spanish (sp), German (ge) and Portuguese (po). If you want it in English or other languages, help us translate the ontolgy file!
    For example:
    df = csvids2csvnames(
    "/home/jose/Dropbox/biblia/tb/programing/xslt/output/b.MAT_rs-ids.csv",
    "/home/jose/Dropbox/biblia/tb/ontology.csv",
    "/home/jose/Dropbox/biblia/tb/programing/python/output/",
    ["id"],
    ["ge", "po","sp"]
    )
    """
    # Lets open the text file
    basenamedoc = os.path.basename(inputcsv)[:-4]
    
    #Lets open the csv ontology file
    dfOntology=pd.read_csv(inputontology, encoding="utf-8", sep="\t")
    #print(dfOntology)
    # NaN is sustitued with zeros
    dfOntology=dfOntology.fillna(value=" ")
    
    #Lets open the csv file
    df=pd.read_csv(inputcsv, encoding="utf-8", sep="\t")
    # NaN is sustitued with zeros
    df=df.fillna(value="0")

    #print(column)
    for language in languages:
    
        # For each column, create another
        for column in columns:
            df[column+"_name"] = " "
            
            for index, row in df.iterrows():
                #print(row[column])
            
                # The line of the ontology is extracted and saved
                dfontologyrow = dfOntology[dfOntology.id == row[column]]
            
                df.at[index,column+"_name"] = ''.join(dfontologyrow["NormalizedName-"+language].get_values())
    
        print("done in ",language)
        
        df.to_csv(outputfolder+language+'_'+basenamedoc+'.csv', sep=';', encoding='utf-8')