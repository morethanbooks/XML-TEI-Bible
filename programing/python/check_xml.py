# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import pandas as pd
import re
import glob
import os
from collections import Counter


communication_verbs = "()"

def finding_structure(inputcsv, inputtei, outputtei):
    """
    finding_structure = finding_structure("/home/jose/Dropbox/biblia/tb/resulting data/ontology.csv","/home/jose/Dropbox/biblia/tb/programing/python/input/rut.xml", "/home/jose/Dropbox/TEIBibel/programacion/python/output/")
    """
    #Lets open the csv file
    df = pd.read_csv(inputcsv, encoding = "utf-8", sep = "\t")
    # NaN is sustitued with zeros
    df = df.fillna(value="0")
    #print(df)
    i=1
    for doc in glob.glob(inputtei):
    
        # It takes the base name of the html file, it cuts its ending and keeps a new xml name
        basenamedoc = os.path.basename(doc)[:-3]  
        docFormatOut=basenamedoc+"xml"    
    
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
            
            content = re.sub(r'( (key|corresp|who)(="| ))([a-z])', r'\1#\4', content)

            if len(re.findall(r'( (key|corresp|who)(="| ))([a-z])', content)) > 0:
                print("encontrados algunos problemas")
                print(re.findall(r'( (key|corresp|who)(="| ))([a-z])', content))
            content = re.sub(r'\n\n+', r'\n', content)
            content = re.sub(r'<(div|head)>', r'<\1 type="pericope">', content)
            content = re.sub(r'^\t*(<ab.*?>)', r'\t\t\t\t\t\t\1\n\t\t\t\t\t\t\t', content, flags=re.MULTILINE)
            content = re.sub(r'(</ab>)', r'\n\t\t\t\t\t\t\1', content)
            content = re.sub(r'(<div [^>]*? type="chapter" [^>]*?) cert="high">', r'\1>', content)
    
            with open (os.path.join(outputtei, docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
            print(i)


finding_structure = finding_structure(
    "/home/jose/Dropbox/biblia/tb/resulting data/ontology.csv",
    "/home/jose/Dropbox/biblia/tb/PHM.xml",
    "/home/jose/Dropbox/biblia/tb/programing/python/output/",
    )
