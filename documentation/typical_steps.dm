Typical search and replaces:

Replace:
(<ab .*?>)(?:<q who="per" corresp="per" type="oral">)?(.*?)(?:</q>)?(</ab>)
With:
\1<q who="per14" corresp="per26" type="oral"><q who="per14" corresp="org70" type="idea">\2</q></q>\3
In:
//div[@n="1"]


