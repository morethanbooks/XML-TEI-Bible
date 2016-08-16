# Aspectos a revisar de un nuevo libro

Antes de dar por terminado un nuevo libro de la Biblia, hay que revisar:
* Colocar # antes en valores de atributos key, who y corresp: ("| )([a-z]) en //@key|//@who|//@corresp con  \1#\2
* validar
* revisar metadatos en teiHeader
* Que los divs y heads de las perícopas tengas el atributo type="pericopes"
* Que las q dentro de q tengan también valores soCalled e idea
* reordenar los ids para que los ids nuevos de un libro sean consecutivos y no haya huecos
* Prettyprint: (\t\t\t\t\t\t<ab.*?>) with \1\n\t\t\t\t\t\t\t; (</ab>) con \n\t\t\t\t\t\t\t\t\1
* Revisar campos secundarios de nuevos registros en ontología y guardarlo como CSV
* Integrar archivo en TEI principal
