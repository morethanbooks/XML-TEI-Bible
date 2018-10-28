# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import pandas as pd
import re
import glob
import os
from collections import Counter
from lxml import etree
from lxml.etree import tostring
from itertools import chain

communication_verbs = "()"

def finishing_xml(inputcsv, inputtei, outputtei):
    """
    finding_structure = finding_structure("/home/jose/Dropbox/biblia/tb/resulting data/ontology.csv","/home/jose/Dropbox/biblia/tb/programing/python/input/rut.xml", "/home/jose/Dropbox/TEIBibel/programacion/python/output/")
    """
    #Lets open the csv file
    df = pd.ExcelFile(inputcsv,  index_col=0)
    df = df.parse('Sheet1')

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
            
            content = re.sub(r'(="| )([a-z]{3}\d+)', r'\1#\2', content)

            if len(re.findall(r'( (key|corresp|who)(="| ))([a-z])', content)) > 0:
                print("encontrados algunos problemas")
                print(re.findall(r'(<ab.*?(?: (?:key|corresp|who)(?:="| ))([a-z]+).*?</ab>)', content))
            content = re.sub(r'\n\n+', r'\n', content)
            content = re.sub(r'<(div|head)>', r'<\1 type="pericope">', content)
            content = re.sub(r'^\t*(<ab.*?>)', r'\t\t\t\t\t\t\1\n\t\t\t\t\t\t\t', content, flags=re.MULTILINE)
            content = re.sub(r'^\t*(</div>)', r'\t\t\t\t\t\1', content, flags=re.MULTILINE)
            content = re.sub(r'^\t*(<div .*? type="book">)', r'\t\t\t\1', content, flags=re.MULTILINE)
            content = re.sub(r'^\t*(<div .*? type="chapter".*?>)', r'\t\t\t\t\1', content, flags=re.MULTILINE)
            content = re.sub(r'^\t*(<div type="pericope".*?>)', r'\t\t\t\t\t\1', content, flags=re.MULTILINE)
            content = re.sub(r'^\t*(<head type="pericope">)', r'\t\t\t\t\t\t\1', content, flags=re.MULTILINE)
            
            content = re.sub(r'(</ab>)', r'\n\t\t\t\t\t\t\1', content,  flags=re.MULTILINE)
            content = re.sub(r'(<div [^>]*? type="chapter" [^>]*?) cert="high">', r'\1>', content)
    
            with open (os.path.join(outputtei, docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
            print(i)

"""
finishing_xml(
    "/home/jose/Dropbox/biblia/tb/entities.xls",
    "/home/jose/Dropbox/biblia/tb/PHI.xml",
    "/home/jose/Dropbox/biblia/tb/programing/python/output/",
    )
"""
def add_freq_of_entities(wdir = "/home/jose/Dropbox/biblia/tb/", bible_file = "TEIBible", do_overwrite = False):
    print("adding freq of entities to entities.xls")
    xls = pd.ExcelFile(wdir+"entities.xls",  index_col=0)
    entities_orig = xls.parse('Sheet1').fillna("")
    
    entities = entities_orig.copy()
    
    entities.index = entities["id"]
    parser = etree.XMLParser(encoding='utf-8')
    documento_xml = etree.parse(wdir+bible_file+".xml", parser)
    documento_root = documento_xml.getroot()
    namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}
    
    
    books = documento_root.xpath('//tei:TEI', namespaces=namespaces_concretos, with_tail=True)
    titles = []
    for book in books:
        title = book.xpath('.//tei:title[2]/tei:idno[@type="string"]/text()', namespaces=namespaces_concretos, with_tail=True)[0]
        titles.append(title)
        print(title)
        if title in entities.columns.tolist() and do_overwrite == True:
            del entities[title]
        if title not in entities.columns.tolist():
            referecend_entities = book.xpath('.//tei:rs/@key', namespaces=namespaces_concretos, with_tail=True)
        
            referecend_unique_entities = [character for sublist in referecend_entities for character in sublist.split(" ")]
            
            entities_dict = dict(Counter(referecend_unique_entities).most_common())
            
            df_freq_entities = pd.DataFrame(list(entities_dict.items()), columns=["id", title]).sort_values(by=title, ascending=False).fillna(0)
            
            entities = pd.merge(entities,df_freq_entities, on="id", how="outer").fillna(0)

    entities["sum_freq"] = entities[titles].sum(axis=1).astype(int)
    entities["median_freq"] = entities[titles].median(axis=1).astype(int)
    entities["mean_freq"] = entities[titles].mean(axis=1).astype(int)
    entities["std_freq"] = entities[titles].std(axis=1).astype(int)
    
    if entities.shape[0] == entities_orig.shape[0]:
        print("all good")
    else:
        print("not all good!", entities.head(), entities_orig.head())

    writer = pd.ExcelWriter(wdir+"entities2.xls")
    entities.to_excel(writer,'Sheet1')
    writer.save()
    
    print("done")
    return entities




def get_referers_and_refereds(wdir = "/home/jose/Dropbox/biblia/tb/", bible_file = "TEIBible", outdir = "/home/jose/Dropbox/biblia/tb/resulting data/"):
    parser = etree.XMLParser(encoding='utf-8')
    documento_xml = etree.parse(wdir+bible_file+".xml", parser)
    documento_root = documento_xml.getroot()
    namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}

    refereces = documento_root.xpath('.//tei:rs[@key]', namespaces=namespaces_concretos, with_tail=True)

    referenced_reference = []
    for reference in refereces:
        referenceds = reference.xpath('./@key', namespaces=namespaces_concretos, with_tail=True)[0]
        referer = ([reference.text] + list(chain(*([c.text] for c in reference.getchildren()))) )
        referer = ''.join(filter(None, referer))
        print(referer)
        #referer = reference.xpath('.//text()', namespaces=namespaces_concretos, with_tail=True)
        """
        if len(referer) > 0:
            referer = referer[0]
        else:
            referer = ""
        """
        referenceds = referenceds.split(" ")
        #print(reference)
        #print(referenceds)
        #print(reference.text)
        for referenced in referenceds:
            #print(referenced, referer)
            referenced_reference.append((referenced, referer)) 
    df = pd.DataFrame(list(set(referenced_reference)), columns=["id","referer"])
    
    books = documento_root.xpath('//tei:TEI', namespaces=namespaces_concretos, with_tail=True)

    for book in books:
        title = book.xpath('.//tei:title[2]/tei:idno[@type="string"]/text()', namespaces=namespaces_concretos, with_tail=True)[0]
        print(title)
        df[title] = 0
        refereces = book.xpath('.//tei:rs[@key]', namespaces=namespaces_concretos, with_tail=True)
        referenced_reference = []
        for reference in refereces:
            referenceds = reference.xpath('./@key', namespaces=namespaces_concretos, with_tail=True)[0]
            referer = ([reference.text] + list(chain(*([c.text] for c in reference.getchildren()))) )
            referer = ''.join(filter(None, referer))
            #referer = reference.xpath('.//text()', namespaces=namespaces_concretos, with_tail=True)
            """
            if len(referer) > 0:
                referer = referer[0]
            else:
                referer = ""
            """
            referenceds = referenceds.split(" ")
            
            #print(reference)
            #print(referenceds)
            #print(reference.text)
            for referenced in referenceds:
                #print(referenced, referer)
                referenced_reference.append((referenced, referer))
        for tuple_ in Counter(referenced_reference).most_common():
            df.loc[(df["id"] == tuple_[0][0]) & (df["referer"] == tuple_[0][1]), title] = tuple_[1]
    
    df.to_csv(outdir+"referer_refered.csv", sep="\t")
#get_referers_and_refereds()
"""
finishing_xml(
    "/home/jose/Dropbox/biblia/tb/entities.xls",
    "/home/jose/Dropbox/biblia/tb/LAM.xml",
    "/home/jose/Dropbox/biblia/tb/programing/python/output/",
    )
"""
#entities = add_freq_of_entities(do_overwrite=True)
    