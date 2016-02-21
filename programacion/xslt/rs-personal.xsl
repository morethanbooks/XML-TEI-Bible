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
	<xsl:template match="/">
		
		<xsl:for-each select="//rs[@key='per1']">
			<xsl:value-of select=".//text()"/><xsl:text>&#xa;</xsl:text>
		</xsl:for-each>
		
	</xsl:template>

	
	<xsl:template match="/">
		
		<xsl:for-each select="distinct-values(//rs//text()|//rs/rs/text())">
			<xsl:value-of select="."/>,
			<xsl:value-of select="count(.)"/>,
		</xsl:for-each>
		
	</xsl:template>
-->

	<xsl:template match="for $s in distinct-values(//ab/rs)">
		
			<p><xsl:value-of select="."/></p>
		
	</xsl:template>
	
	<xsl:output method="xhtml" indent="yes"/>
	<xsl:template match="/">
		
		
		<!-- ### Cover ### -->
		<xsl:result-document href="output/10000.xhtml" method="xhtml"
			doctype-system="http://www.w3c.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
			<html xmlns="http://www.w3.org/1999/xhtml">
				<head>
					<link href="../Styles/estilos.css" rel="stylesheet" type="text/css"/>
					<title>Cubierta</title>
				</head>
				<body>
					<xsl:apply-templates select="//rs"/>,
				</body>
			</html>
		</xsl:result-document>

	</xsl:template>
</xsl:stylesheet>
