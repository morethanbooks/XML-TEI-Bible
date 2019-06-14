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
import networkx as nx
import matplotlib.pyplot as plt
from itertools import count
import numpy as np


namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}


def create_matrix_caracters_text(document_root, namespaces_concretos, xpaths):


    list_characters = [
    list(set(document_root.xpath("//tei:"+element+"/"+attribute, namespaces=namespaces_concretos)))
    for element, attributes in xpaths.items()
    for attribute in attributes
    ]
    list_characters = list(set([character for sublist in list_characters for item in sublist for character in item.split(" ")]))


    df_characters = pd.DataFrame(list_characters, columns=["id"])
    print(sorted(df_characters["id"].tolist()))

    print("nodes from text done: ", df_characters.shape)
    print(df_characters)
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
    print("text parts done: ", df_text_parts.shape)
    print(df_text_parts)
    return df_text_parts

    

def create_binary_matrix(df_characters, df_text_parts, xpaths, text_parts, namespaces_concretos, border):
    # Creamos dataframe vacía donde el índice son los personajes y las columnas las escenas
    df_binary_matrix = pd.DataFrame(0, index = df_characters["id"].tolist(), columns = df_text_parts["id"].tolist())
    #print(df_binary_matrix)
    # Miramos cada verso
    print("", len(text_parts))
    for text_part in text_parts:
        id_text_part = text_part.xpath('@xml:id')
        id_text_part = id_text_part[0]

        # Para ser más eficientes, sacamos una lista de los personaes que aparecen en ese verso
        list_characters = [
        list((text_part.xpath('//tei:'+border+'[@xml:id="'+id_text_part+'"]//tei:'+element+"/"+attribute, namespaces=namespaces_concretos)))
        for element, attributes in xpaths.items()
        for attribute in attributes
        ]
        list_characters = (([character for sublist in list_characters for item in sublist for character in item.split(" ")]))
        #print(id_text_part, etree.tostring(text_part, pretty_print=True, encoding="unicode"), list_characters)
        
        for character in list_characters:
            #print(character, id_text_part)
            #print("selecionando: ", df_binary_matrix[id_text_part][character])
            df_binary_matrix[id_text_part][character] += 1

    print(df_binary_matrix)
    print("binary matrix done: ", df_binary_matrix.shape)
    return df_binary_matrix

def create_edges2(df_binary_matrix, edge = "character"):
    """
    Esta función crea la lista de cantos a partir de la matrix binaria
    """
    print("empezando edges: ")
    edges = []
    # Creamos la lista depediendo de qué queremos observar    
    if edge == "text_unit":
        list_nodes = df_binary_matrix.index.tolist()
        list_edges = df_binary_matrix.columns.tolist()
        
    elif edge == "character":
        list_nodes = df_binary_matrix.columns.tolist()

    #print(list_edges)
    for unit_edge in list_edges:
        old_entity = []
        #print(sorted(df_binary_matrix[unit_edge][df_binary_matrix[unit_edge] > 0].index))
        for entity1 in sorted(df_binary_matrix[unit_edge][df_binary_matrix[unit_edge] > 0].index):
            old_entity.append(entity1)
            for entity2 in sorted(df_binary_matrix[unit_edge][df_binary_matrix[unit_edge] > 0].index):
                #print(entity1,entity2)
                if entity1 != entity2 and entity2 not in old_entity:
                    edges.append((entity1,entity2))
    counter_edges = Counter(edges)

    edges = [[tuplecita[0], tuplecita[1], frequency] for tuplecita,frequency in counter_edges.items()]
    df_edges = pd.DataFrame(edges, columns = ["Source","Target","Weight"])
    df_edges["Type"] = "Undirected"

    print(df_edges, "edges done: ", df_edges.shape)
    return df_edges

def delete_books(documento_root, book, namespaces_concretos):
    # Intenté hacerlo de manera positiva (es decir, solo seleccionar lo que quería), pero parecía que no borraba del todo el resto de libros y no entendía el funcionamiento realmente
    #print(len(documento_root.xpath('//tei:div[@type="book"][not(@xml:id="b.'+book+'")]', namespaces=namespaces_concretos)))
    for non_wanted_book in documento_root.xpath('//tei:div[@type="book"][not(@xml:id="b.'+book+'")]', namespaces=namespaces_concretos):
        non_wanted_book.getparent().remove(non_wanted_book)

    return documento_root

def spliting_text(documento_root, border, namespaces_concretos, printing = True):
    # Sacamos todos los números de escenas
    text_parts = documento_root.xpath('.//tei:'+border+'', namespaces=namespaces_concretos)

    if printing == True:
        for text_part in text_parts:
            print(etree.tostring(text_part, pretty_print=True, encoding="unicode"))

    return text_parts

