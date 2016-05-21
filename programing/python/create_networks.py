# -*- coding: utf-8 -*-
"""
This script gets the relationships between entities that appear in the same verse (that means, that they are values of the attribute who, corresp or key of the elements q or rs).

"""

from lxml import etree
import pandas as pd
from collections import Counter


def create_networks(inputtei, output, border, book, subelements, attributes):
    """
    La función toma:
    inputtei: el lugar del tei
    output: el lugar donde debe guardar el csv
    border: el nombre del elemento que consideramos como unidad
    book: la especificación que debe tener el div xml:id (sin b.)
    subelements: los elementos que deben ser tenidos en cuenta de donde rescatar los valores
    attributes: los atributos que deben ser tenidos en cuenta de donde sacar los valores
    
    Ejemplo de como usarlo:
    
    create_networks(
        inputtei = "/home/jose/Dropbox/biblia/tb/TEIBible.xml", 
        output = "/home/jose/Dropbox/biblia/tb/programing/python/output/",
        border = "ab",
        book = "GEN",
        subelements = ["q","rs"],
        attributes = ["who","corresp","key"],
        )
    """
    # Una lista vacía es creada para guardar las relaciones de personajes
    networks = []
    # Parseamos el archivo xml-tei
    documento_xml = etree.parse(inputtei)

    # Y lo convertimos en un tipo element
    documento_root = documento_xml.getroot()
    #print(type(documento_root))

    # Definimos el namespace del TEI con el que trabajamos
    namespaces_concretos = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}

    # Borramos todos los libros que no sean el que hemos señalado
    # Intenté hacerlo de manera positiva (es decir, solo seleccionar lo que quería), pero parecía que no borraba del todo el resto de libros y no entendía el funcionamiento realmente
    for non_wanted_book in documento_root.xpath('//tei:div[@type="book"][not(@xml:id="b.'+book+'")]', namespaces=namespaces_concretos):
        non_wanted_book.getparent().remove(non_wanted_book)

    # Hacemos una lista de aquellas unidades que hemos seleccionado
    basic_unities = documento_root.xpath('//tei:'+border+'', namespaces=namespaces_concretos) 
    #print(len(basic_unities))


    # Creamos una cadena para usarla como xpath con los elementos que hemos pasado
    unity_xpath = ""
    # Sacamos los elementos de la lista
    for subelement in subelements:
        # Los colocamos con el prefijo del namespace
        unity_xpath = unity_xpath+"|tei:"+subelement    
    # Eliminamos la primera barra
    unity_xpath = unity_xpath[1:]
    #print(unity_xpath )

    # Por cada una de ella
    for unity in basic_unities:
        # Hacemos una lista vacía para los atributos de los elementos inline
        valores_atributos = []

        # Sacamos una lista de los elementos por debajo de la unidad que queremos inspeccionar
        subunities = unity.xpath(unity_xpath, namespaces=namespaces_concretos)
        # Por cada uno de ellos:
        for subunity in subunities:
            
            # Le sacamos los atributos y los ponemos en un diccionario
            atributo = dict(subunity.attrib)
            
            # Le borramos los atributos que no queremos utilizar (por ejemplo cert, type...)
            n_atributo = {k:v for k,v in atributo.items() if any(k == attribute for attribute in attributes) }
            #print(n_atributo)

            # Ponemos todos los valores de una misma unidad en la lista. Es decir, que si por ejemplo en un versículo tenemos diferentes q y rs, en este punto perdemos esa diferenciación
            valores_atributos = valores_atributos + list(n_atributo.values())

        # Debido a que un atributo puede tener diferentes valores seguidos, convertimos la lista en una cadena
        valores_atributos  = ' '.join(valores_atributos)
        # Ahora lo que hacemos es volver a separar los valores en una lista (así ya no hacemos diferencia si los atributos iban en diferentes atributos o como varios valores en un mismo atributo)
        valores_atributos  = valores_atributos.split(' ')

        # La lista la ordenamos para que no haya cosas como per1 per14; per14 per1; además borramos casos repetidos dentro de cada lista, es decir, que si en un versículo aparecía dos veces la misma persona, esa duplicidad se borra
        valores_atributos  = sorted(list(set(valores_atributos)))

        # Hacemos una lista para guardar cada entidad ya vista
        old_entity = []
        # Vamos por iterando por cada valor
        for entity1 in valores_atributos:
            # Y lo ponemos en la lista de entidaddes ya vistas
            old_entity.append(entity1)
            
            #Iteramos de nuevo por las entidades
            for entity2 in valores_atributos:
                # Miramos si la entidad no está ya en la lista
                if entity2 not in old_entity:
                    # Creamos una tuple con esta relación
                    relation = entity1,entity2
                    # Lo añadimos a la lista de relaciones
                    networks.append(relation)
    # Una vez hemos terminado, creamos un counter para ver cuántas veces se repetía cada relación
    networks = Counter(networks)
    #print(type(networks))
    
    # A partir de ese creamos una tabla    
    dfnetworks = pd.DataFrame(list(networks.items()), columns=['entidades','weight'])

    # Dividimos la tuple de entidades en dos columnas diferentes 
    dfnetworks[['source', 'target']] = dfnetworks['entidades'].apply(pd.Series)
    # Y nos cargamos la columna de las tuples de entidades
    dfnetworks = dfnetworks.drop('entidades', 1)
    # Ordenamos la tabla para visualizarla
    dfnetworks = dfnetworks.sort(["weight"], ascending=True)
    print(dfnetworks)

    # La ordenamos de nuevo para ponerla en el csv
    dfnetworks = dfnetworks.sort(["weight"], ascending=False)
    dfnetworks.to_csv(output+book+'-networks-id.csv', sep='\t', encoding='utf-8')
    print("print as: ", output+book+'-networks-id.csv')
