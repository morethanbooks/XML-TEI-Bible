# -*- coding: utf-8 -*-
"""
Created on Mon May  7 06:55:45 2018

@author: jose
"""

import re
import os
import glob
import subprocess
import collections
from nltk.corpus import wordnet as wn
import time 
import shutil
from lxml import etree
import pandas as pd
import time
from collections import Counter

specific_namespaces = {'tei': 'http://www.tei-c.org/ns/1.0', 'xi': 'http://www.w3.org/2001/XInclude',
                       'cligs': 'https://cligs.hypotheses.org/ns/cligs'}


def clean_and_save_file(documento, output_dir, file_name):
    
    #   Guardamos el archivo como anno/archivo.xml
    # TODO: cambiar el tipo narrativo de los pasajes dentro de floating y de sp
    xslt = etree.XSLT(etree.XML('''<?xml version="1.0"?>
        <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:cligs="http://www.w3.org/1999/XSL/argo">
        <xsl:output method="text" encoding="utf8" />
        <xsl:template match="@*|node()">
            <xsl:copy>
                <xsl:apply-templates select="@*|node()" />
            </xsl:copy>
        </xsl:template>
        
        <xsl:template match="token">
            <w><xsl:apply-templates select="@* | node()" /></w>
        </xsl:template>

        <xsl:template match="sentence">
            <s><xsl:apply-templates select="@* | node()" /></s>
        </xsl:template>
        
        <xsl:template match="sentence/@id | token/@id">
            <xsl:attribute name="n">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        
        </xsl:stylesheet>
        '''))

    """
    
        <xsl:template match="@form">
            <xsl:attribute name="cligs:form">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        <xsl:template match="@tag">
            <xsl:attribute name="cligs:tag">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        <xsl:template match="@ctag">
            <xsl:attribute name="cligs:ctag">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>
        
        <xsl:template match="@mood">
            <xsl:attribute name="cligs:mood">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        <xsl:template match="@tense">
            <xsl:attribute name="cligs:tense">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        <xsl:template match="@person">
            <xsl:attribute name="cligs:person">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        <xsl:template match="@num">
            <xsl:attribute name="cligs:num">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        <xsl:template match="@wnsyn">
            <xsl:attribute name="cligs:wnsyn">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        <xsl:template match="@wn">
            <xsl:attribute name="cligs:wnsyn">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        <xsl:template match="@wnlex">
            <xsl:attribute name="cligs:wnlex">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        <xsl:template match="@gen">
            <xsl:attribute name="cligs:gen">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        <xsl:template match="@neclass">
            <xsl:attribute name="cligs:neclass">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        <xsl:template match="@nec">
            <xsl:attribute name="cligs:nec">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>
        

        <xsl:template match="@possessornum">
            <xsl:attribute name="cligs:possessornum">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>

        
        <xsl:template match="@mariax">
            <xsl:attribute name="cligs:mariax">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>
        

        <xsl:template match="@punctenclose">
            <xsl:attribute name="cligs:punctenclose">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>
    """
    documento = xslt(documento)

    document_txt = etree.tostring(documento, encoding="unicode")
    
    document_txt = re.sub(r">\s+</w>", r" />", document_txt, flags=re.MULTILINE)
    document_txt = re.sub(r"^\s*", r"", document_txt, flags=re.MULTILINE)
    document_txt = re.sub(r"\s+<w", r"<w", document_txt)
    
    document_txt = re.sub(r'<TEI.*?>', r'<?xml version="1.0"?><TEI>', document_txt)
    
    document_txt = re.sub(r'<s xmlns:cligs="http://www.w3.org/1999/XSL/argo"', r"<s", document_txt)

    document_txt = re.sub(r'<s n="\d">(.*?)</s>', r'\1', document_txt, flags=re.DOTALL)
    document_txt = re.sub(r'cligs:', r'', document_txt)
    document_txt = re.sub(r'tag="&#10;a +', r'tag="', document_txt)
    
    
    #print(document_txt[0:200])
    with open (output_dir + file_name + ".xml", "w", encoding="utf-8") as fout:
        fout.write(document_txt)
        

def open_temp_anno(xml_file):
    try:
        xml_anno = etree.parse( xml_file ).getroot()
    except:
        if os.stat(xml_file).st_size == 0:
            xml_anno = etree.Element("sentence")
        else:
            print("opening as string")
            with open(xml_file, "r", errors="replace", encoding="utf-8") as fin:
                content = fin.read()
            content = re.sub( r'</sentence>\s+<sentence id="\d+">', r'', content)
            xml_anno = etree.fromstring(content)
    return xml_anno
 