def xpath2string(xpaths):
    string_xpath = "_"+"-".join(sorted(list(xpaths.keys())))+"-".join(sorted([item for sublist in list(xpaths.values()) for item in sublist]))+"_"
    return string_xpath


def open_and_clean_tei(inputtei, file,  book):

    doc = glob.glob(inputtei+file+".xml")[0]
    inputtei_name  = os.path.splitext(os.path.split(doc)[1])[0]
    print(doc, inputtei_name)

    # Parseamos el archivo xml-tei
    document_xml = etree.parse(doc)

    # Y lo convertimos en un tipo element
    document_root = document_xml.getroot()

    return document_root, inputtei_name

    
 
def create_directed_network(inputtei, file,  output, book, xpaths):
    
    document_root, inputtei_name = open_and_clean_tei(inputtei, file,  book)
    string_xpath = xpath2string(xpaths)


    xpath_element = list(xpaths.keys())[0]
    
    xpath_source = list(xpaths.values())[0][0]
    xpath_target = list(xpaths.values())[0][1]
    xpath_type = list(xpaths.values())[0][2]
    
    print(xpath_source,xpath_target,xpath_type)

    communication_list = []    

    if book in [""," ", "Bible"]:
        xpath_root = '//tei:teiCorpus'
    else:
        xpath_root = './/tei:div[@type="book"][@xml:id="b.' + book + '"]'

    complete_xpath = xpath_root + '//tei:' + xpath_element + "[" + xpath_source + "][" + xpath_target+"]["+xpath_type + "]"
    print(complete_xpath)
    for element in document_root.xpath(complete_xpath, namespaces=namespaces_concretos):
        #print(element.text)
        #print(element.xpath("//"+xpath_source))
        sources = element.xpath(".//"+xpath_source)[0].split(" ")
        targets = element.xpath(".//"+xpath_target)[0].split(" ")
        type_communication = element.xpath(".//"+xpath_type)[0]
        seen_sources = []
        seen_targets = []
        for source in sources:
            for target in targets:
                if target not in seen_targets and source not in seen_sources:
                    communication_list.append((source,target,type_communication))
                    seen_sources.append(source)
                    seen_targets.append(target)

    communication_ct = Counter(communication_list)
    
    edges_df = pd.DataFrame([[edge[0][0], edge[0][1], edge[0][2], edge[1]] for edge in list(communication_ct.items())], columns=["Source","Target","Via","Weight"])
    edges_df["Type"] = "Directed"
    edges_df = edges_df.sort_values(by="Weight", ascending=False)

    edges_df.to_csv(output+inputtei_name+"_"+book+string_xpath+'_edges_text-unit.csv', sep='\t', encoding='utf-8')

    return edges_df




def create_undirected_network(inputtei, file, output, border, book, characters_in, xpaths):
    
    document_root, inputtei_name = open_and_clean_tei(inputtei, file, book)

    if book in [""," ", "Bible"]:
        xpath_root = '//tei:teiCorpus'
    else:
        xpath_root = './/tei:div[@type="book"][@xml:id="b.' + book + '"]'

    book_xml =  document_root.xpath(xpath_root, namespaces=namespaces_concretos)[0]

    print(len(book_xml))
    text_parts = spliting_text(book_xml, border, namespaces_concretos)
            
    df_characters = create_matrix_caracters_text(
            document_root = book_xml,
            namespaces_concretos = namespaces_concretos,
            xpaths = xpaths,
            )
    df_text_parts = create_matrix_text_parts(
            text_parts = text_parts,
            namespaces_concretos = namespaces_concretos,
            )

    string_xpath = xpath2string(xpaths)
    
    df_binary_matrix = create_binary_matrix(df_characters, df_text_parts, xpaths, text_parts, namespaces_concretos, border)

    df_binary_matrix.to_csv(output+inputtei_name+"_"+book+string_xpath+'_matrix.csv', sep='\t', encoding='utf-8')

    edges_text_unit = create_edges2(df_binary_matrix, edge = "text_unit")
 
    #edges_character = create_edges(df_binary_matrix, edge = "character")

    edges_text_unit.to_csv(output+inputtei_name+"_"+book+string_xpath+'_edges_text-unit.csv', sep='\t', encoding='utf-8')
    #edges_character.to_csv(output+inputtei_name+"_"+book+string_xpath+'_edges_character.csv', sep='\t', encoding='utf-8')
    df_characters.to_csv(output+inputtei_name+"_"+book+string_xpath+'_nodes_characters.csv', sep='\t', encoding='utf-8')
    df_text_parts.to_csv(output+inputtei_name+"_"+book+string_xpath+'_nodes_text-parts.csv', sep='\t', encoding='utf-8')

    return df_characters, edges_text_unit, df_text_parts


