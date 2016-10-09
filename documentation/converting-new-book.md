* Take plaintext from rv95.txt file.
* Convert it into basic XML-TEI with txt2TEI.py
* Copy xml file from output to input and use finding_structure.py
* Search for <rs> without names with xpath:
	 for $s in distinct-values(//rs[@key="per"]/text()) return ($s, count(//rs[@key="per"][text()=$s]))
* Add new entities to ontology, export as csv and repeat the finding_structure.py with the new entities
