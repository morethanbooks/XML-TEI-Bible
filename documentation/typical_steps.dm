Typical search and replaces:

Replace:
(<ab .*?>)(?:<q who=".+?\d*" toWhom=".+?\d*" type="oral">)*(.*?)(?:</q>)*(</ab>)
With:
\1<q who="per14" toWhom="per26 per500" type="oral">\2</q>\3
In:
//div[@n="1"]


Replace
(<ab .*?>)(?:<q who=".*?" toWhom=".*?" type="oral">)*(.*?<q who=".*?" toWhom=".*?" type="oral">.*?)(?:</q>)*(</q></ab>)|(<ab .*?>)(?:<q who=".*?" toWhom=".*?" type="oral">)*(.*?)(?:</q>)*(</ab>)
With:
\1\4<q who="per14" toWhom="per26" type="oral"><q who="per26" toWhom="org70" type="oral">\2\5</q></q>\3\6
In:
//div[@n="1"]

