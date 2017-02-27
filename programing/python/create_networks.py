# -*- coding: utf-8 -*-
"""
This script gets the relationships between entities that appear in the same verse (that means, that they are values of the attribute who, corresp or key of the elements q or rs).

"""

from lxml import etree
import pandas as pd
from collections import Counter
import os
import glob
import re


def create_matrix_caracters_castItem(documento_root, namespaces_concretos):
    """
    Esta función crea una matriz con los personajes desde el castList
    """
    # Create empty list
    list_characters = []
    # Sacamos todos los castItems:
    castItems = documento_root.xpath('//tei:castItem', namespaces=namespaces_concretos)
    # Sacamos cada personaje:
    for castItem  in castItems:
        # Sacamos los metadatos
        role_name = "".join(castItem.xpath('tei:role/text()', namespaces=namespaces_concretos))
        role_desc = "".join(castItem.xpath('tei:roleDesc//text()', namespaces=namespaces_concretos))
        id_ = "".join(castItem.xpath('tei:role/@xml:id', namespaces=namespaces_concretos))

        # Añadimos los datos a la cadena original        
        list_characters.append(["#"+id_ , role_name , role_desc]) 
    # Convertimos en dataframe
    df_characters = pd.DataFrame(list_characters, columns=["id","label","description"])
    print(df_characters)
    print("nodes from  castItem done")
    return df_characters

def create_matrix_caracters_text(documento_root, namespaces_concretos, xpaths):

    #print(etree.tostring(documento_root, pretty_print=True, encoding="unicode"))

    list_characters = []
    for element, attributes in xpaths.items():
        for attribute in attributes:
            print(element, attribute)
            list_characters.append((list(set(documento_root.xpath("//tei:"+element+"/"+attribute, namespaces=namespaces_concretos)))))

    list_characters = [item for sublist in list_characters for item in sublist]

    list_characters = [i.split(' ', 1) for i in list_characters]

    list_characters = [item for sublist in list_characters for item in sublist]

    list_characters = sorted(list(set(list_characters)))

    df_characters = pd.DataFrame(list_characters, columns=["id"])
    print(df_characters)
    print("nodes from  text done")
    return df_characters


def create_matrix_text_parts(text_parts, namespaces_concretos):
    """
    Esta función crea una matriz con las unidades que hay en la obra
    """
    list_text_parts = []
    # Sacamos cada escena:
    for text_part  in text_parts:
        # Sacamos los atributos
        text_type = "".join(text_part.xpath('@type', namespaces=namespaces_concretos))
        text_number = "".join(text_part.xpath('@xml:id', namespaces=namespaces_concretos))

        # Añadimos los datos a la lista
        list_text_parts.append([text_number , text_type]) 
    #Convertimos en dataframe
    df_text_parts = pd.DataFrame(list_text_parts, columns=["id","type"])
    print(df_text_parts)
    print("text parts done")
    return df_text_parts


def create_binary_matrix(df_characters, df_text_parts, xpaths, documento_root, namespaces_concretos, border):
    """
    Esta función une los dataframes de characters y text_parts y lo rellena con los valores que encuentra en el texto
    """
    print("seguimos!")
    # Creamos dataframe vacía donde el índice son los personajes y las columnas las escenas
    df_binary_matrix = pd.DataFrame(0, index = df_characters["id"].tolist(), columns = df_text_parts["id"].tolist())
    
    # Iteramos por ambos
    for text_part in df_binary_matrix.columns.tolist():
        for character in df_binary_matrix.index.tolist():
            amount_character = 0
            for element, attributes in xpaths.items():
                for attribute in attributes:
                    # Miramos la cantidad de veces que ese personaje aparece en esa unidad
                    amount_character = amount_character + len(documento_root.xpath('//tei:'+border+'[@xml:id="'+text_part+'"]//tei:'+element+'['+attribute+'="'+character+'"]', namespaces=namespaces_concretos))
            #print(text_part, character, amount_character)
            # Rellenamos la tabla con el valor
            df_binary_matrix[text_part][character] = amount_character
    # Creamos una columna sumatorio, ordenamos por ese valor y borramos la columna
    df_binary_matrix["sum"] = df_binary_matrix.sum(axis="columns")
    df_binary_matrix = df_binary_matrix.sort_values(by=["sum"], ascending=False)
    del df_binary_matrix["sum"]

    print(df_binary_matrix)
    print("binary matrix done")
    return df_binary_matrix
    

