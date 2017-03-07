# Aspectos a revisar de un nuevo libro

Antes de dar por terminado un nuevo libro de la Biblia, hay que revisar:
## Pasos manuales
* reordenar los ids para que los ids nuevos de un libro sean consecutivos y no haya huecos
* Revisar metadatos en teiHeader
* Validar
* Que las q dentro de q tengan también valores soCalled e idea
* Revisar campos secundarios de nuevos registros en ontología y guardarlo como CSV
* Prettyprint en Notepad++

## Script revisión y conversión
* Revisar atributos con valores por defecto: //*[@key="per"]|//*[@corresp="per"]|//*[@who="per"]
* Colocar # antes en valores de atributos key, who y corresp: ("| )([a-z]) en //@key|//@who|//@corresp con
* Revisar con ("| )((?!#org\d+|#per\d+|#pla\d+|#wor\d+|#tim\d+).)*("| ) en //text//(@key|@who|@corresp)
* Revisar si de cada tipo de entidades se ha utilizado algún número mayor del que actualmente es
* Que los divs y heads de las perícopas tengas el atributo type="pericopes": <(div|head)> x <\1 type="pericope"> 
* Extra prettyprint: (\t\t\t\t\t<ab.*?>) with \1\n\t\t\t\t\t\t\t ; (</ab>) con \n\t\t\t\t\t\t\1
* Eliminar  cert="high" de divs: (<div [^>]*? type="chapter" [^>]*?) cert="high"> with \1>

## Pasos finales
* Integrar archivo en TEI principal
* Hacer network