def convert_attributes_to_colors(nodes):
    nodes["color"] = 1
    nodes.loc[nodes["Gender"] == "none", "color"] = 1
    nodes.loc[nodes["Gender"] == "male", "color"] = 2
    nodes.loc[nodes["Gender"] == "female", "color"] = 3
    nodes.loc[nodes["id"].isin(["#per1","#per14","#per17"]), "color"] = 4
    nodes.loc[nodes["type"] == "group", "color"] = 5
    nodes.loc[nodes["type"] == "place", "color"] = 6
    return nodes

def visualize_networks(input_folder, input_sfolder, edges_df, xpaths, file_nodes, columns_nodes, output_folder, book,  mode, columns_edges = ["Source","Target",'Weight','Type'], language = "sp", entities_type = ["person","group"], dpi = 300):

    print(edges_df.head())
    # TODO: Pasar categorías que filtra
    # TODO: Asignar colores usando género, tipo y naturaleza
    string_xpath = xpath2string(xpaths)

    file_edges_name = output_folder + book + string_xpath

    edges_df2 = edges_df.copy()
    edges_df2["Weight"] = (np.log(edges_df2["Weight"])*3)+1

    entities_edges = sorted(list(set(edges_df2["Target"].tolist() + edges_df2["Source"].tolist())))
    nodes = pd.ExcelFile(input_folder + file_nodes,  index_col=0)
    nodes = nodes.parse('Sheet1').fillna("")
    
    nodes = convert_attributes_to_colors(nodes)

    wrong_entities = [entity for entity in entities_edges if entity not in nodes["id"].tolist() ]
    if wrong_entities:
        print("id erróneos: \n ===================\n", wrong_entities,"\n ===================\n")
    else:
        print("todos ids correctos!")

    nodes = nodes[nodes['id'].isin(entities_edges)]
    print(nodes.head())
    if mode == "directed":
        graph = nx.from_pandas_edgelist(df = edges_df2, source = columns_edges[0], target = columns_edges[1], edge_attr = columns_edges[2:] , create_using = nx.MultiDiGraph())
    else:
        graph = nx.from_pandas_edgelist(df = edges_df2, source = columns_edges[0], target = columns_edges[1], edge_attr = columns_edges[2:])
        
    degree_dc = dict(nx.degree(graph))

    nx.set_node_attributes(G = graph, name = 'NormalizedName-sp', values = {k:v for (k,v) in zip(nodes["id"], nodes["NormalizedName-sp"])})
    nx.set_node_attributes(G = graph, name =  'NormalizedName-ge', values =  {k:v for (k,v) in zip(nodes["id"], nodes["NormalizedName-ge"])})
    nx.set_node_attributes(G = graph, name =  'Gender', values =  {k:v for (k,v) in zip(nodes["id"], nodes["Gender"])})
    nx.set_node_attributes(G = graph, name =  'type', values =  {k:v for (k,v) in zip(nodes["id"], nodes["type"])})

    nx.set_node_attributes(G = graph, name =  'color', values =  {k:v for (k,v) in zip(nodes["id"], nodes["color"])})

    nx.set_node_attributes(G = graph,  name = 'Degree', values =  {k:(int(v)*100) for (k,v) in degree_dc.items()})

    graph = graph.subgraph( [n for n,attrdict in graph.node.items() if attrdict['type'] in (entities_type)] )

    print( graph.nodes(data=True), type(graph.nodes(data=True)),)
    
    #print( graph.nodes(data=True)[:3], type(graph.nodes(data=True)),)
    labels = nx.get_node_attributes(graph,'NormalizedName-'+language)
    
    nodes = graph.nodes()

    colors = [color for n in nodes for color in [graph.node[n]['color']] ]
    
    print(colors[0:20])
    
    
    degree = [[graph.node[n]['Degree']] for n in nodes]

    print("cantidad nodos: ", len(graph.nodes()))
    plt.figure(figsize=((len(graph.nodes())/10)+10,(len(graph.nodes())/10)+10))
    plt.axis('off')
    pos = nx.spring_layout(graph, k=2, iterations=200)


    widths = [w['Weight'] for (u, v, w) in graph.edges(data=True)]
    
    if mode == "directed":
        nx.draw_networkx_labels(graph, pos, labels = labels, font_size = 15+(len(graph.nodes())/25), arrows= True, alpha = 0.6)
    else:
        nx.draw_networkx_labels(graph, pos, labels = labels, font_size = 15+(len(graph.nodes())/25), alpha=0.6)

    nx.draw_networkx_edges(graph, pos, edge_color = '#87CEFA', width = widths, alpha = 0.4)
    
    nx.draw_networkx_nodes(graph, pos, alpha = 0.55, node_color = colors, cmap = plt.cm.tab10,  style = "solid", node_size = degree)

    if book in ["Bible"]:
        dpi = 50

    nx.write_gexf(graph, path = output_folder + book + string_xpath + "-".join(entities_type) + ".gexf")


    plt.title(mode[0].upper()+mode[1:] +  " Network of " + book + (" (" +  ",".join(entities_type) +")"))
    
    plt.savefig( file_edges_name + "-".join(entities_type) + '.png', dpi = dpi)

    plt.show()


  
