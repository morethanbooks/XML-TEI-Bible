# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""
Created on Fri May 15 19:43:50 2020

@author: jose
"""

# abre y parsea la taxonomía

# Abre el archivo
# saca todo los comentarios que empiecen por <!--sex(o)? junto con la referencia al versículo
# aisla el número de versículo
# añade al final un punto y coma
# aisla cada uno de las diferentes anotaciones
# aisla cada una de las diferentes posibilidades
# aisla el valor
# aisla el atributo given
# aisla el atributo cert
# revisa valor, atributo given y atributo cert
# coloca valores en elemento

import os
import glob 
from lxml import etree
import Levenshtein
import re
import pandas as pd




def open_book(wdir_str, file_str):

    print(glob.glob(wdir_str + file_str))
    doc_str = glob.glob(wdir_str + file_str)[0]
    input_name_str  = os.path.splitext(os.path.split(doc_str)[1])[0]
    print(input_name_str)
    with open(doc_str, "r", errors="replace", encoding="utf-8") as fin:
        content_str = fin.read()
    
        print(type(content_str))
    return content_str


def open_taxonomy(wdir_str, taxonomy_file_str):

    taxonomy_el = etree.parse(wdir_str + taxonomy_file_str).getroot()
    print(type(taxonomy_el))
    return taxonomy_el



def get_list_categories(taxonomy_el, namespaces):
    
    categories_id_lt = taxonomy_el.xpath('//tei:category/@xml:id', namespaces = namespaces)
    
    return categories_id_lt



def parse_sexual_annotations_from_comments(book_str):
    sexual_annotations_from_comments_lt = re.findall('<ab xml:id="(.*?)".*?>\s*<!--\s*sexo?:\s*(.*?) ?;? ?-->', book_str)
    print(sexual_annotations_from_comments_lt)
    return sexual_annotations_from_comments_lt


def find_most_similar_id_of_errors(error_lt, categories_id_lt, standOff_str):
    set_wrong_ids_lt = list(set([list_[1] for list_ in error_lt]))
    for wrong_id_str in set_wrong_ids_lt:
        ratios_category_ids = []
        for category_id_str in categories_id_lt:
            ratio_nr = Levenshtein.ratio(wrong_id_str, category_id_str) 
            ratios_category_ids.append([category_id_str, ratio_nr])
            
        labels_ratio_df = pd.DataFrame(ratios_category_ids, columns=["category", "ratio"]).sort_values(by="ratio", ascending=False)
        #print("labels_ratio_df", labels_ratio_df)
        print("\n")
        to_print = "Consider substitue " + str(wrong_id_str) + " with " + str(labels_ratio_df.iloc[0][0]) + " . Levenshtein ratio:" + str(round(labels_ratio_df.iloc[0][1],2))
        response = input(to_print)
        print(to_print)
        replace_with = ""
        if response not in ["", "0", 0, "n", "no"]:
            if response in ["1", "y", "yes", "s", "sí", 1]:
                replace_with = labels_ratio_df.iloc[0][0]
                print("Replacement accepted")
            else:
                replace_with = response
                print("Replacement modified with", response)
            standOff_str = re.sub('"' + wrong_id_str + '"', '"' + replace_with + '"', standOff_str, flags=re.M)
        else:
            print("Replacement rejected. No change.")
    return standOff_str


def parse_each_sexual_annotation_as_comment(sexual_annotations_from_comments_lt,
    categories_id_lt,
    book_name_str, 
    wdir_str = "./../../../sexual-annotation/",
    ):
    error_lt = []
    
    standOff_str = '<standOff xml:id="b.' + book_name_str + '.sexualThemes"  scheme="taxonomy.xml">\n'
    
    for verse_group_annotations_tp in sexual_annotations_from_comments_lt:
        verse_id_str, annotations_of_verse_str = verse_group_annotations_tp[0], verse_group_annotations_tp[1]
        print(verse_id_str)
        #print(len(group_annotations_str), (group_annotations_str))
        #group_annotations_str = group_annotations_str + ";"
        for different_annotations_str in list(filter(None, annotations_of_verse_str.split(sep=";"))):
            if different_annotations_str == " ":
                pass
            else:
                print(different_annotations_str)
                spanGrp_str = '<spanGrp type="theme" inst="#' + verse_id_str+ '">'        
                for optional_annotation_str in list(filter(None, different_annotations_str.split(sep="|"))):
                    value_str = re.findall(r"^\s*([^ ]+)", optional_annotation_str,  flags=re.MULTILINE|re.DOTALL)[0]
                    span_str = '\n\t<span ana="' + value_str+ '">\n\t\t<certainty match="@ana" locus="value"'
                    print(type(value_str))
                    print(value_str)
                    if "cert=" in optional_annotation_str:
                        cert_str = re.findall(r'cert="(.*?)"', optional_annotation_str)[0]
                    else:
                        cert_str = "high"
                    span_str = span_str + ' cert="' + cert_str+ '"'
                        
                    if "given=" in optional_annotation_str:
                        given_str = re.findall(r'given="(.*?)"', optional_annotation_str)[0]
                    else:
                        given_str = "text"
        
                    span_str = span_str + ' given="' + given_str+ '"'
        
                    span_str = span_str + "/>\n\t</span>"
        
                    if value_str not in categories_id_lt:
                        print("ERROR!!", value_str)
                        error_lt.append([verse_id_str, value_str])
                    spanGrp_str = spanGrp_str + span_str
                spanGrp_str = spanGrp_str + "\n</spanGrp>\n"
                standOff_str = standOff_str + spanGrp_str
    standOff_str = standOff_str + "\n</standOff>"

    #print(standOff_str)
    print("errors", error_lt)
    from collections import Counter
    print (Counter([verse_annotation[1] for verse_annotation in error_lt]).most_common())
    
    standOff_str = find_most_similar_id_of_errors(error_lt, categories_id_lt, standOff_str)


    

    text_file = open(wdir_str + "standOff_element.xml", "w")
    n = text_file.write(standOff_str)
    text_file.close()
    return error_lt, standOff_str



def save_book_with_standOff_element(book_str, standOff_str,
    book_name_str,
    wdir_str = "./../../sexual-annotation/",
    ):
    book_str = re.sub(r'\s*<!--\s*sexo?:\s*(.*?) ?;? ?-->', r'', book_str)
    book_str = re.sub(r'</text>', r'</text>\n' + standOff_str, book_str)

    text_file = open(wdir_str + book_name_str + "_standOff.xml", "w", encoding="utf-8")
    text_file.write(book_str)
    text_file.close()
   

