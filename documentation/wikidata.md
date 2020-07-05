SELECT ?biblical_character ?biblical_characterLabel WHERE {
  ?biblical_character wdt:P31 wd:Q20643955.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
LIMIT 500000