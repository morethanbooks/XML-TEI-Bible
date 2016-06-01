# XML-TEI Bible Documentation

This file gives some general information of how this project is being built.

# Overview

The main file of this project is the TEIBible.xml file, which is in the root of the folder. This projects encodes the books of the Bible one by one not in any previsable order. That explain the fact that only some of the books are (and will be) inside the TEIBible.xml. The other most important file is the ontology.xsl; there you will find the basic information about the people, groups, places, times and books that are encoded in the TEIBible.

All the other files and folders are documentation, extra files or work-in-process files.

## Licence

My work in this project and its markup are published under Creative Commons Licence BY Attribution 4.0 International. The data is available over GitHub and is published as it is. Please, take in consideration that this project lacks of any kind of financial or institutional support, for good and bad.

# Original Idea

I, José Calvo Tello, started this project in 2015 out of pure interest in his free time. I didn't find any version of the Bible in XML-TEI in which information below the verse level was encoded, like references to people and places, or who was talking and to whom. My interest on the Bible awaked the idea of encode such information, which meant another kind of reading and would allow the use of new computational techniques to get more information about the text.

Although this project is not part of my research work, neither I am preparing the data to answer any hypothesis, while working I am using my background as scholar with experience in different areas of philology, NLP and Digital Humanities.

# Text

At the moment following books are fully encoded in this chronological order:

* Gospel of Matthew
* Gospel of John
* Revelation
* Genesis
* Book of Ruth

At the moment, following book is being encoded:
* Book of Jonah

## Original Text

The original text comes from a Reina Valera translation into Spanish. I didn't take any of the most modern in order to avoid copy right problems.

## Language

The text is in Spanish because is my mother tongue. The project doesn't forsee to export the structure of the markup to other languages, but I could help to develope a strategy of doing it.

## Markup

The text is encoded in XML-TEI and controlled with a scheme, also published in the project. The root element of the TEIBible.xml  is a teiCorpus, which has very basic metadata. Every book is then encoded as a TEI element, with some basic Metadata.

### Chapters, Pericopes and Verses

The books of the Bible are identified using the ids from here: http://www.umiacs.umd.edu/~resnik/parallel/bible/bookcodes.all

In each book, the chapters are encoded as divs, keeping the number of,  the chapter both in a @n attribute and in the id. The verses follow the same system but are encoded as ab elements (I decided to use it because neither the definition of the p element nor l element fit the concept of the biblical verse).

Between chapters and verses exists a medium level of division, which typically has a title. I call it pericopes (although the pericopes are often used only to this level of division in the Gospels). 

In a few cases, the pericope division doesn't fit the verse division. That means, a part of a verse belong to a pericope and the rest of the part of the verse belong to the next pericope. This is a classical example where the xml rules doesn't match the complexity of the reality. In this cases I decided to put the whole verse in one of the pericopes, in order to keep the structure simple. It happens this, for example, in Genesis 35:22. 

One attribute used in different kind of elements is cert. In general in the majority of the cases it means that the encoder was not sure about some information encoded. One very good example of it when in Matthew 13:54 is said that Jesus _Vino a su tierra_, being uncertain if Nazareth, Belen or other place is meant. In case the attribute is in the TEI element div with the value high, it means that the whole book is not fully corrected but the specific chapter is.

### Name entities
It has been used the rs TEI element with the attribute key. It has been encoded the reference of:
* People, as per + number
* Groups and organizations, as org + number
* Places (known, unknown and spiritual), as pla + number
* Very clear time references, as tim + number
* Written works and books, as wor + number

The order of the number follow in the majority of the cases the order that I have been following encoding the Bible. So Jesus is per1 not because I think he is very important, but because he is the first person been mentioned in Matthew (the first book that I encoded).

To know more about the information that is encoded about each of this entities, read the section about the ontology.

#### Grammatical details
Proper (_Raquel_) and common names (_mujer_) have been disambiguated manually (future work: resolution of pronouns, verbs...). The phrase referenced to a entity might contain adjectives (_hija menor_), preposition followed by determinants or other names (_hija de Labán_). Neither subordinate adjective phrases (_hija que tuvo en Canaán_) nor determinants (_la mujer_) or possesive pronouns (_hija mío_) are part of the reference to the entity. Numbers are part of the resolution because in many cases they create a lexicalized phrase (_24 ancianos_, _12 tribus_). In case two proper names are mentioned one after the other referenced to the same person (_dijo a su mujer Rebeca_) both are encoded individually. In  general, adjectives not followed by a noun have been not resoluted (_ella era joven_); only in case and adjective was been used as a noun (_el menor_) it has been encoded.

#### Semantical details
In general, only people mentioned by name are encoded. Exception constitute people with a strong relative relations (_mujer de Noé_, _suegra de Pedro_), or that play an important role in different chapters (_faraón_, _copero del faraón_).

