# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/jose/.spyder2/.temp.py
"""
import re
import os
import glob


def findingq(text):
    """
        It decodes the HTML entities and it deletes some anoying characters
    """
    """
    text = re.sub(r'("(per[0-9]+)((?!"per).)*>[^<]*?)"([^>]*?[^\r])"([^>])', r'\1<!--revisar--><q who="\2">\4</q>\5', text, flags=re.MULTILINE|re.DOTALL)

    text = re.sub(r'((per[0-9]*)((?!"per).)*>[^<]*?)"([^>]*?[^\r]*)"', r'\1<!--revisar--><q who="\2">\4</q>', text, flags=re.MULTILINE|re.DOTALL)

    text = re.sub(r'(<rs key="(per[0-9]+)">((?!"per).)*?>[^<]*?)"([^>\r]*?<*.*?)"?$"', r'\1<!--revisar--><q who="\2">\4</q>', text, flags=re.MULTILINE|re.DOTALL)

    text = re.sub(r'("(per[0-9]+).*?[^!])--([^>].*?)$', r'\1<!--revisar--><q who="\2">\3</q>', text, flags=re.MULTILINE|re.DOTALL)

    text = re.sub(r'("(per[0-9]+).*?[^!])--([^>].*?)$', r'\1<!--revisar--><q who="\2">\3</q>', text, flags=re.MULTILINE|re.DOTALL)
    """
    text = re.sub(r':? ?«(.*?)»', r' <q>\1</q>', text, flags=re.MULTILINE)

    text = re.sub(r'xml:id', r'xml_id', text, flags=re.MULTILINE)
    text = re.sub(r'http:', r'http_', text, flags=re.MULTILINE)


    text = re.sub(r':(.+)', r' <q>\1</q>', text, flags=re.MULTILINE)

    text = re.sub(r'^(\t+)((((?!<q).)*)[^\w](yo|tú)[^\w].+)', r'\1<q>\2</q>', text, flags=re.MULTILINE|re.IGNORECASE)

    text = re.sub(r'(<rs key="((per|org)\d+).*?>.*?)<q>', r'\1<q who="\2">', text, flags=re.MULTILINE)
    text = re.sub(r'(<rs key="((per|org)\d+).*?>.*?)<q>', r'\1<q who="\2">', text, flags=re.MULTILINE)
    text = re.sub(r'(<rs key="((per|org)\d+).*?>.*?)<q>', r'\1<q who="\2">', text, flags=re.MULTILINE)

    text = re.sub(r'_', r':', text, flags=re.MULTILINE)

    return text



def main():
    i=1
    for doc in glob.glob("/home/jose/Dropbox/TEIBibel/juanTEI.xml"):
    
        # It takes the base name of the html file, it cuts its ending and keeps a new xml name
        basenamedoc = os.path.basename(doc)[:-3]  
        docFormatOut=basenamedoc+"xml"    
    
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
    
        # it cleans the HTML from entities, etc        
        content=findingq(content)
        
     
            
            # It writes the result in the output folder
    
        with open (os.path.join("/home/jose/Dropbox/TEIBibel/programacion/python/output/", docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
        print(doc)
        print("Processed documents: ",i)
        i+=1

main()