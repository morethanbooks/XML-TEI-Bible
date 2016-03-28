<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    version="2.0">
    
    <xsl:output method="text"/>
    
    <xsl:template match="/">
        <xsl:text>whoid,correspid
</xsl:text>
        <!--für jedes q (select) macht eine Gruppe (for-each-group) und gruppiere (group by)  nach dem einzelnen Wert im who @-->
        <xsl:for-each-group select="//div[@xml:id='b.MAT']//q" group-by="@who/tokenize(.,'\s')">
            <!--<xsl:sort/>-->
            <!--Nimmt den aktuellen key und speichert das als Variable-->
            <xsl:variable name="currkey" select="current-grouping-key()"/>
           
           <!--Für jedes Mitglied der Gruppe  -->
            <xsl:for-each select="current-group()">
                <!--Für jeden Wert in den @corresp -->
                <xsl:for-each select="@corresp/tokenize(.,'\s')">
                    
                    <!--schreibe den Gruppierenschlüssela und den Wert von dem letzten for-each heraus -->
                    <xsl:value-of select="$currkey"/>,<xsl:value-of select="."/><xsl:text>
</xsl:text>
                </xsl:for-each>
            </xsl:for-each>
        </xsl:for-each-group>
    </xsl:template>
    
</xsl:stylesheet>