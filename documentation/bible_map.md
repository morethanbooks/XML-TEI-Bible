# Specification about Bible Map

The basic idea is to show different kind of informations from the Bible in a map, to understand better different aspects from the entire Bible or specific books.

# Choosing Text Source

The user have the possibility of choosing whether the information comes from the entire Bible, one of the testaments of specific books. I imagine this option as checkboxes (first the entire Bible, then the two testaments and finally, maybe in a drop-down menu the different books).

# Layers of information

The user have the possibility of choosing different layers of information that should be showed or not in the map (each one of them showing a different icon). I imagine this similarly to the options in Google Maps or Google Earth about restaurants, cafés, institutions, etc. 

- Places: the places referred in the chosen base-text appear as circles, with their names in Spanish (it is what we have for now)
- Books: for each book of the Bible, all the places referred are extracted, their coordinates are extracted and the mean of all of them is calculated, resulting into a geolocation for each book. This should give a general overview about which places are referred in each book (Exodus-Egypt, majority of the old testament-Israel, Acts-around Cyprus, Revelation-current Turkey...).
- People: from the chosen base-text, all references to people are extracted; for each person, all places co-ocurring in the same pericope (we could also try verses and chapters, but verses could be too narrow, chapters too wide) are extracted (maybe get only a set of them, so the frequency of some very frequent doesn't pull everything too tight to Israel), their coordinates mapped and the average calculated. So each person gets a geolocation. Since there are around 2000 people and the great majority are around Israel, we should filter them either with quantitative filters (mean frequency in the chosen books), qualitative (important but infrequent people like Mary should be in) or a mix. (Maybe we can show the icon as a male or female depending on the person's gender?)
- Groups: the same than with independent people, but with groups (tribes of Israel, family of Abraham, moabits...). The filter is maybe not so needed, since the groups are probably more spread in the map. Let's see
- Certainty: the degree of certainty of the place (high, medium and low) can be expressed with he colour of the place
- Genre: a similar information to the "Books", only in stead of grouping the information in texts, grouping the information in the different genres (poetic, letter, prophetic, gospels, historical...)
- Sentiment Analysis: each entity (places, books, people, groups) gets a polarity score based on the average sentiment score of all the verses in which the it appears (in the entire Bible or in the selected texts? I guess in the selected texts?). This information is then showed through the color of the icon.
- Type of references: for each entity, there are different ways of referring it: a standardized form (*Jesús*) or the most frequent that is actually used (*señor*). Since for many people the standardized and the most common are the same, we should make available the possibility of using "the most common that is not the standardized form".

# Historical Development

Since the Bible covers a large period of history, it could very interesting to observe this in dimanic development. The idea would be to choose the texts and the layers of information, and then have the option to click somewhere in a kind of play button. This will render the selected layers from the selected texts in chronological order (the dates of the period that each book covers has to be integrated in the XML-TEI). For example, we could choose to observe in whole Bible the information about books and places, and then click "play history". The user then will see first the map empty, and then the places of Genesis AND the book icon of Genesis (with places around Irak-Israel-Egypt), then they will disappear and the name of Exodus and the places of Exodus will appear (around Egypt), and so on. Of course the user could have selected other layers information, such as groups and people, or even the sentiment and places (showing how the sentiment of different places change over time).

# Non-earthly places

Besides the earthly places, all non-earthly places are also referred in the text. This can be shown splitting the window vertically (80% for earthly, 20% for non-earthly). Then the entities can be equally showed in a vertical axis. I think we should show in this axis only the places that are not in the regular map. That means that for the normal map we would filter out all superior places and not showing them there; and for the non-earthly axis we would only show the non-human groups, people and places. We would show in the regular map where the non-human people and groups are place (we want to know to which places are referred entities such as God(s), angels or demons.


# Language options

For now we only have the information in Spanish, we could already think about options for other languages and where should we place that in the map.

# Further development

- Semantic annotation: dictionaries or topic modelling, showing the highest value related to each place or entities (books, people, groups...)

# Extraction of information

This part is just pseudo-code for the extraction of the information for the different layers:


## Places:

open the entities files and get the places

For each book:
	for each different place in the entities file
		check how many times it appears in the book

sum the references of the new testament and old testament
save the (places are rows, columns are books)

### Location
This information is already in entities.xls

## Books:
Open the entities
Open the file of books
For each book
	get all the references to places in the book
	make a set of the references
	filter out the references that have an exceptable certainty
	get the geolocation
	calculate the mean (median?) of the latitude and the longitude
save this information in the file of books

## Genres
Open the file of books
for each genre
	Calculate the mean (median?) of the books that are part of the books

## People

Open the entities
for each person
	for each book in the bible
		for each pericope
			get the places that are mentioned
		calculate the mean-median latitude and longitude of the places of each person and save it
	calculate the longitude and latitude of the Old and New Testament
	calculate the longitude and latitude of the Bible

## Groups

The same as with people

# Prototype

http://informatik.uni-leipzig.de:8080/BiblePlaces2.0/

# Feedback from the first Review Process


- What is the quality of the georeferences?
- What is the novelty of the project? Why is it interesting? What is new? 
- Reviewer: You call it a "gold standard", but, is it really?
- What exactly is already implemented? 



