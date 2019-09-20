"""
Spyder Editor

"""
import pandas as pd
import re
import glob
import os
from collections import Counter


communication_verbs = "()"

def finding_common_rs(content):
    """
        It searchs for textual patterns that matchs things like names
    """
    nombres_comunes = {
        "pla" : ["ciudad","ciudades","lugares","mar", "río", "aldeas","provincia","región","monte","territorio","valle","regiones"],
        "per" : ["amo","amos","capitán","capitanes","esclavo","esclavos","esclava","esclavas","espías?","espía","faraón","huesped","huespedes","jefe","jefes","joven","jovenes","juez","madre","madres","mujer","niño","niños","pastor","pastores","primogénito","primogénitos","reina","reinas","señores","varón","varones","siervo","sierva","marido","maridos","nuera","nueras","pariente","criado","criados","suegra","criadas","criada","profeta","gobernador","apóstol"],
        "org" : ["hijos","descendientes","autoridad","descendencia","descendencias","familia","familias","hijos","hijas","pueblos","siervas","tribu","tribus","soldados"],
    }

    for key,values in nombres_comunes.items():
        for value in values:
            content = re.sub(r'(\W)(' + re.escape(value)+r')(\W)', r'\1<rs key="' + re.escape(key)+r'">\2</rs>\3', content)
    """
    variaciones_comunes = {
        "per14" : ["Jehová","Todopoderoso","Señor","Padre","Omnipotente","Hacedor","Redentor","Creador","Altísimo","Soberano"],
        "per1" : ["Cristo","Jesucristo","Hijo","Mesías","Salvador"],
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
    """
    return content

def finding_proper_rs(content):

    content = re.sub(r'([a-zá-úñüç,;>] )([A-ZÁ-ÚÜÑ][a-zá-úñüç-]+)([^a-zá-úñüç])', r'\1<rs key="per">\2</rs>\3', content)
    
    return content


def finding_rs_from_ontology(content, df, book, books_list):
    # It goes row by row
    #print(book)
    for index, row in df.iterrows():
        print(row["NormalizedName-sp"])

        if (row["type"] == "person" and row["importance"] == 1) or (row["type"] == "group") or (row["type"] == "place") or (row["type"] == "time") or (row["order-edition"] == book) or ((row["order-edition"] in books_list)):# or (row["book"] in ["NT"]):
            content = re.sub(r'<rs key="per">('+ re.escape(row["NormalizedName-sp"]) +r')</rs>', r'<rs key="'+row["id"]+r'">\1</rs>', content, flags=re.DOTALL|re.MULTILINE|re.UNICODE)

        if (row["type"] == "group") & (row["variants"] != ""):
            content = re.sub(r'(\W)('+ re.escape(row["variants"]) +r')(\W)', r'\1<rs key="'+row["id"]+r'">\2</rs>\3', content, flags=re.DOTALL|re.MULTILINE|re.UNICODE)

        if (row["type"] == "group") :
            content = re.sub(r'<rs key="#org">('+ re.escape(row["NormalizedName-sp"]) +r')</rs>', r'<rs key="'+row["id"]+r'">\1</rs>', content, flags=re.DOTALL|re.MULTILINE|re.UNICODE)
    
    return content
        
