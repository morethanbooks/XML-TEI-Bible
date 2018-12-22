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

def spliting_text(documento_root, border, namespaces_concretos, printing = False):
    # Sacamos todos los números de escenas
    text_parts = documento_root.xpath('//tei:'+border+'', namespaces=namespaces_concretos)

    if printing == True:
        for text_part in text_parts:
            print(etree.tostring(text_part, pretty_print=True, encoding="unicode"))

    return text_parts

def xpath2string(xpaths):
    string_xpath = "_"+"-".join(sorted(list(xpaths.keys())))+"-".join(sorted([item for sublist in list(xpaths.values()) for item in sublist]))+"_"
    return string_xpath


def open_and_clean_tei(inputtei, file, deleting_books, book):

    doc = glob.glob(inputtei+file+".xml")[0]
    inputtei_name  = os.path.splitext(os.path.split(doc)[1])[0]
    print(doc, inputtei_name)

    # Parseamos el archivo xml-tei
    document_xml = etree.parse(doc)

    # Y lo convertimos en un tipo element
    document_root = document_xml.getroot()

    # Definimos el namespace del TEI con el que trabajamos

    if deleting_books == True:
        document_root = delete_books(document_root, book, namespaces_concretos)

    return document_root, inputtei_name

    
 
def create_directed_network(inputtei, file, deleting_books, output, book, xpaths):
    
    document_root, inputtei_name = open_and_clean_tei(inputtei, file, deleting_books, book)


    xpath_element = list(xpaths.keys())[0]
    
    xpath_source = list(xpaths.values())[0][0]
    xpath_target = list(xpaths.values())[0][1]
    xpath_type = list(xpaths.values())[0][2]
    
    print(xpath_source,xpath_target,xpath_type)

    communication_list = []    

    for element in document_root.xpath('.//tei:div[@type="book"][@xml:id="b.' + book + '"]//tei:' + xpath_element +"[@type]", namespaces=namespaces_concretos):
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
    print()

    return edges_df