def create_networks_bible( mode = "directed", xpaths = {"q" : ["@who", "@toWhom", "@type"]},
                          books_bible = ['HEB','RUT','1SA', '2SA','GEN','EXO','PSA','JON','MIC','NAH','HAB','ZEP','HAG','ZEC','MAL','MAT','JOH','ACT','REV','1JO','2JO','3JO','JUD', "JOB", "JAM", "1PE", "2PE", "EZE", "ECC","ROM","1CO","2CO","JOS","MAR","LUK","DAN","HOS","JDG","OBA","JOE","PHM","NEH","EZR","1TI", "2TI", "TIT","JER","PHI","AMO","LEV","LAM","GAL","1KI","1TH","2TH","ISA","EPH","2KI","EST","NUM","Bible"],
                          border = "ab[@type='verse']" , concatenate = False):
    
        
    for book in books_bible:
        print(book)
        if mode == "undirected":
            df_characters, edges_text_unit, df_text_parts = create_undirected_network(
                    inputtei = "/home/jose/Dropbox/biblia/tb/",
                    file = "TEIBible", # "*.xml"
                    output = "/home/jose/Dropbox/biblia/tb/resulting data/",
                    border = border,
                    book = book,
                    characters_in = "text",
                    xpaths = xpaths
                    )
            edges_df = edges_text_unit
                
        elif mode == "directed":
             edges_directed = create_directed_network(
                    inputtei = "/home/jose/Dropbox/biblia/tb/",
                    file = "TEIBible", # "*.xml"
                    output = "/home/jose/Dropbox/biblia/tb/resulting data/",
                    book = book,
                    xpaths = xpaths
                    )
             edges_df = edges_directed            
        graph = visualize_networks(
                           input_folder = "/home/jose/Dropbox/biblia/tb/",
                           edges_df = edges_df,
                           input_sfolder = "/home/jose/Dropbox/biblia/tb/resulting data/",
                           file_nodes = "entities.xls",
                           output_folder = "/home/jose/Dropbox/biblia/tb/visualizations/networks/",
                           columns_nodes = "",
                           book = book,
                           mode = mode,
                           xpaths = xpaths,
                           language = "sp",
                           )
        if 'edges_concatente' not in locals() and concatenate == True:
            edges_concatente = edges_df.copy()
            edges_concatente["book"] = book
        elif  'edges_concatente' in locals() and  concatenate == True:
            edges_df["book"] = book
            edges_concatente = pd.concat([edges_concatente,edges_df])
        else:
            pass
    if  concatenate == True:
        edges_concatente = edges_concatente.sort_values(by="Weight", ascending=False)
        edges_concatente.to_csv("/home/jose/Dropbox/biblia/tb/resulting data/"+"-".join(books_bible)+".csv", sep="\t")

        graph = visualize_networks(
                           input_folder = "/home/jose/Dropbox/biblia/tb/",
                           edges_df = edges_concatente,
                           input_sfolder = "",
                           file_nodes = "entities.xls",
                           output_folder = "/home/jose/Dropbox/biblia/tb/visualizations/networks/",
                           columns_nodes = "",
                           book = ", ".join(books_bible),
                           mode = mode,
                           xpaths = xpaths,
                           language = "sp",
                           )

    return graph


#create_networks_bible(mode = "directed", xpaths = {"q" : ["@who", "@toWhom","@type"]}, books_bible = ['NUM'])

#create_networks_bible(mode = "undirected", xpaths = {"q" : ["@who", "@toWhom"], "rs" : ["@key"]} , books_bible = ['NUM'])

#create_networks_bible(books_bible = ['Bible'])
create_networks_bible(mode = "undirected", xpaths = {"q" : ["@who", "@toWhom"], "rs" : ["@key"]} , books_bible = ["Bible"])

# TODO: Generalizar la función de undirected para que también se puedan crear networks de coaparición en un mismo sustantivo
# TODO: Crear una función para hacer varios tipos de grafos (filtrando lugares, organizaciones, seres superiores...)


