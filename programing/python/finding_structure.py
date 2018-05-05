# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import pandas as pd
import re
import glob
import os
from collections import Counter


communication_verbs = "()"

def finding_standard_rs(content):
    """
        It searchs for textual patterns that matchs things like names
    """
    nombres_comunes = {
        "pla" : ["ciudad","ciudades","lugares","mar", "río", "aldeas","provincia","región","monte","territorio","valle"],
        "per" : ["amo","amos","capitán","capitanes","esclavo","esclavos","esclava","esclavas","espías?","espía","faraón","huesped","huespedes","jefe","jefes","joven","jovenes","juez","madre","madres","mujer","niño","niños","padre","padres","pastor","pastores","primogénito","primogénitos","reina","reinas","señor","señores","varón","varones","hijo","hija","siervo","sierva","marido","maridos","nuera","nueras","pariente","criado","criados","suegra","criadas","criada","profeta","gobernador","apóstol"],
        "org" : ["autoridad","descendencia","descendencias","familia","familias","hijos","hijas","pueblos","siervas","tribu","tribus","soldados"],
    }

    for key,values in nombres_comunes.items():
        for value in values:
            content = re.sub(r'(\W)(' + re.escape(value)+r')(\W)', r'\1<rs key="' + re.escape(key)+r'">\2</rs>\3', content)
    
    variaciones_comunes = {
        "per14" : ["Jehová","Todopoderoso","Señor","Padre","Omnipotente","Hacedor","Redentor","Creador","Altísimo"],
        "per1" : ["Cristo","Jesucristo","Hijo","Mesías"],
        "per20" : ["Satanás"],
        "per17" : ["Espíritu"],
        "org0" : ["hombres", "hombre", "naciones", "pueblos","mundo","hijos de los hombres", "persona"],
        "org70" : ["pueblo", "hijos de Israel", "cas de Israel"],
        "org131" : ["siervos"],
        "org19" : ["necio", "impío","impíos"],
        "org18" : ["sabio", "justo","justos"],
        "org24" : ["ejército",],
        "org37" : ["hermanos","hermano"],
        "org4" : ["ángeles",],
        "org101" : ["enemigo",],
        "org18" : ["santos",],
        "org100" : ["reyes","rey"],
        "pla30" : ["Templo"],
        "wor1" : ["Ley"],

    }
    for key,values in variaciones_comunes.items():
        for value in values:
            content = re.sub(r'(\W)(' + re.escape(value)+r')(\W)', r'\1<rs key="' + re.escape(key)+r'">\2</rs>\3', content)

    content = re.sub(r'([a-zá-úñüç,;>] )([A-ZÁ-ÚÜÑ][a-zá-úñüç-]+)([^a-zá-úñüç])', r'\1<rs key="per">\2</rs>\3', content)
    
    return content


def finding_rs_from_ontology(content, df, book):
    # It goes row by row
    #print(book)
    for index, row in df.iterrows():
        #print(row["NormalizedName-sp"])
        if (row["type"] == "person" and row["importance"] == 1) or (row["type"] == "group") or (row["type"] == "place") or (row["type"] == "time") or (row["order-edition"] == book) or (row["order-edition"] == "NEH") :
            content = re.sub(r'(\W)('+ re.escape(row["NormalizedName-sp"]) +r')(\W)', r'\1<rs key="'+row["id"]+r'">\2</rs>\3', content, flags=re.DOTALL|re.MULTILINE|re.UNICODE)
        if (row["type"] == "group") & (row["variants"] != ""):
            content = re.sub(r'(\W)('+ re.escape(row["variants"]) +r')(\W)', r'\1<rs key="'+row["id"]+r'">\2</rs>\3', content, flags=re.DOTALL|re.MULTILINE|re.UNICODE)
    return content
        
