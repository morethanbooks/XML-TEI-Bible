# Especification about Bible Map

The basic idea is to show different kind of informations from the Bible in a map, to understand better different aspects from the entire Bible or specific books.

# Choosing Text Source

The user have the possibility of choosing whether the information comes from the entire Bible, one of the testaments of specific books. I imagine this option as checkboxes (first the entire Bible, then the two testaments and finally, maybe in a drop-down menu the different books).

# Layers of information

The user have the possibility of choosing different layers of information that should be showed or not in the map (each one of them showing a different icon). I imagine this similarly to the options in Google Maps or Google Earth about restaurants, cafés, institutions, etc. 

* Places: the places referred in the chosen base-text appear as circles, with their names in Spanish (it is what we have for now)
* Books: for each book of the Bible, all the places referred are extracted, their coordinates are extracted and the mean of all of them is calculated, resulting into a geolocation for each book. This should give a general overview about which places are referred in each book (Exodus-Egypt, majority of the old testament-Israel, Acts-around Cyprus, Revelation-current Turkey...).
* People: from the chosen base-text, all references to people are extracted; for each person, all places coocurring in the same pericope (we could also try verses and chapters, bbut verses could be too narrow, chapters too wide) are extracted (maybe get only a set of them, so the frequency of some very frequent doesn't pull everything too tight to Israel), their coordinates mapped and the average calculated. So each person gets a geolocation. Since there are around 2000 people and the great majority are around Israel, we should filter them either with quantitative filters (mean frequency in the chosen books), qualitative (important but unfrequent people like Mary should be in) or a mix. (Maybe we can show the icon as a male or female depeding on the person's gender?)
* Groups: the same than with indepedent people, but with groups. The filter is maybe not so needed, since the groups are probably more spread in the map. Let's see
* Sentiment Analysis: each entity (places, books, people, groups) gets a polarity score based on the average sentiment score of all the verses the it appears. This information is then showed through the color of the icon.


# Non-terrenal places

Besides the terrenal places, all non-terrenal places are also referred in the text. This can be shown splitting the window vertically (80% for terrenal, 20% for non-terrenal). Then the entities can be equally showed in a vertical axis.

# Language options

For now we only have the information in Spanish, we could already think about options for other languages and where should we place that in the map.

# Further development

* Semantic annotation: dictionaries or topic modelling