def improve_structure(content):
    
    # Intentamos encontrar el identificador de cosas como su "mujer Noemí":
    #content = re.sub(r'(<rs key=")per(">[^<]*?</rs> <rs key=\"([^\"]*?)\">)', r'\1\3\2', content)
    #content = re.sub(r'(<rs key=\"([^\"]*?)\">[^>]*</rs>)(, <rs key=")per', r'\1\3\2', content)
    
    #content = re.sub(r'Jehová', r': <rs key="#per14">Jehová</rs>.', content)
    #content = re.sub(r'Ley', r': <rs key="#wor1">Ley</rs>.', content)
    # Colocamos los numeradores dentro del rs
    content = re.sub(r'(\W)(dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|quince|dicieseis|diecisiete|dicieocho|diecinueve|veinte|treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|noventa|cien|ciento|quinientos|mil|miles|\d+\.?\d*)+(\W)(<rs [^>]*?>)', r'\1\4\2\3', content)


    # 
    content = re.sub(r'(</rs>)( de | de la | del | en | en el | en la | de su )(<rs .*?>.*?</rs>)', r'\2\3\1', content)
    content = re.sub(r'(</rs>)( de | de la | del | en | en el | en la | de su )(<rs .*?>.*?</rs>)', r'\2\3\1', content)
    content = re.sub(r'(</rs>)( de | de la | del | en | en el | en la | de su )(<rs .*?>.*?</rs>)', r'\2\3\1', content)

    content = re.sub(r'<rs key="(#per[^"]*?)">([^>]*?)</rs> <rs key="#per\d*">([a-z])', r'<rs key="\1">\2</rs> <rs key="\1">\3', content)
    
    """

    para números

    content = re.sub(r': (\d+\.?\d*)+\.', r': <rs key="#org70">\1</rs>.', content)
    
    content = re.sub(r'<rs key="#org">familia de los <rs key="(.*?)">(.*?)</rs></rs>', r'<rs key="\1">familia de los <rs key="\1">\2</rs></rs>', content)
    

    content = re.sub(r'<rs key="#org22">(tribu de.*?)</rs>', r'\1', content)

    content = re.sub(r'<rs key="#pla4">', r'<rs key="#org70">', content)

    content = re.sub(r'<rs key="#org0">', r'<rs key="#org70">', content)

    content = re.sub(r'<rs key="#(per|pla)\d*"><rs key="(#org\d+)">([^<]+?)</rs></rs>', r'<rs key="\2">\3</rs>', content)
            
    content = re.sub(r'<rs key="#org(.*?)">tribu de <rs key="(#org\d+)">', r'<rs key="\2">tribu de <rs key="\2">', content)
    
    content = re.sub(r'<rs key="#org44">tribu de <rs key="#org44">Manasés</rs></rs></rs>', r'<rs key="#org44">tribu de <rs key="#org44">Manasés</rs></rs>', content)
     
    content = re.sub(r'Hijos y descendientes de <rs key="(#org\d+)">(.*?)</rs>', r'<rs key="\1">Hijos</rs> y <rs key="\1">descendientes de <rs key="\1">\2</rs></rs>', content)

    content = re.sub(r' tribu de <rs key="(#org\d+)">(.*?)</rs>', r' <rs key="\1">tribu de <rs key="\1">\2</rs></rs>', content)

    content = re.sub(r' jefe ', r' <rs key="#org25">jefe</rs>', content)

    content = re.sub(r' varones ', r' <rs key="#org70">varones</rs> ', content)
     
    content = re.sub(r' casas ', r' <rs key="#org22">casa</rs> ', content)
     
    content = re.sub(r'<rs key="(#org\d+)"><rs key="#org70">hijos de <rs key=".*?">(.*?)</rs></rs></rs>', r'<rs key="\1">hijos de <rs key="\1">\2</rs></rs>', content)
    """

    return content
    
