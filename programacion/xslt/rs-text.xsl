<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:tei="http://www.tei-c.org/ns/1.0"
	version="2.0"
	xmlns:xhtml="http://www.w3.org/1999/xhtml"
	xmlns="http://www.w3.org/1999/xhtml"
	xpath-default-namespace="http://www.tei-c.org/ns/1.0"
	exclude-result-prefixes="tei xsl xhtml"
	>

<xsl:output method="xhtml" indent="yes"/>

<xsl:template match="/">
<xsl:for-each select="//rs">
<xsl:text>
</xsl:text>
<xsl:value-of select=".//text()"/>
</xsl:for-each>
</xsl:template>

</xsl:stylesheet>
