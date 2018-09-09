Typical search and replaces:

Replace:
(<ab .*?>)(?:<q who="...\d*" toWhom="...\d*" type="oral">)*(.*?)(?:</q>)*(</ab>)
With:
\1<q who="per14" toWhom="per910" type="oral">\2</q>\3
In:
//div[@n="1"]


