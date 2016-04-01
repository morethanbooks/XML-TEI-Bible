# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import re
import os
import glob


def findingq(text):
    """
        It decodes the HTML entities and it deletes some anoying characters
        finq = finq(
        "/home/jose/Dropbox/biblia/tb/genesis.xml",
        "/home/jose/Dropbox/biblia/tb/programing/python/output/"
        )

    """
    text = re.sub(r':? ?«(.*?)»', r' <q who="per1" corresp="#" type="oral" >\1</q>', text, flags=re.MULTILINE)

    text = re.sub(r'xml:id', r'xml_id', text, flags=re.MULTILINE)
    text = re.sub(r'http:', r'http_', text, flags=re.MULTILINE)


    text = re.sub(r'^(\t+)((((?!<q).)*)[^\w](yo|tú|me|soy|te|estoy|he|tengo|tienes|eres|estás|has|ti|mí|mi|tu)[^\w].+)', r'\1<q who="per1" corresp="#" type="oral">\2</q>', text, flags=re.MULTILINE|re.IGNORECASE)

    text = re.sub(r'(<rs key="((per|org)\d+).*?>.*?)<q>', r'\1<q who="\2" corresp="#" type="oral">', text, flags=re.MULTILINE)
    text = re.sub(r'(<rs key="((per|org)\d+).*?>.*?)<q>', r'\1<q who="\2" corresp="#" type="oral">', text, flags=re.MULTILINE)
    text = re.sub(r'(<rs key="((per|org)\d+).*?>.*?)<q>', r'\1<q who="\2" corresp="#" type="oral">', text, flags=re.MULTILINE)

    text = re.sub(r'_', r':', text, flags=re.MULTILINE)

    return text



def finq(inputtei, outputtei):
    """
    finq = finq("/home/jose/Dropbox/TEIBibel/apocalipsis.xml", "/home/jose/Dropbox/TEIBibel/programacion/python/output/")
    """

    i=1
    for doc in glob.glob(inputtei):
    
        # It takes the base name of the html file, it cuts its ending and keeps a new xml name
        basenamedoc = os.path.basename(doc)[:-3]  
        docFormatOut=basenamedoc+"xml"    
    
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
    
        # it cleans the HTML from entities, etc        
        content=findingq(content)
        
     
            
            # It writes the result in the output folder
    
        with open (os.path.join(outputtei, docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
        print(doc)
        print("Processed documents: ",i)
        i+=1