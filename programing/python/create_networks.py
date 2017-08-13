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


    list_characters = [
    list(set(documento_root.xpath("//tei:"+element+"/"+attribute, namespaces=namespaces_concretos)))
    for element, attributes in xpaths.items()
    for attribute in attributes
    ]
    list_characters = list(set([character for sublist in list_characters for item in sublist for character in item.split(" ")]))


    df_characters = pd.DataFrame(list_characters, columns=["id"])
    print(sorted(df_characters["id"].tolist()))

    print(df_characters)
    print("nodes from text done: ", df_characters.shape)
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
    print("text parts done: ", df_text_parts.shape)
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
        #print(text_part)
        for character in df_binary_matrix.index.tolist():
            #print(character)
            
            
            amount_character = sum([
            len(documento_root.xpath('//tei:'+border+'[@xml:id="'+text_part+'"]//tei:'+element+'['+attribute+'="'+character+'"]', namespaces=namespaces_concretos))
            for element, attributes in xpaths.items()
            for attribute in attributes
            ])
            
            df_binary_matrix[text_part][character] = amount_character
            #print(text_part, character, amount_character)
            # Rellenamos la tabla con el valor
    # Creamos una columna sumatorio, ordenamos por ese valor y borramos la columna
    df_binary_matrix["sum"] = df_binary_matrix.sum(axis="columns")
    df_binary_matrix = df_binary_matrix.sort_values(by=["sum"], ascending=False)
    del df_binary_matrix["sum"]

    print(df_binary_matrix)
    print("binary matrix done: ", df_binary_matrix.shape)
    return df_binary_matrix
    

def create_binary_matrix2(df_characters, df_text_parts, xpaths, text_parts, namespaces_concretos, border):
    # Creamos dataframe vacía donde el índice son los personajes y las columnas las escenas
    df_binary_matrix = pd.DataFrame(0, index = df_characters["id"].tolist(), columns = df_text_parts["id"].tolist())
    #print(df_binary_matrix)
    # Miramos cada verso
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

    # TODO: Pasar esto a List comprehension

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
    print(edge, "edges done: ", df_edges.shape)
    
    return df_edges


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

        string_xpath = xpath2string(xpaths)
        
        df_binary_matrix = create_binary_matrix2(df_characters, df_text_parts, xpaths, text_parts, namespaces_concretos, border)

        df_binary_matrix.to_csv(output+inputtei_name+"_"+book+string_xpath+'_matrix.csv', sep='\t', encoding='utf-8')

        edges_text_unit = create_edges2(df_binary_matrix, edge = "text_unit")
 
        #edges_character = create_edges(df_binary_matrix, edge = "character")

        edges_text_unit.to_csv(output+inputtei_name+"_"+book+string_xpath+'_edges_text-unit.csv', sep='\t', encoding='utf-8')
        #edges_character.to_csv(output+inputtei_name+"_"+book+string_xpath+'_edges_character.csv', sep='\t', encoding='utf-8')
        df_characters.to_csv(output+inputtei_name+"_"+book+string_xpath+'_nodes_characters.csv', sep='\t', encoding='utf-8')
        df_text_parts.to_csv(output+inputtei_name+"_"+book+string_xpath+'_nodes_text-parts.csv', sep='\t', encoding='utf-8')

        return df_characters, edges_text_unit, df_text_parts


def visualize_networks(input_folder, file_edges, file_nodes, columns_nodes, output_folder, columns_edges = ["Source","Target",'Weight','Type']):

    # TODO: Pasar categorías que filtra
    # TODO: Asignar colores usando género, tipo y naturaleza

    edges = pd.read_csv(input_folder+file_edges, encoding="utf-8", sep="\t")
    file_edges_name = os.path.splitext(file_edges)[0]
  
    entities_edges = sorted(list(set(edges["Target"].tolist() + edges["Source"].tolist())))
    nodes = pd.read_csv(input_folder+file_nodes, encoding="utf-8", sep="\t")
    #print(sorted(entities_edges))
    wrong_entities = [entity for entity in entities_edges if entity not in nodes["id"].tolist() ]
    if wrong_entities:
        print("id erróneos: \n ===================\n", wrong_entities,"\n ===================\n")
    else:
        print("todos ids correctos!")

    nodes = nodes[nodes['id'].isin(entities_edges)]
    graph = nx.from_pandas_dataframe(df = edges, source = columns_edges[0], target = columns_edges[1], edge_attr = columns_edges[2:] )

    d = nx.degree(graph)


    nx.set_node_attributes(graph, 'NormalizedName-sp', {k:v for (k,v) in zip(nodes["id"], nodes["NormalizedName-sp"])})
    nx.set_node_attributes(graph, 'Gender', {k:v for (k,v) in zip(nodes["id"], nodes["Gender"])})
    nx.set_node_attributes(graph, 'type', {k:v for (k,v) in zip(nodes["id"], nodes["type"])})

    nx.set_node_attributes(graph, 'Degree', {k:(int(v)*100) for (k,v) in d.items()})

    graph = graph.subgraph( [n for n,attrdict in graph.node.items() if attrdict['type'] == 'person'] )

    
    print( graph.nodes(data=True), type(graph.nodes(data=True)),)
    
    #print( graph.nodes(data=True)[:3], type(graph.nodes(data=True)),)
    labels = nx.get_node_attributes(graph,'NormalizedName-sp')
    
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
    
    nx.draw_networkx(graph, pos, labels = labels, width = widths, font_size=15+(len(graph.nodes())/25), alpha=0.4, edge_color='#87CEFA', node_color=colors, cmap=plt.cm.RdYlBu, style= "solid", node_size = degree)

    plt.savefig(output_folder+file_edges_name+'.png', dpi=50)
    #print(d)
    #print(nx.nodes(graph))

    #plt.show()
    
def create_networks_bible():
    xpaths = {"rs" : ["@key"], "q" : ["@who", "@corresp"]}
    
    string_xpath = xpath2string(xpaths)
    books_bible = ['GEN','EXO','RUT','1SA', 'PSA','JON','MIC','NAH','HAB','ZEP','HAG','ZEC','MAL','MAT','JOH','ACT','REV','1JO','2JO','3JO','JUD', "JOB", "JAM", "1PE", "2PE", "EZE", ]
    books_bible = ["EZE"]
    
    for different_book in books_bible:

        df_characters, edges_text_unit, df_text_parts = create_networks(
                inputtei = "/home/jose/Dropbox/biblia/tb/",
                file = "TEIBible", # "*.xml"
                output = "/home/jose/Dropbox/biblia/tb/resulting data/",
                border = "ab[@type='verse']",
                book = different_book,
                deleting_books = True,
                characters_in = "text",
                xpaths = xpaths
                )
        graph = visualize_networks( input_folder = "/home/jose/Dropbox/biblia/tb/resulting data/",
                           file_edges = "TEIBible_"+different_book+string_xpath+"_edges_text-unit.csv",
                           file_nodes = "ontology.csv",
                           output_folder = "/home/jose/Dropbox/biblia/tb/visualizations/networks/",
                           columns_nodes = ""
                           )
    return

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