def call_freeling_multiwords():
    # Abrimos freeling para multiwords
    subprocess.call("analyze -f es.cfg --server on --port 50000 --outlv tagged  --sense ukb  --workers 2 --output xml --noloc --nonumb --ner --nec --nodate --noquant &", shell=True)

def call_freeling_tokens():
    # Abrimos freeling para tokens
    subprocess.call("analyze -f es.cfg --server on --port 50005 --outlv tagged  --sense ukb  --workers 2 --output xml --ner --nec &", shell=True)


def refresh_temp(temp_dir):
    #    Borramos y creamos una nueva carpeta temp
    if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

def save_segement_txt(s, text_file):
    # remember the text of the <s>
    text = s.text
    if text == None:
        text = " "
    with open(text_file, "w") as text_file:
        text_file.write(text)
    return text

def use_freeling(text_file, xml_file, port):
    Command = "analyzer_client " + port + " < " + text_file + " > " + xml_file   
    subprocess.call(Command, shell=True)

    
def replace_basic_element(s, text):
    # remove the <s> from its parent
    parent = s.getparent()
    parent.remove(s)
    # create a new <s>
    new_s = etree.SubElement(parent, "s")

    choice = etree.SubElement(new_s, "choice")

    # create the <orig>, set the remembered text on it
    orig = etree.SubElement(choice, "orig")
    orig.text = text

    return choice




        
def open_dpde(proverbs_file = "/home/jose/Dropbox/MTB/investigacion/mytoolbox/dpde/dpde.csv"):
    dpde = pd.read_csv(proverbs_file, sep="\t", index_col=0)
    dpde_ls = dpde.loc[dpde["is_token"] == 0]["discursive_particles"].tolist()

    return dpde_ls

def open_proverbs(proverbs_file = "/home/jose/Dropbox/MTB/investigacion/mytoolbox/refranario/proverbs.csv"):
    # selecciona qué quieres hacer con ciertos tipos textuales (header, stage, l)
    
    proverbs = pd.read_csv(proverbs_file, index_col=0, sep="\t").fillna("")
    
    proverbs_ls = proverbs.replace(to_replace=r'[^\w\s]', value='', regex=True).replace(to_replace=r'[^\w\s]', value='', regex=True)["proverb"].tolist()

    return proverbs_ls


def open_mariax(file = "/home/jose/Dropbox/MTB/investigacion/mytoolbox/mariaX/resulting-data/catalogues_shared-CoNSSA_only-tokens_df.parquet"):
    mariax_df = pd.read_parquet(file)
    return mariax_df

    

