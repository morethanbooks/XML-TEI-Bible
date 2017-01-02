# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/jose/.spyder2/.temp.py
"""
import re
import os
import glob


def txt2TEI(text, bookcode):
    """
        It decodes the HTML entities and it deletes some anoying characters
    """
    text = re.sub(r'\A(.*?)\Z', r'<body>\n<ab xml:id="b.' + bookcode + r'" type="book">\n\1\n</div>\n</body>', text, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)

    text = re.sub(r'^\|(\d+)\|(\d+)\|(\d+)\|(.+?)\|\d+', r'<ab xml:id="b.' + bookcode + r'.\2.\3" type="verse" n="\3">\4</ab>', text, flags=re.IGNORECASE|re.MULTILINE)
    text = re.sub(r'(<ab xml:id="(b.' + bookcode + r'.(\d+)).[^>]*?n="1">)', r'\n<div xml:id="\2" type="chapter" n="\3">\n<div type="pericope">\n<head type="pericope"></head>\1', text, flags=re.IGNORECASE|re.MULTILINE)
    text = re.sub(r'(</ab>\s+)(<div|</body>)', r'\1</div>\n</div>\n\2', text, flags=re.IGNORECASE|re.MULTILINE)



    return text



def main(book, bookcode):
    i=1
    for doc in glob.glob('/home/jose/Dropbox/biblia/tb/programing/python/input/' + book + '.txt'):
    
        # It takes the base name of the html file, it cuts its ending and keeps a new xml name
        basenamedoc = os.path.basename(doc)[:-3]  
        docFormatOut=basenamedoc+"xml"    
    
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
    
        # it cleans the HTML from entities, etc        
        content=txt2TEI(content, bookcode)
        
     
            
            # It writes the result in the output folder
    
        with open (os.path.join("/home/jose/Dropbox/biblia/tb/programing/python/output/", docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
        print(doc)
        print("Processed documents: ",i)
        i+=1

main("MIC","MIC")