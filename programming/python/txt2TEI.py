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
    text = re.sub(r'\A(.*?)\Z', r'<body>\n<div xml:id="b.' + bookcode + r'" type="book">\n\1\n</div>\n</body>', text, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)

    text = re.sub(r'^\|(\d+)\|(\d+)\|(\d+)\|(.+?)\|\d+', r'<ab xml:id="b.' + bookcode + r'.\2.\3" type="verse" n="\3">\4</ab>', text, flags=re.IGNORECASE|re.MULTILINE)
    text = re.sub(r'(<ab xml:id="(b.' + bookcode + r'.(\d+)).[^>]*?n="1">)', r'\n<div xml:id="\2" type="chapter" n="\3">\n<div type="pericope">\n<head type="pericope"></head>\1', text, flags=re.IGNORECASE|re.MULTILINE)
    text = re.sub(r'(</ab>\s+)(</div|</body>|<div)', r'\1</div>\n</div>\n\2', text, flags=re.IGNORECASE|re.MULTILINE)
    text = re.sub(r'</head>', r'</head>\n', text, flags=re.IGNORECASE|re.MULTILINE)

    text = re.sub(r'</head>', r'</head>\n', text, flags=re.IGNORECASE|re.MULTILINE)

    text = re.sub(r'\A(.*?)\Z', r'<?xml version="1.0" encoding="UTF-8"?>\n<?xml-model href="https://raw.githubusercontent.com/morethanbooks/XML-TEI-Bible/master/scheme/tei_lite.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n<?xml-stylesheet type="text/css" href="styles/styles.css" rel="stylesheet" title="Classic"?>\n<?xml-stylesheet type="text/css" href="styles/word2pix-quotes.css" rel="stylesheet" title="Word2Pix Quotations"?>\n<?xml-stylesheet type="text/css" href="styles/word2pix-reference.css" rel="stylesheet" title="Word2Pix References"?>\n<?xml-stylesheet type="text/css" href="styles/word2pix-level-q.css" rel="stylesheet" title="Word2Pix Level Quotation"?><TEI xmlns="http://www.tei-c.org/ns/1.0">\n	<teiHeader>\n		<fileDesc>\n			<titleStmt>\n				<title></title>\n				<title type="idno">\n					<idno type="string">' + bookcode + r'</idno>\n					<idno type="viaf"></idno>\n				</title>\n				<author>\n					<name type="short"></name>\n					<name type="full"></name>\n					<idno type="viaf"></idno>\n				</author>\n				<principal key="#jct">José Calvo Tello</principal>\n			</titleStmt>\n			<publicationStmt>\n				<publisher>José Calvo Tello</publisher>\n				<availability status="free">\n					<p>The text is freely available.</p>\n				</availability>\n				<date when="2019">2019</date>\n			</publicationStmt>\n			<sourceDesc>\n				<bibl type="digital-source"><date when="2000">2000</date><idno></idno>.</bibl>\n				<bibl type="print-source">Reina Valera, <date when="1995">1995</date></bibl>\n				<bibl type="edition-first"><date when="1569">1569</date></bibl>\n			</sourceDesc>\n		</fileDesc>\n		<encodingDesc>\n			<p></p>\n		</encodingDesc>\n		<revisionDesc>\n			<change when="2019-03-01" who="#jct">First version of </change>\n		</revisionDesc>\n	</teiHeader>\n	<text>\n		<front>\n			<div />\n		</front>\1\n<back />\n</text>\n</TEI>', text, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)



    return text



def main(bookcode):
    i=1
    for doc in glob.glob('/home/jose/Dropbox/biblia/tb/' + bookcode + '.txt'):
    
        # It takes the base name of the html file, it cuts its ending and keeps a new xml name
        basenamedoc = os.path.basename(doc)[:-3]  
        docFormatOut=basenamedoc+"xml"    
    
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
    
        # it cleans the HTML from entities, etc        
        content=txt2TEI(content, bookcode)
        
     
            
            # It writes the result in the output folder
    
        with open (os.path.join("/home/jose/Dropbox/biblia/tb/programming/python/output/", docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
        with open (os.path.join("/home/jose/Dropbox/biblia/tb/programming/python/input/", docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
        print(doc)
        print("Processed documents: ",i)
        i+=1

main("EPH")