def create_edges(df_binary_matrix, edge = "character"):
    """
    Esta función crea la lista de cantos a partir de la matrix binaria
    """
    # Creamos la lista depediendo de qué queremos observar    
    if edge == "text_unit":
        list_nodes = df_binary_matrix.index.tolist()
    elif edge == "character":
        list_nodes = df_binary_matrix.columns.tolist()
        
    edges = []
    old_nodes = []
    # Vamos iterando por cada valor
    for node1 in list_nodes:

        # Y lo ponemos en la lista de entidaddes ya vistas
        old_nodes.append(node1)
        #Iteramos de nuevo por las entidades
        for node2 in list_nodes:
            #print(node1, node2)
  
            # Miramos si la entidad no está ya en la lista
            if node2 not in old_nodes:
                # Dependiendo de qué nos interesa, miramos qué entidades comparten en qué dimensión valores superior a 0
                if edge == "text_unit":
                    #print("vamos!")
                    #print(df_binary_matrix.columns[ (df_binary_matrix.loc[node1] > 0 ) & (df_binary_matrix.loc[node2] > 0 ) ])
                    amount_edges = len(df_binary_matrix.columns[ (df_binary_matrix.loc[node1] > 0 ) & (df_binary_matrix.loc[node2] > 0 ) ] )
                elif edge == "character":
                    amount_edges = len(df_binary_matrix.index[ (df_binary_matrix[node1] > 0 ) & (df_binary_matrix[node2] > 0 ) ] )
                    
                if amount_edges > 0:
                    # Solo guardamos los cantos si estos son más que 0
                    edges.append([node1, node2, amount_edges,"Undirected"])
                    #print(node1, node2, amount_edges)
                    
    # Lo guardamos como dataframe
    df_edges = pd.DataFrame(edges, columns=["Source","Target","Weight","Type"])
    df_edges = df_edges.sort_values(by=["Weight"], ascending=False)
    print(edge, "edges done")
    
    return df_edges

def delete_books(documento_root, book, namespaces_concretos):
    # Intenté hacerlo de manera positiva (es decir, solo seleccionar lo que quería), pero parecía que no borraba del todo el resto de libros y no entendía el funcionamiento realmente
    #print(len(documento_root.xpath('//tei:div[@type="book"][not(@xml:id="b.'+book+'")]', namespaces=namespaces_concretos)))
    for non_wanted_book in documento_root.xpath('//tei:div[@type="book"][not(@xml:id="b.'+book+'")]', namespaces=namespaces_concretos):
        non_wanted_book.getparent().remove(non_wanted_book)

    return documento_root

def spliting_text(documento_root, border, namespaces_concretos, printing = False):
    # Sacamos todos los números de escenas
    text_parts = documento_root.xpath('//tei:'+border+'', namespaces=namespaces_concretos)

    if printing == True:
        for text_part in text_parts:
            print(etree.tostring(text_part, pretty_print=True, encoding="unicode"))

    return text_parts


def create_networks(inputtei, file, output, border, book, deleting_books, characters_in, xpaths):
    
    for doc in glob.glob(inputtei+file+".xml"):
        inputtei_name  = os.path.splitext(os.path.split(doc)[1])[0]
        print(doc, inputtei_name, book)

        # Parseamos el archivo xml-tei
        documento_xml = etree.parse(doc)
    
        # Y lo convertimos en un tipo element
        documento_root = documento_xml.getroot()
        #print(type(documento_root))
    
        # Definimos el namespace del TEI con el que trabajamos
        namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}

        if deleting_books == True:
            documento_root = delete_books(documento_root, book, namespaces_concretos)

        text_parts = spliting_text(documento_root, border, namespaces_concretos)
                
        if characters_in == "castItem":
            df_characters = create_matrix_caracters_castItem(
                    documento_root = documento_root,
                    namespaces_concretos = namespaces_concretos,
                    )
        elif characters_in == "text":
            df_characters = create_matrix_caracters_text(
                    documento_root = documento_root,
                    namespaces_concretos = namespaces_concretos,
                    xpaths = xpaths,
                    )
        df_text_parts = create_matrix_text_parts(
                text_parts = text_parts,
                namespaces_concretos = namespaces_concretos,
                )

        string_xpath = "_"+"-".join(xpaths.keys())+"-".join([item for sublist in list(xpaths.values()) for item in sublist])+"_"
        
        df_binary_matrix = create_binary_matrix(df_characters, df_text_parts, xpaths, documento_root, namespaces_concretos, border)

        df_binary_matrix.to_csv(output+inputtei_name+"_"+book+string_xpath+'_matrix.csv', sep='\t', encoding='utf-8')

        edges_text_unit = create_edges(df_binary_matrix, edge = "text_unit")

        edges_character = create_edges(df_binary_matrix, edge = "character")

        edges_text_unit.to_csv(output+inputtei_name+"_"+book+string_xpath+'_edges_text-unit.csv', sep='\t', encoding='utf-8')
        edges_character.to_csv(output+inputtei_name+"_"+book+string_xpath+'_edges_character.csv', sep='\t', encoding='utf-8')
        df_characters.to_csv(output+inputtei_name+"_"+book+string_xpath+'_nodes_characters.csv', sep='\t', encoding='utf-8')
        df_text_parts.to_csv(output+inputtei_name+"_"+book+string_xpath+'_nodes_text-parts.csv', sep='\t', encoding='utf-8')


create_networks(
        inputtei = "/home/jose/Dropbox/biblia/tb/",
        file = "TEIBible", # "*.xml"
        output = "/home/jose/Dropbox/biblia/tb/resulting data/",
        border = "ab[@type='verse']",
        book = "MAL",
        deleting_books = True,
        characters_in = "text",
        xpaths = {"rs" : ["@key"], "q" : ["@who", "@corresp"]}
        )