def annotate_from_ds(wdir = "/home/jose/cligs/ne/",  
    input_dir = "ds/",
    temp_dir = "temp/",
    output_dir = "partialy_annotated/",
    file = "*.xml",
    xml_unit = "s",):

    input_dir = wdir + input_dir
    temp_dir = wdir + temp_dir
    output_dir = wdir + output_dir

    call_freeling_multiwords()
    call_freeling_tokens()
    refresh_temp(temp_dir)
    #proverbs_ls = open_proverbs()
    #dpde_ls  = open_dpde()
    #mariax_df = open_mariax()
    time.sleep(5)
    for doc in glob.glob(input_dir + file):
        refresh_temp(temp_dir)
        start_time = time.time()
        file_name  = os.path.splitext(os.path.split(doc)[1])[0]
        
        print(output_dir+file_name)
        # We check if the file already exists in output_dir
        if os.path.exists(output_dir+file_name+".xml") == False or file == "ne0334.xml":
            
            with open(doc, "r", errors="replace", encoding="utf-8") as fin:
                content = fin.read()
            content = re.sub(r'<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:cligs="https://cligs.hypotheses.org/ns/cligs">', r'<TEI xmlns:cligs="https://cligs.hypotheses.org/ns/cligs">', content)
            content = re.sub(r'<\?.*?>', r'', content)
            documento = etree.fromstring(content)
    
            # abre un archivo de direct-speech (ds)
            #documento = etree.parse( doc ).getroot()
            #namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}
            
            # hace un bucle sobre las unidades que debe analizar (s)
            sentences = len(documento.xpath("//body//" + xml_unit))
            print(sentences)
            for i, s in enumerate(documento.xpath("//body//" + xml_unit)):
                #print(doc, i)
                #print("starting sentence + --- %s seconds ---" % (time.time() - start_time))
            
                # guardamos el archivo de texto como temp_i.txt
                text_file = temp_dir + "temp_" + str(i) + ".txt"
                text = save_segement_txt(s, text_file)
                
                # analizamos el archivo de texto con freeling-tokens y lo guardamos como tokens_i.xml
                tokens_xml_file = temp_dir + "tokens_" + str(i) + ".xml"
                use_freeling(text_file, tokens_xml_file, port = "50000")
            
                # analizamos el archivo de texto con freeling-multiwords y lo guardamos como multiwords_i.xml
                multiwords_xml_file = temp_dir + "multiwords_" + str(i) + ".xml"
                use_freeling(text_file, multiwords_xml_file, port = "50005")
        
                # comprobamos que tokens_i.xml y multiwords_i.xml existen
                #while (os.path.isfile(multiwords_xml_file) != True ) | (os.path.isfile(tokens_xml_file) != True ):
                #    time.sleep(0.1)
                #print("annotated + --- %s seconds ---" % (time.time() - start_time))
                
                multiwords_annotation = open_temp_anno(multiwords_xml_file) 
                tokens_annotation = open_temp_anno(tokens_xml_file) 
                
                choice = replace_basic_element(s, text)
            
            
                # lo guardamos como elementos
                multiwords_annotation_parent = etree.SubElement(choice, "reg", source="freeling")
                multiwords_annotation_parent.attrib["type"] = "multiwords"
                
                multiwords_annotation_parent.append(multiwords_annotation)
                #print("in tree --- %s seconds ---" % (time.time() - start_time))

                #annotate_lexname(multiwords_annotation_parent)
                #print("lexnames --- %s seconds ---" % (time.time() - start_time))
                #annotate_mariax(multiwords_annotation_parent, mariax_df)
                #print("mariax --- %s seconds ---" % (time.time() - start_time))

                tokens_annotation_parent = etree.SubElement(choice, "reg", source="freeling")
                tokens_annotation_parent.attrib["type"] = "tokens"
                tokens_annotation_parent.append(tokens_annotation)
                
                #add_idiom2choice(choice, text, proverbs_ls)
                #print("refranario --- %s seconds ---" % (time.time() - start_time))
                #add_idiom2choice(choice, text, dpde_ls, source = "dpde", type_ = "dis-part")
                #print("dpde --- %s seconds ---" % (time.time() - start_time))
            

            clean_and_save_file(documento, output_dir, file_name)
            print("converted --- %s seconds ---" % (time.time() - start_time))
            print("mean seconds for sentences", (time.time() - start_time)/ sentences)

def add_idiom2choice(s, idioms_ls, type_ = "proverbs", source = "refranario"):
    idioms_in_s = []
    text = s.xpath(".//orig/text()")[0]
    for idiom in idioms_ls:
        if idiom.lower() in re.sub(r"[^\w\s]", r"", text.lower()):
            #print(idiom)
            idioms_in_s.append(idiom.lower())
    if len(idioms_in_s) > 0:
        idiom_el = etree.SubElement(s.xpath(".//choice")[0], "reg", source = source)
        idiom_el.attrib["type"] = type_
        for idiom_in_s in idioms_in_s:
            etree.SubElement(idiom_el, "phr", text=idiom_in_s)
    #return choice


def annotate_mariax(s, mariax_df):
    for w in s.xpath(".//reg[@source='freeling'][@type='multiwords']/w[@lemma][@pos='noun' or @pos='verb' or @pos='adjective']"):
        lemma = w.xpath('./@lemma')[0] 
        if lemma not in ['ser', 'estar' ,'todo' ,'embargo' ,'haber' ,'hacer' ,'tener', 'dar' ,'echar' ,'claro' ,'echar' ,'poner' ,'bueno' ,'s' ,'sacar','ir','mano','llevar','coger','tomar','correr','dejar','salir']:
            #print(lemma)
            try:
                #mariax_df[lemma]
                #print("yey")
                catalogues = "|".join(mariax_df.loc[mariax_df[lemma]==1].index.tolist())
                w.attrib['mariax'] = catalogues
                #print(catalogues,"\n")
            except:
                pass