def improve_struccture(content):
    
    # Intentamos encontrar el identificador de cosas como su "mujer Noemí":
    content = re.sub(r'(<rs key=")per(">[^<]*?</rs> <rs key=\"([^\"]*?)\">)', r'\1\3\2', content)
    content = re.sub(r'(<rs key=\"([^\"]*?)\">[^>]*</rs>)(, <rs key=")per', r'\1\3\2', content)
    
    # Colocamos los numeradores dentro del rs
    content = re.sub(r'(\W)(dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce)(\W)(<rs [^>]*?>)', r'\1\4\2\3', content)

    # Intentamos encontrar el identificador de cosas como su mujer Noemí:
    content = re.sub(r'(</rs>)( de | de la | del | en | en el | en la | de su )(<rs .*?>.*?</rs>)', r'\2\3\1', content)
    content = re.sub(r'(</rs>)( de | de la | del | en | en el | en la | de su )(<rs .*?>.*?</rs>)', r'\2\3\1', content)
    content = re.sub(r'(</rs>)( de | de la | del | en | en el | en la | de su )(<rs .*?>.*?</rs>)', r'\2\3\1', content)

    
    return content
    
def findingq(text, genre):
    """
        It decodes the HTML entities and it deletes some anoying characters
        finq = finq(
        "/home/jose/Dropbox/biblia/tb/genesis0.xml",
        "/home/jose/Dropbox/biblia/tb/programing/python/output/"
        )

    """

    text = re.sub(r'((dij|insist|pregunt|respond|exclam|diciendo|decir|decía|diciéndo|Dijo|dije|Dije).*?: )(((?!<q).)*)(</ab>)', r'\1<q who="per" corresp="per" type="oral">\3</q>\5', text)

    text = re.sub(r'xml:id', r'xml_id', text)
    text = re.sub(r'http:', r'http_', text)

    text = re.sub(r'(<ab [^>]*?>)((((?!<q).)*)(»|«).+?)(</ab>)', r'\1<q who="per" corresp="per" type="oral">\2</q>\6', text)

    if genre != "letter":
        text = re.sub(r'(<ab [^>]*?>)((((?!<q).)*)[^\w](yo|tú|me|soy|te|estoy|he|tengo|tienes|eres|estás|has|ti|mí|mi|tu|os)[^\w].+?)(</ab>)', r'\1<q who="per" corresp="per" type="oral">\2</q>\6', text)

    text = re.sub(r'_', r':', text, flags=re.MULTILINE)

    return text
    
def values_q(content):

    # Intentamos recoger cosas como "Rut dijo a Noemí: "
    # No sé si funciona!
    content= re.sub(r'(<rs key="(#?(?:per|org)\d+)">.*?</rs>[^<]*?<rs key="(#?(?:per|org)\d+)">.*?</rs>.*?)<q who="per" corresp="per" type="oral">', r'\1<q who="\2" corresp="\3" type="oral">', content, flags=re.MULTILINE)

    # Buscamos el rs con identificador completo antes del q y se lo colocamos como valor del atributo who:
    content = re.sub(r'(<rs key="(#?(per|org)\d+)">(((?!<rs key="(#?(per|org)\d+)">).)*))<q who="per" corresp="per" type="oral">', r'\1\5<q who="\2" corresp="per" type="oral">', content)

    # Colocamos el mismo q del versículo anterior en caso de 
    content = re.sub(r'((<q who="#per\d+" corresp=".*?" type="oral">).*?</q></ab>\s+<ab [^>]*?>)<q who="per" corresp="per" type="oral">', r'\1\2', content)


    content = re.sub(r'(<q who=".*?" corresp="per14") type="oral">', r'\1 type="prayer">', content)
    
    return(content)

def find_people_without_id(content, outputtei, bookcode):
    people_without_id = []
    people_without_id = people_without_id + re.findall(r"<rs key=\"per\">([A-Z][^<]*?)</rs>", content)
    print(type(people_without_id))
    people_without_id = Counter(people_without_id)
    for people in people_without_id:
        print((people))

    print(people_without_id, len(people_without_id))
    people_without_id_df = pd.DataFrame(list(people_without_id.items()), columns=['entity','frequency'])

    people_without_id_df = people_without_id_df.sort_values(by='frequency', ascending=False)
    people_without_id_df.to_csv(outputtei+bookcode+"people_without_id.csv", sep='\t', encoding='utf-8')

    #print(people_without_id_df)

    