def findingq(text, genre):
    """
        It decodes the HTML entities and it deletes some anoying characters
        finq = finq(
        "/home/jose/Dropbox/biblia/tb/genesis0.xml",
        "/home/jose/Dropbox/biblia/tb/programing/python/output/"
        )

    """

    text = re.sub(r'((dij|insist|pregunt|respond|exclam|diciendo|decir|decía|diciéndo|Dijo|dije|Dije).*?: )(((?!<q).)*)(</ab>)', r'\1<q who="per" toWhom="per" type="oral">\3</q>\5', text)

    text = re.sub(r'xml:id', r'xml_id', text)
    text = re.sub(r'http:', r'http_', text)

    text = re.sub(r'(<ab [^>]*?>)((((?!<q).)*)(»|«).+?)(</ab>)', r'\1<q who="per" toWhom="per" type="oral">\2</q>\6', text)

    if genre != "letter":
        text = re.sub(r'(<ab [^>]*?>)((((?!<q).)*)[^\w](yo|tú|me|soy|te|estoy|he|tengo|tienes|eres|estás|has|ti|mí|mi|tu|os|vosotros|haced|tú|[^ ]*?eréis)[^\w].+?)(</ab>)', r'\1<q who="per" toWhom="per" type="oral">\2</q>\6', text)

    text = re.sub(r'_', r':', text, flags=re.MULTILINE)

    text = re.sub(r'<q who="per" toWhom="per" type="oral">', r'<q who="#per39" toWhom="#org0" type="oral">', text)

    return text
    
def values_q(content):

    # Intentamos recoger cosas como "Rut dijo a Noemí: "
    # No sé si funciona!
    content= re.sub(r'(<rs key="(#?(?:per|org)\d+)">.*?</rs>[^<]*?<rs key="(#?(?:per|org)\d+)">.*?</rs>.*?)<q who="per" toWhom="per" type="oral">', r'\1<q who="\2" toWhom="\3" type="oral">', content, flags=re.MULTILINE)

    # Buscamos el rs con identificador completo antes del q y se lo colocamos como valor del atributo who:
    content = re.sub(r'(<rs key="(#?(per|org)\d+)">(((?!<rs key="(#?(per|org)\d+)">).)*))<q who="per" toWhom="per" type="oral">', r'\1\5<q who="\2" toWhom="per" type="oral">', content)

    # Colocamos el mismo q del versículo anterior en caso de 
    content = re.sub(r'((<q who="#per\d+" toWhom=".*?" type="oral">).*?</q></ab>\s+<ab [^>]*?>)<q who="per" toWhom="per" type="oral">', r'\1\2', content)


    content = re.sub(r'(<q who=".*?" toWhom="per14") type="oral">', r'\1 type="prayer">', content)
    
    return(content)

def find_people_without_id(content, outputtei, bookcode, df):
    people_without_id = []
    people_without_id = people_without_id + re.findall(r"<rs key=\"per\">([A-Z][^<]*?)</rs>", content)
    print(type(people_without_id))
    people_without_id = dict(Counter(people_without_id))
    
    wrong_people = ["Calvo","Valera"]
    for wrong_person in wrong_people:
        try:
            del people_without_id[wrong_person]
        except:
            pass
    for people in people_without_id:
        print((people))

    print(people_without_id, len(people_without_id))
    people_without_id_df = pd.DataFrame(list(people_without_id.items()), columns=['entity','frequency'])

    people_without_id_df["type"] = "person"
    people_without_id_df["place?"] = 0

    for index, row in people_without_id_df.iterrows():
        person = row["entity"]

        results = len(re.findall(r"(en) <rs key=\"per\">"+person+r"</rs>", content))
        
        people_without_id_df.loc[index,"place?"] = results
        
        if df.loc[df["NormalizedName-sp"]==person].shape[0] > 0: 
            people_without_id_df.loc[index,"recheck"] = df.loc[df["NormalizedName-sp"]==person].sort_values(by="sum_freq", ascending=False).iloc[0]["id"]
            people_without_id_df.loc[index, 'recheck-in'] = df.loc[df["NormalizedName-sp"]==person].sort_values(by="sum_freq", ascending=False).iloc[0]["order-edition"]

    for index, row in people_without_id_df.iterrows():
        if row["place?"] / row["frequency"] > 0.2:
            people_without_id_df.loc[index,"type"] = "place"

    people_without_id_df.fillna("")
    people_without_id_df = people_without_id_df.sort_values(by=['type','frequency'], ascending=False)
    people_without_id_df.to_csv(outputtei+bookcode+"people_without_id.csv", sep='\t', encoding='utf-8')
    
    print(people_without_id_df)

    

