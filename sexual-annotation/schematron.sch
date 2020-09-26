<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt">
    <sch:ns uri="http://www.tei-c.org/ns/1.0" prefix="tei"/>
    <sch:pattern>
        <sch:rule context="tei:spanGrp">
            
            <sch:let name="taxonomy-file" value="document('taxonomy.xml')"/>            

            <sch:let name="taxonomy" value="$taxonomy-file//tei:taxonomy" />

            <sch:assert test="tei:span/@ana = $taxonomy//tei:category/@xml:id">Category error.</sch:assert>
            
        </sch:rule>
    </sch:pattern>
</sch:schema>