def deleting_wrong_entities(content, bookcode):
    content = re.sub(r'<rs key="#pla230">Mira</rs>', r'Mira', content)
    content = re.sub(r'<rs key="#pla258">Sin</rs>', r'Sin', content)
    content = re.sub(r'<rs key="#per17"><rs key="per17">Espíritu</rs> <rs key="per">Santo</rs></rs>', r'<rs key="#per17"><rs key="per17">Espíritu Santo</rs>', content)

    content = re.sub(r'"#per5"', r'"#pla2"', content)
    content = re.sub(r'<rs key="org\d*">((hombres|hijos) de <rs key="#pla2">Judá</rs>)</rs>', r'<rs key="#org39">\1</rs>', content)
    content = re.sub(r'<rs key="org\d*">((hombres|hijos) de <rs key="#pla4">Israel</rs>)</rs>', r'<rs key="#org70">\1</rs>', content)
    content = re.sub(r'<rs key="#pla(\d*)">([^ ]*? de )<rs key="(#?pla\d+)"', r'<rs key="\1">\1<rs key="\2"', content)
    
    content = re.sub(r'\A.*?</teiHeader>', r'<?xml version="1.0" encoding="UTF-8"?>\n<?xml-stylesheet type="text/css" href="styles/styles.css" rel="stylesheet" title="Classic"?>\n<?xml-stylesheet type="text/css" href="styles/word2pix-quotes.css" rel="stylesheet" title="Word2Pix Quotations"?>\n<?xml-stylesheet type="text/css" href="styles/word2pix-reference.css" rel="stylesheet" title="Word2Pix References"?>\n<?xml-stylesheet type="text/css" href="styles/word2pix-level-q.css" rel="stylesheet" title="Word2Pix Level Quotation"?><TEI xmlns="http://www.tei-c.org/ns/1.0">\n	<teiHeader>\n		<fileDesc>\n			<titleStmt>\n				<title></title>\n				<title type="idno">\n					<idno type="string">'+bookcode+'</idno>\n					<idno type="viaf"></idno>\n				</title>\n				<author>\n					<name type="short"></name>\n					<name type="full"></name>\n					<idno type="viaf"></idno>\n				</author>\n				<principal key="#jct">José Calvo Tello</principal>\n			</titleStmt>\n			<publicationStmt>\n				<publisher>José Calvo Tello</publisher>\n				<availability status="free">\n					<p>The text is freely available.</p>\n				</availability>\n				<date when="2018">2018</date>\n			</publicationStmt>\n			<sourceDesc>\n				<bibl type="digital-source"><date when="2000">2000</date><idno></idno>.</bibl>\n				<bibl type="print-source">Reina Valera, <date when="1995">1995</date></bibl>\n				<bibl type="edition-first"><date when="1569">1569</date></bibl>\n			</sourceDesc>\n		</fileDesc>\n		<encodingDesc>\n			<p></p>\n		</encodingDesc>\n		<revisionDesc>\n			<change when="2018-02-02" who="#jct">First version of </change>\n		</revisionDesc>\n	</teiHeader>\n', content, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)

    return(content)


def finding_structure(inputcsv, inputtei, outputtei, bookcode, genre = "not-letter"):
    """
    finding_structure = finding_structure("/home/jose/Dropbox/biblia/tb/resulting data/ontology.csv","/home/jose/Dropbox/biblia/tb/programing/python/input/rut.xml", "/home/jose/Dropbox/TEIBibel/programacion/python/output/")
    """
    #Lets open the csv file
    df = pd.read_csv(inputcsv, encoding = "utf-8", sep = "\t")
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
            
            # Buscamos las personas de la ontología
            content = finding_rs_from_ontology(content, df, bookcode)
            
            # Buscamos las personas genéricas
            content = finding_standard_rs(content)
            
            # Intentamos mejorar la estructura de rss
            content = improve_struccture(content)
            
            find_people_without_id(content, outputtei,bookcode)

            content = deleting_wrong_entities(content, bookcode)
            
            # Buscamos estructuras q
            content = findingq(content, genre)
                
            # Intentamos dar valores a los atributos de q
            content = values_q(content)
            
        
            # it cleans the HTML from entities, etc        
            # TODO: introducir función que arregle algunos valores como "<rs key="org">hijos de <rs key="#pla4">Israel</rs></rs>", "<rs key="org">hijos de <rs key="#pla2">Judá</rs></rs>",
            # It writes the result in the output folder
    
            with open (os.path.join(outputtei, docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
            print(i)


finding_structure = finding_structure(
    "/home/jose/Dropbox/biblia/tb/resulting data/ontology.csv",
    "/home/jose/Dropbox/biblia/tb/programing/python/input/EZR.xml",
    "/home/jose/Dropbox/biblia/tb/programing/python/output/",
    "EZR",
    genre = "prophetical"
    )