def deleting_wrong_entities(content, bookcode):
    uncommon_entities_list = ["justicia","Mira","Sin","paz","justo"]
    for uncommon_entity in uncommon_entities_list:
        
        content = re.sub(r'<rs key="[^"]*?">' + uncommon_entity + '</rs>', uncommon_entity, content)

    content = re.sub(r'<rs key="#per17"><rs key="per17">Espíritu</rs> <rs key="per">Santo</rs></rs>', r'<rs key="#per17">Espíritu Santo</rs>', content)
    content = re.sub(r'<rs key="#per1"><rs key="#per1">Señor</rs> <rs key="#per1">Jesucristo</rs></rs>', r'<rs key="#per1">Señor</rs> <rs key="#per1">Jesucristo</rs>', content)
    
    

    content = re.sub(r'"#per5"', r'"#pla2"', content)
    content = re.sub(r'<rs key="org\d*">((hombres|hijos) de <rs key="#pla2">Judá</rs>)</rs>', r'<rs key="#org39">\1</rs>', content)
    content = re.sub(r'<rs key="org\d*">((hombres|hijos) de <rs key="#pla4">Israel</rs>)</rs>', r'<rs key="#org70">\1</rs>', content)
    content = re.sub(r'<rs key="#pla(\d*)">([^ ]*? de )<rs key="(#?pla\d+)"', r'<rs key="\3">\2<rs key="\3"', content)

    content = re.sub(r'<rs key="(.*?)"><rs key="\1">(.*?)</rs>(.*?)</rs>', r'<rs key="\1">\2\3</rs>', content)
    
    content = re.sub(r'\A.*?</teiHeader>', r'<?xml version="1.0" encoding="UTF-8"?>\n<?xml-model href="https://raw.githubusercontent.com/morethanbooks/XML-TEI-Bible/master/scheme/tei_lite.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n<?xml-stylesheet type="text/css" href="styles/styles.css" rel="stylesheet" title="Classic"?>\n<?xml-stylesheet type="text/css" href="styles/word2pix-quotes.css" rel="stylesheet" title="Word2Pix Quotations"?>\n<?xml-stylesheet type="text/css" href="styles/word2pix-reference.css" rel="stylesheet" title="Word2Pix References"?>\n<?xml-stylesheet type="text/css" href="styles/word2pix-level-q.css" rel="stylesheet" title="Word2Pix Level Quotation"?><TEI xmlns="http://www.tei-c.org/ns/1.0">\n	<teiHeader>\n		<fileDesc>\n			<titleStmt>\n				<title></title>\n				<title type="idno">\n					<idno type="string">'+bookcode+'</idno>\n					<idno type="viaf"></idno>\n				</title>\n				<author>\n					<name type="short"></name>\n					<name type="full"></name>\n					<idno type="viaf"></idno>\n				</author>\n				<principal key="#jct">José Calvo Tello</principal>\n			</titleStmt>\n			<publicationStmt>\n				<publisher>José Calvo Tello</publisher>\n				<availability status="free">\n					<p>The text is freely available.</p>\n				</availability>\n				<date when="2019">2019</date>\n			</publicationStmt>\n			<sourceDesc>\n				<bibl type="digital-source"><date when="2000">2000</date><idno></idno>.</bibl>\n				<bibl type="print-source">Reina Valera, <date when="1995">1995</date></bibl>\n				<bibl type="edition-first"><date when="1569">1569</date></bibl>\n			</sourceDesc>\n		</fileDesc>\n		<encodingDesc>\n			<p></p>\n		</encodingDesc>\n		<revisionDesc>\n			<change when="2019-02-02" who="#jct">First version of </change>\n		</revisionDesc>\n	</teiHeader>\n', content, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)

    return(content)