def create_undirected_network(inputtei, file, output, border, book, deleting_books, characters_in, xpaths):
    
    document_root, inputtei_name = open_and_clean_tei(inputtei, file, deleting_books, book)

    text_parts = spliting_text(document_root, border, namespaces_concretos)
            
    df_characters = create_matrix_caracters_text(
            document_root = document_root,
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


def visualize_networks(input_folder, input_sfolder, edges_df, xpaths, file_nodes, columns_nodes, output_folder, book,  mode, columns_edges = ["Source","Target",'Weight','Type'], language = "sp"):

    print(edges_df)
    # TODO: Pasar categorías que filtra
    # TODO: Asignar colores usando género, tipo y naturaleza
    string_xpath = xpath2string(xpaths)

    file_edges_name = os.path.splitext(output_folder+book+string_xpath+'.csv')[0]

    entities_edges = sorted(list(set(edges_df["Target"].tolist() + edges_df["Source"].tolist())))
    nodes = pd.ExcelFile(input_folder + file_nodes,  index_col=0)
    nodes = nodes.parse('Sheet1').fillna("")
    #print(sorted(entities_edges))
    wrong_entities = [entity for entity in entities_edges if entity not in nodes["id"].tolist() ]
    if wrong_entities:
        print("id erróneos: \n ===================\n", wrong_entities,"\n ===================\n")
    else:
        print("todos ids correctos!")

    nodes = nodes[nodes['id'].isin(entities_edges)]
    graph = nx.from_pandas_edgelist(df = edges_df, source = columns_edges[0], target = columns_edges[1], edge_attr = columns_edges[2:] , create_using = nx.MultiDiGraph())

    d = dict(nx.degree(graph))


    nx.set_node_attributes(G = graph, name = 'NormalizedName-sp', values = {k:v for (k,v) in zip(nodes["id"], nodes["NormalizedName-sp"])})
    nx.set_node_attributes(G = graph, name =  'NormalizedName-ge', values =  {k:v for (k,v) in zip(nodes["id"], nodes["NormalizedName-ge"])})
    nx.set_node_attributes(G = graph, name =  'Gender', values =  {k:v for (k,v) in zip(nodes["id"], nodes["Gender"])})
    nx.set_node_attributes(G = graph, name =  'type', values =  {k:v for (k,v) in zip(nodes["id"], nodes["type"])})

    nx.set_node_attributes(G = graph,  name = 'Degree', values =  {k:(int(v)*100) for (k,v) in d.items()})

    graph = graph.subgraph( [n for n,attrdict in graph.node.items() if attrdict['type'] == 'person'] )

    
    print( graph.nodes(data=True), type(graph.nodes(data=True)),)
    
    #print( graph.nodes(data=True)[:3], type(graph.nodes(data=True)),)
    labels = nx.get_node_attributes(graph,'NormalizedName-'+language)
    
    groups = set(nx.get_node_attributes(graph,'Gender').values())
    mapping = dict(zip(sorted(groups),count()))
    nodes = graph.nodes()
    colors = [mapping[graph.node[n]['Gender']] for n in nodes]
    
    degree = [[graph.node[n]['Degree']] for n in nodes]

    print("cantidad nodos: ", len(graph.nodes()))
    plt.figure(figsize=((len(graph.nodes())/10)+10,(len(graph.nodes())/10)+10))
    plt.axis('off')
    pos = nx.spring_layout(graph, k = 0.9)


    widths = [w['Weight'] for (u, v, w) in graph.edges(data=True)]
    
    #nx.draw(graph, pos)
    nx.draw_networkx_labels(graph,pos,labels = labels,font_size=15+(len(graph.nodes())/25),arrows= True )
    nx.draw_networkx_edges(graph, pos, edge_color='#87CEFA', width = widths, )
    nx.draw_networkx_nodes(graph, pos, 
                           alpha=0.55, node_color=colors, cmap=plt.cm.RdYlBu,  style= "solid",node_size = degree)
    nx.write_gexf(graph, path = output_folder + book + ".gexf")

    plt.savefig( file_edges_name + '.png', dpi=50)
    #print(d)
    #print(nx.nodes(graph))

    #plt.show()


  
def create_networks_bible(mode = "directed"):
    xpaths = {"rs" : ["@key"], "q" : ["@who", "@toWhom"]}
    xpaths = {"q" : ["@who", "@toWhom", "@type"]}
    
    string_xpath = xpath2string(xpaths)
    books_bible = ['GEN','EXO','RUT','1SA', 'PSA','JON','MIC','NAH','HAB','ZEP','HAG','ZEC','MAL','MAT','JOH','ACT','REV','1JO','2JO','3JO','JUD', "JOB", "JAM", "1PE", "2PE", "EZE", "ECC","ROM","1CO","2CO","JOS","MAR","LUK","DAN","HOS","JDG","OBA","JOE","PHM","NEH","EZR","1TI", "2TI", "TIT","JER","PHI","AMO","LEV","LAM","GAL","1KI","1TH","2TH"]
    books_bible = ["EXO"]
    
    # seleccionamos si trabajamos con la biblia o libros
    # seleccionamos si trabajamos direccional o no
        # seleccionamos el xpath
            # creamos un dataframe dependiendo del tipo
            # sacamos los edges
    
    for book in books_bible:

        if mode == "undirected":
            df_characters, edges_text_unit, df_text_parts = create_undirected_network(
                    inputtei = "/home/jose/Dropbox/biblia/tb/",
                    file = "TEIBible", # "*.xml"
                    output = "/home/jose/Dropbox/biblia/tb/resulting data/",
                    border = "ab[@type='verse']",
                    book = book,
                    deleting_books = True,
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
                    deleting_books = True,
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
    return graph

create_networks_bible()



"""
df_characters, edges_text_unit, df_text_parts = create_networks(
        inputtei = "/home/jose/Dropbox/biblia/tb/",
        file = "TEIBible", # "*.xml"
        output = "/home/jose/Dropbox/biblia/tb/resulting data/",
        border = "ab[@type='verse']",
        book = "JOB", #JOB JON GEN EXO RUT PSA JON MIC NAH HAB ZEP HAG ZEC MAL MAT JOH ACT REV 
        deleting_books = True,
        characters_in = "text",
        xpaths = {"rs" : ["@key"], "q" : ["@who", "@corresp"]}
        )

graph = visualize_networks( input_folder = "/home/jose/Dropbox/biblia/tb/resulting data/",
                   file_edges = "TEIBible_ACT_q-rs@corresp-@key-@who__edges_text-unit.csv",
                   file_nodes = "ontology.csv",
                   output_folder = "/home/jose/Dropbox/biblia/tb/visualizations/",
                   columns_nodes = ""
                   )
"""
# TODO: Crear una función para hacer varios tipos de grafos (filtrando lugares, organizaciones, seres superiores...)

# TODO: Crear función para hacer varios tipos de grafos de todos los libros que ya tengo