The groups are harder to delimit than individual persons. It has been encoded information about more or less well defined groups (_fariseos_, _discípulos_), celestial groups (_ángeles_, _demonios_), ethnical groups (_samaritanos_, _amorreos_, _egipcios_),  churches and religios groups (_sanedrín_, _iglesia de Efeso_), tribes and descendants (_tribu de Judá_, _hijos de Labán_). Anyway, the line of groups that are worth to mark and those groups who are not is thin.

If a person are not referenced with a name  or a strong relations, manytimes the person is marked just as part of the group that belongs. That happens specially with the angels: even if only one angel appears, he is marked as the group of angels. In case several people are refentiated and they do not constitute a clear group (_sus dos esposas_) or it is very clear who are meant (_Pedro y Juan, dos de sus discípulos_), they are referentiated not with an id of the group, but with the different personal ids.

### Direct Speech
Another main aspect of the markup of the text is the direct speech: everytime someone communicates with other person in some way (speacilly spoken and written) is marked with the TEI element q. The person or people who communicate is marked through its id with the attribute who. The person talked to is marked with the attribute corresp (in the absence of a better attribute). Both attributes can contain several values (_entonces Juan y Pedro dijeron a los fariseos y sacerdotes_). The kind of the communication is encoded with the attribute type, been possible the values:
* oral
* written
* dream
* unknown
* prayer
* vow
* soCalled (when quoting what other people have said)
* idea (when quoting something that someone should say to other person).

In case the person quotes some text, this is encoded in the attribute source.

Of course in case that someone tells that other person said, this are encoded as nested q. There are many example of very complex structures of this kind.

# Ontology

In the ontology file you find for each of this categories:
* id
* normalized name in Spanish (most natural name for this person)
* aclaration (if needed, speacilly assigning some familiar relations)
* variants (if the person had several names, like Jacob-Israel)
* comment (if needed)
* book (only AT as Old Testament, or NT as New Testament)
* cert (if the encoder is not sure if this distinction should actually be made or not)
* Gender (female, male or other, been male the default value)
* normalized names in German and Portuguese (work in progress beeing made by Matthias Ziegler)

# Previous Work and Inspiration

There different projects that have helped to put together this idea. One incredible resource is http://www.openbible.info/, which have a similar orientation and offer a lot of interesting visualizations and data.

Many of the things that I put in use in this project I have learnt from the CLiGS at the University of Würzburg, Germany, (http://cligs.hypotheses.org/) and many of my scripts look like a lot like the our toolbox.

# Aditional files

This project also includes some other files:
* Scheme to control the XML-TEI
* CSS to visualize the text in Browser and correct it
* Some files of documentation
* XSLT and Python scripts to extract some interesting information
* The resulting data and visualizations
* CSV file (ontology.csv) to control the ids used


# Thanks to

Thanks to Maria Calvo for many data, patiente and knowledge. The way I work owes you more than I normally recognize.
Thanks to Tabea for listening and support.
Thanks to Matthias Ziegler for thinking that this project is worth of his time.

# Future Work and colaboration

There is a lot that one can do with this text. My main tasks for the next future are:
* encode books of the Bible with the structured here presented
* improve the scripts that prepare the data for the personal correction in order to spare time and work
* improve the scripts that take the data and visualize it in different ways

And with this purposes I have work for a couple of years. Besides it, there a lot of ideas or possibilities. I am very open to work together with other people if they want to help. Here I list some ideas (of course there is a lot more to be done) sorted more or less by stimated difficulty:
* add geolocalization coordinates of places
* translate the ids of the entities to other languages in order to get visualizations in this languages aswell
* encode the pass of the time at the chapter level
* encode reference between verses in the Bible
* map the entities of the ontology with other resources like DB-Pedia, Strong concordances,
* speacilly the verse that are parallel to other very similar in other Gospels
* encode abstract actions like someone dying, someone getting married...
* mix linguistic annotation in the TEI structure
* resolute authomatically the people referenced in pronouns, verbs and other POS
* encode topic like money, forgiveness, love... Maybe use the Thompson Chain Reference (https://en.wikipedia.org/wiki/Thompson_Chain-Reference_Bible)
* add different information about the entities: subtypes, relations between people (wife-husband, parent-child, boss-servant) or between people and groups
* extract information about the relations between the entities from the text using structures like _mujer de Noe_.  <rs key=”per16”>mujer de <rs key=”per4”>Jacob</rs></rs> o <q who=”per16” corresp=”per14” type=”prayer”>Mi <rs key=”per109”>hijo</rs></q>; o <rs key=”per14 per15”>hijos de <rs key=”per4”>Jacob</rs></rs>
* export the structure of the markup to other languages (speacilly the original languages of the Bible) with some kind of Machine Learning method