def find_rs_from_referer_refered(content, testament = "antiguo", minimal_freq = 4) :
    referer_refered = pd.read_csv("/home/jose/Dropbox/biblia/tb/resulting data/referer_refered.csv",sep="\t", index_col=0).fillna("")
    
    entities = pd.ExcelFile("/home/jose/Dropbox/biblia/tb/entities.xls",  index_col=0)
    entities = entities.parse('Sheet1').fillna(0)
    entities.index = entities["id"]
    
    books = pd.ExcelFile("/home/jose/Dropbox/biblia/tb/documentation/books.xlsx",  index_col=0)
    books = books.parse('Sheet1').fillna("")
    
    books_list = [book for book in books.loc[books["testament"].isin([testament])]["codebook"].tolist() if book in entities.columns.tolist()]
        
    
    entities["sum_books"] = entities[books_list].sum(axis=1)
    
    print(entities)
    print(entities["sum_books"].head()[0])
    print(entities["sum_books"].dtype)
    entities = entities.loc[ ((entities["sum_freq"] > 1) & (entities["importance"] == 1)) |  ((entities["sum_freq"] > 3) ) | ( (entities["type"].isin(["group","place","work"]))) ].copy()

    print(entities.head())
    #entities = entities.loc[  (entities["importance"] == 1) ].copy()
    
    print(entities)
    referer_refered["sum_books"] = referer_refered[books_list].sum(axis=1)
    referer_refered = referer_refered.loc[(referer_refered["id"].isin(entities.index.tolist()) ) & (referer_refered["referer"] != "") & (referer_refered["sum_books"] > 0)]
    #referer_refered.index = referer_refered["id"]
    columns = books_list.copy()
    columns.append("referer")
    columns.append("id")
    
    referer_refered = referer_refered[columns]
    
    referer_refered["sum"] = referer_refered.sum(axis=1)

    referer_refered["type"] = referer_refered["id"].str.extract("#(...)\d+")

    referer_refered = referer_refered.sort_values(by="sum", ascending=False)
    
    referer_refered = referer_refered.loc[ (referer_refered["sum"] > minimal_freq ) | (referer_refered["type"].isin(["pla"] )) ].sort_values(by="sum", ascending = False).groupby("referer").head(1)
    
    referer_refered["len"] = referer_refered["referer"].str.len()
    referer_refered = referer_refered.sort_values(by = "len", ascending = False)
    
    for id_, row in referer_refered[["referer","id"]].iterrows():
        print(row["referer"], row["id"])
        content = re.sub(r'(\W)('+ re.escape(row["referer"]) +r')(\W)', r'\1<rs key="'+row["id"]+r'">\2</rs>\3', content, flags=re.DOTALL|re.MULTILINE|re.UNICODE)

    return content

def finding_structure(inputcsv, inputtei, outputtei, bookcode, genre = "not-letter", testament = "antiguo", books_list=[]):
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
            
            
            # Buscamos las personas genéricas
            content = find_rs_from_referer_refered(content, testament = testament)
            print("done with referer")

            content = finding_proper_rs(content)

            #content = finding_proper_rs(content)

            # Buscamos las personas de la ontología
            content = finding_rs_from_ontology(content, df, bookcode, books_list = books_list)

            # Intentamos mejorar la estructura de rss
            content = improve_structure(content)

            
            find_people_without_id(content, outputtei,bookcode, df)

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
    "/home/jose/Dropbox/biblia/tb/entities.xls",
    "/home/jose/Dropbox/biblia/tb/programming/python/input/1CH.xml",
    "/home/jose/Dropbox/biblia/tb/programming/python/output/",
    "1CH",
    genre = "history", # "letter","prophetical",
    testament = "old",
    books_list = ["1KI","2KI","JOS","1CH","2CH", "NEH", "EZR", "GEN","EXO","NUM","LEV", "DEU","JDG","RUT","1SA","2SA","1KI","2KI",],#"JOS","JOS","JDG","RUT","1SA","2SA","MAT"],
    )
