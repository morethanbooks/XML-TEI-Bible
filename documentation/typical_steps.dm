Typical search and replaces:

Replace:
(<ab .*?>)(?:<q who="per" corresp="per" type="oral">)?(.*?)(?:</q>)?(</ab>)
With:
\1<q who="per14" corresp="per910" type="oral">\2</q>\3
In:
//div[@n="1"]


