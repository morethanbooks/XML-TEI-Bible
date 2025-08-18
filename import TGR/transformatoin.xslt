<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xhtml="https://www.w3.org/1999/xhtml/" exclude-result-prefixes="xs tei xhtml" version="2.0">
    <xsl:output encoding="utf-8" method="xhtml" indent="yes"/>

    <xsl:template match="tei:teiHeader">
        <details>
            <summary>Metadaten aus <pre style="display: inline;">teiHeader</pre></summary>
            <ul>
                <details>
                    <summary>Text-ID:</summary>
                    <ul>
                        <xsl:apply-templates select="//tei:text/@xml:id"/>
                    </ul>
                </details>
                <details>
                    <summary>Typ-Index: <pre style="display: inline;"><a href="http://www.folklore.uni-jena.de/attribut_a.xhtml" target="_blank">(Link zum Schema)</a></pre></summary>
                    <ul>
                        <xsl:apply-templates select="//tei:keywords[@scheme = 'http://www.folklore.uni-jena.de/attribut_a.xhtml']/tei:list/tei:item"/>
                    </ul>
                </details>
                <details>
                    <summary>Motiv-Index: <pre style="display: inline;"><a href="http://www.folklore.uni-jena.de/attribut_c.xhtml" target="_blank">(Link zum Schema)</a></pre></summary>
                    <ul>
                        <xsl:apply-templates select="//tei:keywords[@scheme = 'http://www.folklore.uni-jena.de/attribut_c.xhtml']/tei:list/tei:item"/>
                    </ul>
                </details>
                <details>
                    <summary>Digitale Quelle:</summary>
                    <ul>
                        <xsl:apply-templates select="//tei:fileDesc/tei:sourceDesc"/>
                    </ul>
                </details>
            </ul>
        </details>
    </xsl:template>

    <xsl:template match="tei:sourceDesc/tei:bibl[@type = 'digitalSource']/tei:ref">
        <li>
            <xsl:text/>
            <xsl:choose>
                <xsl:when test="@target">
                    <a href="{@target}" target="_blank">
                        <xsl:value-of select="."/>
                    </a>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
        </li>
    </xsl:template>

    <xsl:template match="tei:textClass/tei:keywords[@scheme = 'http://www.folklore.uni-jena.de/attribut_a.xhtml']/tei:list/tei:item">
        <li>
            <xsl:text/>
            <xsl:value-of select="."/>
        </li>
    </xsl:template>

    <xsl:template match="tei:textClass/tei:keywords[@scheme = 'http://www.folklore.uni-jena.de/attribut_c.xhtml']/tei:list/tei:item">
        <li>
            <xsl:text/>
            <xsl:value-of select="."/>
        </li>
    </xsl:template>

    <xsl:template match="tei:text/@xml:id">
        <li>
            <xsl:text/>
            <xsl:value-of select="string(.)"/>
        </li>
    </xsl:template>

    <xsl:template match="tei:text//tei:p">
        <p>
            <xsl:value-of select="string(.)"/>
        </p>
    </xsl:template>

    <xsl:template match="tei:text//tei:ab">
        <p>
            <xsl:value-of select="string(.)"/>
        </p>
    </xsl:template>

    <xsl:template match="tei:text//tei:head[@type='pericope']">
        <h2 style="color:red; ">
            <xsl:value-of select="string(.)"/>
        </h2>
    </xsl:template>

    <xsl:template match="tei:text//tei:rs">
        <span style="color:red; ">
            <xsl:value-of select="string(.)"/>
        </span>
    </xsl:template>


	<!--Metadata about the work and links to GND and Wikidata, GND and TGR genre-->
	<!--head bigger, with the @n of the great-father div-->
	<!-- @n of ab shown at the beginning -->
	<!-- rs bold -->
	<!-- q underlined -->
	<!-- rs containing people in blue -->
	<!-- rs containing groups in green -->
	<!-- rs containing places in pink -->
	<!-- mouse-over option for showing ids in rs/@key and q/@who and q/@toWhom -->
	

    <xsl:template match="/">
        <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <title>
                    <xsl:value-of select="/tei:TEI/tei:teiHeader[1]/tei:fileDesc[1]/tei:titleStmt[1]/tei:title[1]"/>
                </title>
            </head>
            <body>
                <xsl:call-template name="title"/>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>

    <xsl:template name="title">
        <h1>
            <xsl:value-of select="//tei:titleStmt[1]/tei:title[1]/string()"/>
        </h1>
    </xsl:template>

    <xsl:template match="node() | @*">
        <xsl:apply-templates/>
    </xsl:template>

</xsl:stylesheet>
