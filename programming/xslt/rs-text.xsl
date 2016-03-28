<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:tei="http://www.tei-c.org/ns/1.0"
	version="2.0"
	xmlns:xhtml="http://www.w3.org/1999/xhtml"
	xmlns="http://www.w3.org/1999/xhtml"
	xpath-default-namespace="http://www.tei-c.org/ns/1.0"
	exclude-result-prefixes="tei xsl xhtml"
	>
	
	<!--
	Choose the book through its id in the xml:id attribute and put it in the select attribute of the next variable
	Examples:
	<xsl:variable name="text" select="'b.APO'"/>
	<xsl:variable name="text" select="'b.MAT'"/>
	<xsl:variable name="text" select="'b.JOH'"/>
	-->
	<xsl:variable name="name" select="'b.JOH'" />
	
	<xsl:output method="text" indent="yes"/>
	<xsl:template match="/">
		<xsl:result-document  href="output/{$name}_rs-text.csv" method="text">
			<xsl:text>text
</xsl:text>
			<xsl:for-each select="//div[@xml:id=$name]//rs/text()">
	<xsl:value-of select="."/>
		<xsl:text>
</xsl:text>
			</xsl:for-each>
		</xsl:result-document>
	</xsl:template>
	
</xsl:stylesheet>