def add_entity_ord(document):
    types_tokenization = ["multiwords", "tokens"]
    for type_tokenization in types_tokenization:
        xpath = "//reg[@source='freeling'][@type= '" + type_tokenization+ "' ]/w[@type='proper'][@neclass='person' or @neclass='other']"
        people = document.xpath(xpath)
        ordered_people = Counter([person.attrib["form"] for person in people]).most_common()
        ordered_people = [(s, person[0]) for s, person in enumerate(ordered_people)]
        for person in ordered_people:
            person_ord = person[0]
            person_name = person[1]
            
            try:
                person_elements = document.xpath(xpath + "[@form='"+person_name+"']" )
                for person_element in person_elements:
                    person_element.attrib['ord_ent'] = str(person_ord)
            except:
                pass

def annotate_lexname(s):
    for w in s.xpath(".//tei:anno[@source='freeling'][@type='multiwords']//tei:w", namespaces = specific_namespaces):
        #print(wordnet_numerical_pos, wordnet_numerical_id)
        try:

            wordnet_id = w.xpath('./@wn')[0]
            wordnet_numerical_id = int( re.findall(r"(\d+)",wordnet_id)[0])
            wordnet_numerical_pos =  re.findall(r"\d+\-(.+)",wordnet_id)[0]

            lex_names = wn._synset_from_pos_and_offset(wordnet_numerical_pos, wordnet_numerical_id).lexname()
            w.attrib['wnlex'] = lex_names
        except:
            pass

def add_ling_annotation(wdir = "/home/jose/Dropbox/Doktorarbeit/novelasespanolas/",
    input_dir = "annotated/",
    output_dir = "annotated_lexnames/",
    file = "*.xml",
    xml_unit = "tei:s"):

    input_dir = wdir + input_dir
    output_dir = wdir + output_dir

    proverbs_ls = open_proverbs()
    dpde_ls  = open_dpde()
    mariax_df = open_mariax()

    for doc in glob.glob(input_dir + file):
        file_name  = os.path.splitext(os.path.split(doc)[1])[0]
        print(file_name)
        
        if os.path.exists(output_dir+file_name+".xml") == True:
            
            print("file already exists (either complete or it is running)")
        else:

            start_time = time.time()

            with open (output_dir+file_name+".xml", "w", encoding="utf-8") as fout:
                fout.write("")

            document = etree.parse(doc).getroot()
    
            sentences = len(document.xpath("//tei:body//tei:seg/" + xml_unit, namespaces = specific_namespaces))
            print(sentences)
            for i, s in enumerate(document.xpath("//tei:body//tei:seg/" + xml_unit, namespaces = specific_namespaces)):
                #print(i)

                annotate_lexname(s)
    
                #annotate_mariax(s, mariax_df)
    
                #add_idiom2choice(s, proverbs_ls)
                #add_idiom2choice(s, dpde_ls, source = "dpde", type_ = "dis-part")
                
            add_entity_ord(document)
    
            document.getroottree().write(output_dir + file_name + ".xml", encoding="utf-8")
            print("converted --- %s seconds ---" % (time.time() - start_time))
            print("mean seconds for sentences", (time.time() - start_time)/ sentences)
            
#add_ling_annotation()


def make_files_lighter(wdir = "/home/jose/Dropbox/Doktorarbeit/novelasespanolas/",
    input_dir = "annotated_lexnames/",
    output_dir = "annotated_lexnames/",
    file = "*.xml"):

    input_dir = wdir + input_dir
    output_dir = wdir + output_dir

    for doc in glob.glob(input_dir + file):
        file_name  = os.path.splitext(os.path.split(doc)[1])[0]
        
        print(output_dir+file_name)
        # We check if the file already exists in output_dir
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
        content = re.sub(r'\A', r'<?xml version="1.0" encoding="UTF-8"?>\n', content, flags=re.MULTILINE)
        """
        content = re.sub(r'<TEI .*?>', r'<TEI>', content)
        content = re.sub(r'<s n="\d">(.*?)</s>', r'\1', content, flags=re.DOTALL)
        content = re.sub(r'cligs:', r'', content)
        content = re.sub(r'tag="&#10;a +', r'tag="', content)
        content = re.sub(r'<\?.*?>', r'', content)
        """

        with open (output_dir + file_name + ".xml", "w", encoding="utf-8") as fout:
            fout.write(content)
        
#make_files_lighter()
    
#annotate_from_ds()
