# Documentation about the Annotation of Sexual Themes

In 2020 I have started annotating sexual themes in the Bible.

# Taxonomy
There is a taxonomy file with the list of the sexual themes.

# Steps
1. Annotate when the text mentions one of the themes in the taxonomy:
	1. That are marked with the type explicitly-sexual, or implicitly-sexual
	2. The values marked as no-sexual are only annotated when the in the verse there are other explicitly- or implicitly-sexual themes.
	3. Men and women are marked as sexual topics only when they play an important difference for the sexual themes. Note that men and women (both as single persons and as groups) are marked through entities.
	3. 
2. When there are sexual acts, it should be also annotated:	
	1. which stage (sexual-act-stage) if specified
	2. which type (sexual-act-type) if specified
	3. which situation (sexual-act-situation) if specified
	4. which participants (sexual-act-participants) if specified
3. Whenever an explicitly sexual aspect is annotated, it should be referred with a volaration ("valorations"). However, this is a secondary annotation that can be added later in a specific campaign.


# Certainty
 Annotate the certainty of the values in the attribute @cert based on following situations:
 
- **high**: there are clear textual evidences in the verse or in near verses
- **medium**: there are some textual evidences in the verse or in near verses, although they require some interpretation
- **low**: the textual evidences are weak, however either the traditions have stated this relation, or the annotator 

# Validation
Besides the typical schema, there is schematron that validates whether the values in the annotation are in the taxonomy.

# Annotation Format

Once the annotation is finished, the annotation is saved in elements `spanGrp` inside an `standOff` element. For example, in the following element there is the information that in Genesis 4.1 a coitus is being mentioned, and that the certainty is high based on textual evidences.

    <spanGrp type="theme" inst="#b.GEN.4.1">
    	<span ana="#coitus">
	   	   <certainty match="@ana" locus="value" cert="high" given="text"/>
	   </span>
    </spanGrp>

The actual verse in English (New International Version):

> Adam made love to his wife Eve, and she became pregnant and gave birth to Cain. She said, “With the help of the Lord I have brought forth a man.”

To check the entire annotation of this verse, check the file /sexual-annotation/TEIBible.xml and search for the following element:

    <standOff xml:id="b.GEN.sexualThemes" scheme="taxonomy.xml">

This `standOff` element appears after the closing tag of the `text` element.

However, to make the annotation process easier, while reading the verses, I just add a comment with the prefix `sex` and then the values and the certainties if they are not high. Here an example of the annotated values for the verse Genesis 4:1:

        <!--sex: coitus; heterosexual-sex; neutral; conception; birth; descendant-->

This is read by a Python script and transformed in the `spanGrp` element seen previously.

# Completeness

To check which books have been annotated already, check /documentation/books.xlsx

# Why are you Annotating this?

Pure personal interest. I have the hypothesis that what the churches communicate about sex has little biblical base. By that, churches are imposing sexual rules based on prejudices.
