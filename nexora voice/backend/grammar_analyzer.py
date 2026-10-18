"""
Speech Delivery Analyser - Spoken Grammar & Syntactic Analysis Engine
Performs comprehensive grammatical, syntactic, and structural evaluation of user speech transcripts.
Detects:
1. Subject-Verb Agreement (singular/plural mismatches, irregular pronoun verbs)
2. Tense Inconsistency & Irregular Verb Forms (have went, did saw, etc.)
3. Articles & Determiners (phonetic a/an rules, countable noun gaps, quantifier mismatches)
4. Prepositions & Spoken Collocations (depend of, discuss about, listen music, etc.)
5. Double Negatives (don't know nothing, can't hardly, etc.)
6. Pronoun Case & Agreement (between you and I, him and me went, etc.)
7. Spoken Informal Slang / Colloquialisms (gonna, wanna, gotta, ain't, etc.)
8. Duplicate Spoken Words / False Starts (the the, I I, etc.)
9. Run-On Spoken Sentences & Fragmented Clauses (>28 words unpunctuated, dangling clauses)
10. Multilingual Grammar Checks (Spanish, French, German, Hindi, Tamil, etc.)
"""

import re
import math
from typing import List, Dict, Any, Tuple, Optional


# Severity mapping
SEV_MINOR = 1
SEV_MODERATE = 2
SEV_SERIOUS = 3


# ==============================================================================
# RULE DEFINITIONS FOR ENGLISH SPOKEN GRAMMAR
# ==============================================================================

# 1. Subject-Verb Agreement Patterns
SUBJECT_VERB_PATTERNS = [
    # Pronoun + mismatch verb
    (r"\b(he|she|it)\s+(?:are|were)\b", "{0} is", "Singular third-person subject '{0}' requires the singular verb 'is' (or 'was').", SEV_SERIOUS, "subject_verb_mismatch"),
    (r"\b(he|she|it)\s+have\b", "{0} has", "Third-person singular '{0}' takes 'has', not 'have'.", SEV_SERIOUS, "subject_verb_mismatch"),
    (r"\b(he|she|it)\s+do\b", "{0} does", "Third-person singular '{0}' takes 'does', not 'do'.", SEV_SERIOUS, "subject_verb_mismatch"),
    (r"\b(he|she|it)\s+don't\b", "{0} doesn't", "Third-person singular '{0}' requires 'doesn't' (does not) instead of 'don't'.", SEV_SERIOUS, "subject_verb_mismatch"),
    (r"\b(they|we|you)\s+(?:is|was)\b", "{0} are", "Plural pronoun '{0}' requires plural verb form 'are' (or 'were').", SEV_SERIOUS, "subject_verb_mismatch"),
    (r"\b(they|we|you)\s+has\b", "{0} have", "Plural pronoun '{0}' takes 'have', not 'has'.", SEV_SERIOUS, "subject_verb_mismatch"),
    (r"\b(they|we|you)\s+does\b", "{0} do", "Plural pronoun '{0}' takes 'do', not 'does'.", SEV_SERIOUS, "subject_verb_mismatch"),
    (r"\b(everyone|everybody|someone|somebody|anyone|anybody|nobody|no one|each)\s+(?:are|were)\b", "{0} is", "Indefinite pronoun '{0}' is grammatically singular and takes 'is' or 'was'.", SEV_MODERATE, "subject_verb_mismatch"),
    (r"\b(everyone|everybody|someone|somebody|anyone|anybody|nobody|no one|each)\s+have\b", "{0} has", "Indefinite pronoun '{0}' takes 'has', not 'have'.", SEV_MODERATE, "subject_verb_mismatch"),
    (r"\b(people)\s+(?:is|was)\b", "people are", "'People' is a plural noun and takes plural verb 'are' (or 'were').", SEV_SERIOUS, "subject_verb_mismatch"),
    (r"\b(people)\s+has\b", "people have", "'People' takes plural verb 'have', not 'has'.", SEV_SERIOUS, "subject_verb_mismatch"),
    (r"\bthis\s+(people|men|women|children|feet|teeth|data)\b", "these {0}", "'{0}' is plural; use the plural demonstrative 'these' instead of 'this'.", SEV_MODERATE, "determiner_mismatch"),
    (r"\b(these|those)\s+(person|man|woman|child|foot|tooth)\b", "this {1}", "'{1}' is singular; use the singular demonstrative 'this' or 'that'.", SEV_MODERATE, "determiner_mismatch"),
]

# 2. Tense & Verb Form Patterns
TENSE_VERB_PATTERNS = [
    # Perfect tense + past simple (should be past participle)
    (r"\b(have|has|had|having)\s+went\b", "{0} gone", "The past participle of 'go' is 'gone'. Use '{0} gone', not '{0} went'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+saw\b", "{0} seen", "The past participle of 'see' is 'seen'. Use '{0} seen', not '{0} saw'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+took\b", "{0} taken", "The past participle of 'take' is 'taken'. Use '{0} taken', not '{0} took'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+ate\b", "{0} eaten", "The past participle of 'eat' is 'eaten'. Use '{0} eaten', not '{0} ate'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+did\b", "{0} done", "The past participle of 'do' is 'done'. Use '{0} done', not '{0} did'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+spoke\b", "{0} spoken", "The past participle of 'speak' is 'spoken'. Use '{0} spoken', not '{0} spoke'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+wrote\b", "{0} written", "The past participle of 'write' is 'written'. Use '{0} written', not '{0} wrote'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+broke\b", "{0} broken", "The past participle of 'break' is 'broken'. Use '{0} broken', not '{0} broke'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+chose\b", "{0} chosen", "The past participle of 'choose' is 'chosen'. Use '{0} chosen', not '{0} chose'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+began\b", "{0} begun", "The past participle of 'begin' is 'begun'. Use '{0} begun', not '{0} began'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+came\b", "{0} come", "The past participle of 'come' is 'come'. Use '{0} come', not '{0} came'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+ran\b", "{0} run", "The past participle of 'run' is 'run'. Use '{0} run', not '{0} ran'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\b(have|has|had|having)\s+drank\b", "{0} drunk", "The past participle of 'drink' is 'drunk'. Use '{0} drunk', not '{0} drank'.", SEV_SERIOUS, "tense_inconsistency"),

    # Auxiliary 'did' + past tense (double past)
    (r"\bdid\s+went\b", "did go", "After the auxiliary 'did', use the base verb form 'go', not past tense 'went'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\bdid\s+saw\b", "did see", "After 'did', use base form 'see', not 'saw'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\bdid\s+had\b", "did have", "After 'did', use base form 'have', not 'had'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\bdid\s+came\b", "did come", "After 'did', use base form 'come', not 'came'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\bdid\s+spoke\b", "did speak", "After 'did', use base form 'speak', not 'spoke'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\bdid\s+took\b", "did take", "After 'did', use base form 'take', not 'took'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\bdid\s+knew\b", "did know", "After 'did', use base form 'know', not 'knew'.", SEV_SERIOUS, "tense_inconsistency"),
    (r"\bdid\s+found\b", "did find", "After 'did', use base form 'find', not 'found'.", SEV_SERIOUS, "tense_inconsistency"),

    # Non-standard regularized past tense
    (r"\bcatched\b", "caught", "'Catch' is an irregular verb. Past tense is 'caught', not 'catched'.", SEV_MODERATE, "tense_inconsistency"),
    (r"\bteached\b", "taught", "'Teach' is irregular. Past tense is 'taught', not 'teached'.", SEV_MODERATE, "tense_inconsistency"),
    (r"\bbringed\b", "brought", "'Bring' is irregular. Past tense is 'brought', not 'bringed'.", SEV_MODERATE, "tense_inconsistency"),
    (r"\bbuyed\b", "bought", "'Buy' is irregular. Past tense is 'bought', not 'buyed'.", SEV_MODERATE, "tense_inconsistency"),
    (r"\bcosted\b", "cost", "The past tense of 'cost' is 'cost', not 'costed'.", SEV_MODERATE, "tense_inconsistency"),
    (r"\bhitted\b", "hit", "The past tense of 'hit' is 'hit', not 'hitted'.", SEV_MODERATE, "tense_inconsistency"),
    (r"\bhurted\b", "hurt", "The past tense of 'hurt' is 'hurt', not 'hurted'.", SEV_MODERATE, "tense_inconsistency"),
]

# 3. Articles & Determiners Patterns
ARTICLE_PATTERNS = [
    # 'a' before vowel sound
    (r"\ba\s+(apple|orange|egg|elephant|idea|opinion|example|opportunity|issue|impact|instance|important|easy|excellent|obvious|accurate|immediate|unusual)\b", "an {0}", "Use indefinite article 'an' before vowel sounds: 'an {0}', not 'a {0}'.", SEV_MODERATE, "article_error"),
    (r"\ba\s+(hour|honest|honor|heir)\b", "an {0}", "'{0}' starts with a silent 'h' and vowel sound; use 'an {0}', not 'a {0}'.", SEV_MODERATE, "article_error"),

    # 'an' before consonant sound
    (r"\ban\s+(university|uniform|unique|unit|user|universal|european|one)\b", "a {0}", "'{0}' begins with a consonant glide sound (/juː/ or /w/); use 'a {0}', not 'an {0}'.", SEV_MODERATE, "article_error"),

    # Quantifier mismatches
    (r"\b(much)\s+(people|students|children|friends|problems|questions|reasons|years|words)\b", "many {1}", "'{1}' is a countable plural noun; use 'many {1}' instead of 'much {1}'.", SEV_MODERATE, "determiner_mismatch"),
    (r"\b(less)\s+(people|students|children|friends|problems|questions|reasons|years)\b", "fewer {1}", "For countable plural items like '{1}', standard formal usage prefers 'fewer {1}' over 'less {1}'.", SEV_MINOR, "determiner_mismatch"),
    (r"\bevery\s+(students|people|children|friends|problems)\b", "every student / all {0}", "'Every' modifies singular nouns; use 'every student' or 'all {0}'.", SEV_MODERATE, "determiner_mismatch"),
]

# 4. Prepositions & Collocations
PREPOSITION_PATTERNS = [
    (r"\bdepend\s+of\b", "depend on", "The standard preposition is 'depend on' (or 'upon'), not 'depend of'.", SEV_MODERATE, "preposition_error"),
    (r"\bdepends\s+of\b", "depends on", "The standard preposition is 'depends on' (or 'upon'), not 'depends of'.", SEV_MODERATE, "preposition_error"),
    (r"\bdepending\s+of\b", "depending on", "Use 'depending on', not 'depending of'.", SEV_MODERATE, "preposition_error"),
    (r"\blisten\s+(music|to\s+music)\b", "listen to music", "The verb 'listen' requires the preposition 'to' before its object: 'listen to {0}'.", SEV_MODERATE, "preposition_error"),
    (r"\blisten\s+(me|him|her|them|us)\b", "listen to {0}", "Use 'listen to {0}', not 'listen {0}'.", SEV_MODERATE, "preposition_error"),
    (r"\bdiscuss\s+about\b", "discuss", "'Discuss' is a transitive verb that takes a direct object without 'about' (e.g. 'discuss the topic', not 'discuss about the topic').", SEV_MODERATE, "preposition_error"),
    (r"\bdiscussed\s+about\b", "discussed", "Use 'discussed the topic' without 'about'.", SEV_MODERATE, "preposition_error"),
    (r"\bdiscussing\s+about\b", "discussing", "Use 'discussing' directly with the object, omitting 'about'.", SEV_MODERATE, "preposition_error"),
    (r"\binterested\s+on\b", "interested in", "The adjective 'interested' collocates with 'in', not 'on'.", SEV_MODERATE, "preposition_error"),
    (r"\bmarried\s+with\b", "married to", "In standard English, one is 'married to' someone, not 'married with'.", SEV_MODERATE, "preposition_error"),
    (r"\bcongratulate\s+for\b", "congratulate on", "The standard idiom is 'congratulate on' (e.g. 'congratulate you on your achievement').", SEV_MODERATE, "preposition_error"),
    (r"\bexplain\s+(me|him|her|them|us)\s+(\w+)\b", "explain {1} to {0}", "'Explain' requires prepositional phrase 'to {0}' (e.g. 'explain the issue to me', not 'explain me the issue').", SEV_MODERATE, "preposition_error"),
    (r"\bexplain\s+(me|him|her|them|us)\b", "explain to {0}", "Use 'explain to {0}', not 'explain {0}'.", SEV_MODERATE, "preposition_error"),
    (r"\bgood\s+in\s+(speaking|debating|math|english|sports|presenting)\b", "good at {0}", "When describing competence or skill, use 'good at {0}', not 'good in {0}'.", SEV_MINOR, "preposition_error"),
    (r"\bsuperior\s+than\b", "superior to", "'Superior' takes the preposition 'to', not 'than'.", SEV_MODERATE, "preposition_error"),
    (r"\binferior\s+than\b", "inferior to", "'Inferior' takes the preposition 'to', not 'than'.", SEV_MODERATE, "preposition_error"),
    (r"\bpay\s+attention\s+on\b", "pay attention to", "The idiom is 'pay attention to', not 'pay attention on'.", SEV_MODERATE, "preposition_error"),
    (r"\bconcentrate\s+in\b", "concentrate on", "Use 'concentrate on', not 'concentrate in'.", SEV_MODERATE, "preposition_error"),
    (r"\bcomplain\s+about\s+(him|her|them|someone)\s+to\b", "complain to", "Collocation order: 'complain to someone about something'.", SEV_MINOR, "preposition_error"),
    (r"\barrive\s+to\s+(the\s+city|new\s+york|london|school|work|paris)\b", "arrive at / in {0}", "Use 'arrive at' (for venues) or 'arrive in' (for cities/countries), not 'arrive to'.", SEV_MODERATE, "preposition_error"),
]

# 5. Double Negatives Patterns
DOUBLE_NEGATIVE_PATTERNS = [
    (r"\b(don't|doesn't|didn't|cannot|can't|won't|wouldn't|couldn't|shouldn't)(\s+\w+)?\s+nothing\b", "{0}{1} anything", "Double negative: '{0}{1} nothing' expresses a non-standard construction. Use '{0}{1} anything'.", SEV_SERIOUS, "double_negative"),
    (r"\b(can't|cannot|couldn't)\s+hardly\b", "can hardly", "'Hardly' is already negative; pairing it with '{0}' creates an improper double negative. Use 'can hardly' or 'could hardly'.", SEV_SERIOUS, "double_negative"),
    (r"\b(haven't|hasn't|hadn't)\s+no\b", "{0} any", "Double negative: Use '{0} any' or affirmative 'have no'.", SEV_SERIOUS, "double_negative"),
    (r"\b(didn't|don't|doesn't)\s+have\s+no\b", "{0} have any", "Double negative: Use '{0} have any', not '{0} have no'.", SEV_SERIOUS, "double_negative"),
    (r"\bnever\s+(told|said|gave|showed)\s+nobody\b", "never {0} anybody", "Double negative: 'never ... nobody'. Use 'never {0} anybody'.", SEV_SERIOUS, "double_negative"),
    (r"\bnot\s+never\b", "never", "Redundant double negative 'not never'. Use 'never' alone.", SEV_SERIOUS, "double_negative"),
    (r"\bwithout\s+no\b", "without any", "'Without' is negative; use 'without any', not 'without no'.", SEV_SERIOUS, "double_negative"),
]

# 6. Pronoun Case & Agreement
PRONOUN_PATTERNS = [
    (r"\bbetween\s+you\s+and\s+I\b", "between you and me", "Prepositions like 'between' take objective pronoun cases: 'between you and me', not 'between you and I'.", SEV_MODERATE, "pronoun_case"),
    (r"\bfor\s+you\s+and\s+I\b", "for you and me", "Object of preposition 'for' must be in objective case: 'for you and me'.", SEV_MODERATE, "pronoun_case"),
    (r"\bto\s+you\s+and\s+I\b", "to you and me", "Object of preposition 'to' must be 'me': 'to you and me'.", SEV_MODERATE, "pronoun_case"),
    (r"\bwith\s+you\s+and\s+I\b", "with you and me", "Object of preposition 'with' must be 'me': 'with you and me'.", SEV_MODERATE, "pronoun_case"),
    (r"\b(him\s+and\s+me|me\s+and\s+him)\s+(went|did|have|saw|came|are|were|stand|speak)\b", "he and I {2}", "Compound subject requires subjective pronouns: 'he and I {2}', not '{0} {2}'.", SEV_MODERATE, "pronoun_case"),
    (r"\b(her\s+and\s+me|me\s+and\s+her)\s+(went|did|have|saw|came|are|were|stand|speak)\b", "she and I {2}", "Compound subject requires subjective pronouns: 'she and I {2}'.", SEV_MODERATE, "pronoun_case"),
    (r"\b(them)\s+(went|did|saw|said|came)\b", "they {2}", "Subject of a clause requires subjective pronoun 'they', not objective 'them'.", SEV_SERIOUS, "pronoun_case"),
    (r"\btheirselves\b", "themselves", "Standard reflexive pronoun is 'themselves', not non-standard 'theirselves'.", SEV_MODERATE, "pronoun_case"),
    (r"\bourself\b", "ourselves", "Reflexive form for plural 'our' is 'ourselves', not 'ourself'.", SEV_MODERATE, "pronoun_case"),
]

# 7. Spoken Informal Slang / Colloquialisms
SLANG_PATTERNS = [
    (r"\bgonna\b", "going to", "Spoken contraction 'gonna' undermines formal oratory tone. Pronounce 'going to' clearly.", SEV_MINOR, "colloquial_slang"),
    (r"\bwanna\b", "want to", "Spoken contraction 'wanna' is overly informal. Pronounce 'want to'.", SEV_MINOR, "colloquial_slang"),
    (r"\bgotta\b", "have to / must", "Spoken contraction 'gotta' is informal. Use 'have to' or 'must' for executive presence.", SEV_MINOR, "colloquial_slang"),
    (r"\bkinda\b", "kind of / rather", "Colloquial 'kinda' weakens rhetorical certainty. Use 'rather' or articulate 'kind of'.", SEV_MINOR, "colloquial_slang"),
    (r"\bsorta\b", "sort of", "Colloquial 'sorta' signals hesitation. Pronounce 'sort of' or choose a precise adjective.", SEV_MINOR, "colloquial_slang"),
    (r"\bain't\b", "is not / are not", "Non-standard contraction 'ain't' sharply degrades formal credibility. Use 'is not', 'are not', or 'have not'.", SEV_SERIOUS, "colloquial_slang"),
    (r"\bdunno\b", "do not know", "Slang 'dunno' signals casual indifference. Articulate 'do not know'.", SEV_MODERATE, "colloquial_slang"),
    (r"\bgimme\b", "give me", "Slang 'gimme' is non-standard. Articulate 'give me'.", SEV_MINOR, "colloquial_slang"),
    (r"\blemme\b", "let me", "Slang 'lemme' is informal. Articulate 'let me'.", SEV_MINOR, "colloquial_slang"),
    (r"\boutta\b", "out of", "Slang 'outta' is informal. Articulate 'out of'.", SEV_MINOR, "colloquial_slang"),
]

# Multilingual pattern collections for all 10 supported languages
MULTILINGUAL_GRAMMAR_RULES = {
    "es": [
        # Subject-verb agreement
        (r"\b(nosotros)\s+(es|está|ha|hace|va|habla)\b", "somos / estamos / hemos / hacemos / vamos / hablamos", "El pronombre plural 'nosotros' exige verbo en primera persona plural, no singular '{1}'.", SEV_SERIOUS, "subject_verb_mismatch", "Concordancia Sujeto-Verbo"),
        (r"\b(ellos|ellas|ustedes)\s+(es|está|va|habla|tiene)\b", "son / están / van / hablan / tienen", "Sujeto plural '{0}' exige verbo en plural (3ª persona plural).", SEV_SERIOUS, "subject_verb_mismatch", "Concordancia Sujeto-Verbo"),
        (r"\b(yo)\s+(es|está|va|tiene|hace|son)\b", "soy / estoy / voy / tengo / hago", "El pronombre singular 'yo' exige verbo en primera persona singular.", SEV_SERIOUS, "subject_verb_mismatch", "Concordancia Sujeto-Verbo"),
        (r"\b(la\s+gente)\s+(son|están|fueron|tienen|van)\b", "la gente es / está / fue / tiene / va", "'Gente' es un sustantivo colectivo singular y concuerda en singular en español normativo.", SEV_MODERATE, "subject_verb_mismatch", "Concordancia Sujeto-Verbo"),
        # Gender & article concordance
        (r"\b(la|una)\s+(problema|tema|sistema|idioma|programa|planeta|mapa|día)\b", "el {1}", "'{1}' es sustantivo masculino de origen griego o histórico; use 'el/un {1}', no 'la/una {1}'.", SEV_MODERATE, "gender_agreement", "Concordancia de Género"),
        (r"\b(el|un)\s+(casa|mano|foto|gente|noche|verdad|ciudad|parte)\b", "la {1}", "'{1}' es femenino; use 'la/una {1}', no 'el/un {1}'.", SEV_MODERATE, "gender_agreement", "Concordancia de Género"),
        (r"\b(las)\s+(problemas|temas|sistemas|idiomas|programas)\b", "los {1}", "Sustantivo masculino en plural; use 'los {1}'.", SEV_MODERATE, "gender_agreement", "Concordancia de Género"),
        # Prepositions & Collocations
        (r"\bconsistir\s+de\b", "consistir en", "La preposición adecuada con 'consistir' es 'en', no 'de'.", SEV_MODERATE, "preposition_error", "Régimen Preposicional"),
        (r"\bsoñar\s+de\b", "soñar con", "En español normativo se dice 'soñar con', no 'soñar de'.", SEV_MODERATE, "preposition_error", "Régimen Preposicional"),
        (r"\ben\s+base\s+a\b", "a base de / sobre la base de", "Locución impropia 'en base a'. Emplee 'sobre la base de' o 'a base de'.", SEV_MINOR, "preposition_error", "Régimen Preposicional"),
        (r"\bde\s+acuerdo\s+a\b", "de acuerdo con", "En el registro formal oratorio se recomienda 'de acuerdo con'.", SEV_MINOR, "preposition_error", "Régimen Preposicional"),
        # Colloquial slang / Apocope
        (r"\bpos\b", "pues", "Contracción informal 'pos'. Pronuncie 'pues' con claridad oratoria.", SEV_MINOR, "colloquial_slang", "Vulgarismo / Registro Oral"),
        (r"\bpa\b", "para", "Apócope coloquial 'pa'. Articule 'para' en oratoria formal.", SEV_MINOR, "colloquial_slang", "Vulgarismo / Registro Oral"),
        (r"\btoy\b", "estoy", "Contracción 'toy'. Articule 'estoy'.", SEV_MINOR, "colloquial_slang", "Vulgarismo / Registro Oral"),
        (r"\bta\b", "está", "Apócope 'ta'. Articule 'está'.", SEV_MINOR, "colloquial_slang", "Vulgarismo / Registro Oral"),
        (r"\btonces\b", "entonces", "Contracción oral 'tonces'. Diga 'entonces'.", SEV_MINOR, "colloquial_slang", "Vulgarismo / Registro Oral"),
    ],
    "fr": [
        # Subject-verb agreement
        (r"\b(nous)\s+(est|a|va|fait|parle)\b", "sommes / avons / allons / faisons / parlons", "Le pronom pluriel 'nous' exige un verbe conjugué à la 1re personne du pluriel.", SEV_SERIOUS, "subject_verb_mismatch", "Accord Sujet-Verbe"),
        (r"\b(ils|elles)\s+(a|est|va|fait|parle)\b", "ont / sont / vont / font / parlent", "Le sujet pluriel '{0}' exige un verbe au pluriel.", SEV_SERIOUS, "subject_verb_mismatch", "Accord Sujet-Verbe"),
        (r"\b(je)\s+(est|a|va|sont|avons)\b", "suis / ai / vais", "Le pronom 'je' exige la première personne du singulier.", SEV_SERIOUS, "subject_verb_mismatch", "Accord Sujet-Verbe"),
        (r"\b(les\s+gens)\s+(est|a|va)\b", "les gens sont / ont / vont", "'Les gens' est un pluriel et requiert l'accord au pluriel.", SEV_SERIOUS, "subject_verb_mismatch", "Accord Sujet-Verbe"),
        (r"\b(tout\s+le\s+monde)\s+(sont|ont|vont)\b", "tout le monde est / a / va", "'Tout le monde' est grammaticalement singulier et s'accorde au singulier.", SEV_MODERATE, "subject_verb_mismatch", "Accord Sujet-Verbe"),
        # Gender & article concordance
        (r"\b(le|un)\s+(maison|voiture|vie|chose|personne|heure|femme|ville)\b", "la {1}", "'{1}' est féminin en français; employez 'la/une {1}'.", SEV_MODERATE, "gender_agreement", "Accord en Genre"),
        (r"\b(la|une)\s+(problème|monde|temps|pays|travail|jour|groupe|homme)\b", "le {1}", "'{1}' est masculin; employez 'le/un {1}'.", SEV_MODERATE, "gender_agreement", "Accord en Genre"),
        # Preposition & Collocation
        (r"\bvisiter\s+à\s+(un|une|des|mon|ma|mes)?\s*(\w+)\b", "rendre visite à", "On 'rend visite à une personne', on ne 'visite pas à'.", SEV_MODERATE, "preposition_error", "Régime Prépositionnel"),
        (r"\bse\s+rappeler\s+de\b", "se souvenir de / se rappeler", "'Se rappeler' est transitif direct (se rappeler quelque chose, sans 'de').", SEV_MODERATE, "preposition_error", "Régime Prépositionnel"),
        (r"\bpallier\s+à\b", "pallier", "'Pallier' est transitif direct (pallier un manque, sans 'à').", SEV_MODERATE, "preposition_error", "Régime Prépositionnel"),
        # Colloquial oral contractions
        (r"\bj'sais\s+pas\b", "je ne sais pas", "Forme orale relâchée. Utilisez la négation complète 'je ne sais pas' en prise de parole formelle.", SEV_MINOR, "colloquial_slang", "Niveau de Langue Oral"),
        (r"\bt'es\b", "tu es", "Élision familière 't'es'. Prononcez 'tu es' pour une diction oratoire soignée.", SEV_MINOR, "colloquial_slang", "Niveau de Langue Oral"),
        (r"\by\s+a\b", "il y a", "Omission du pronom impersonnel. Dites 'il y a'.", SEV_MINOR, "colloquial_slang", "Niveau de Langue Oral"),
        (r"\bchuis\b", "je suis", "Contraction populaire 'chuis'. Articulez 'je suis'.", SEV_MINOR, "colloquial_slang", "Niveau de Langue Oral"),
    ],
    "de": [
        # Subject-verb agreement
        (r"\b(wir)\s+(ist|bin|bist|hat|kann)\b", "sind / haben / können", "Plural 'wir' verlangt Pluralverb ('wir sind', 'wir haben', 'wir können').", SEV_SERIOUS, "subject_verb_mismatch", "Subjekt-Verb-Kongruenz"),
        (r"\b(sie)\s+(bin|bist)\b", "ist / sind", "Falsche Verbkonjugation nach 'sie'.", SEV_SERIOUS, "subject_verb_mismatch", "Subjekt-Verb-Kongruenz"),
        (r"\b(ich)\s+(bist|sind|ist|habt)\b", "bin / habe", "1. Person Singular 'ich' erfordert 'bin' oder 'habe'.", SEV_SERIOUS, "subject_verb_mismatch", "Subjekt-Verb-Kongruenz"),
        (r"\b(du)\s+(ist|sind|hat|haben)\b", "bist / hast", "2. Person Singular 'du' erfordert 'bist' oder 'hast'.", SEV_SERIOUS, "subject_verb_mismatch", "Subjekt-Verb-Kongruenz"),
        # Preposition & Case
        (r"\bwegen\s+(dem|den)\b", "wegen des / der", "Präposition 'wegen' verlangt im gehobenen Vortragsstil den Genitiv ('wegen des/der').", SEV_MINOR, "preposition_error", "Präpositions-Kasus"),
        (r"\bmit\s+(den|das)\s+(mann|frau|kind|team)\b", "mit dem / der", "'Mit' verlangt stets den Dativ ('mit dem Mann/Team', 'mit der Frau').", SEV_MODERATE, "preposition_error", "Präpositions-Kasus"),
        # Colloquialisms
        (r"\bnen\b", "einen", "Umgangssprachliches 'nen'. Artikulieren Sie 'einen'.", SEV_MINOR, "colloquial_slang", "Umgangssprache"),
        (r"\bne\b", "eine", "Umgangssprachliches 'ne'. Artikulieren Sie 'eine'.", SEV_MINOR, "colloquial_slang", "Umgangssprache"),
        (r"\bisses\b", "ist es", "Zusammenziehung 'isses'. Deutlich 'ist es' sprechen.", SEV_MINOR, "colloquial_slang", "Umgangssprache"),
        (r"\bgemma\b", "gehen wir", "Mundartliches 'gemma'. Sagen Sie 'gehen wir'.", SEV_MINOR, "colloquial_slang", "Umgangssprache"),
    ],
    "hi": [
        # Gender agreement with verbs
        (r"\b(लड़की|महिला|औरत|माँ|माताजी|बहन|बेटी)\s+.*?\s+(जा\s+रहा\s+है|कर\s+रहा\s+है|बोल\s+रहा\s+है|गया|सोच\s+रहा\s+है)\b", "जा रही है / कर रही है / गई", "स्त्रीलिंग कर्ता के साथ क्रिया का स्त्रीलिंग रूप ('रही है / गई') होना चाहिए।", SEV_SERIOUS, "gender_agreement", "लिंग-क्रिया अन्वय (Gender Agreement)"),
        (r"\b(लड़का|पुरुष|आदमी|पिता|पिताजी|भाई|बेटा)\s+.*?\s+(जा\s+रही\s+है|कर\s+रही\s+है|बोल\s+रही\s+है|गई)\b", "जा रहा है / कर रहा है / गया", "पुल्लिंग कर्ता के साथ क्रिया का पुल्लिंग रूप ('रहा है / गया') होना चाहिए।", SEV_SERIOUS, "gender_agreement", "लिंग-क्रिया अन्वय (Gender Agreement)"),
        # Plural concordance
        (r"\b(लोग|बच्चे|लोगो|छात्रगण|श्रोतागण)\s+.*?\s+(जा\s+रहा\s+है|खेल\s+रहा\s+है|आ\s+रहा\s+है|था)\b", "रहे हैं / थे", "बहुवचन कर्ता के साथ बहुवचन क्रिया ('रहे हैं / थे') का प्रयोग करें।", SEV_SERIOUS, "subject_verb_mismatch", "वचन-क्रिया अन्वय (Plural Concordance)"),
        # Subject-auxiliary consistency
        (r"\bहम\s+जाता\s+हूँ\b", "हम जाते हैं / मैं जाता हूँ", "कर्ता और सहायक क्रिया का असंगत प्रयोग। 'मैं जाता हूँ' या 'हम जाते हैं' कहें।", SEV_MODERATE, "subject_verb_mismatch", "कर्ता-सहायक क्रिया अन्वय"),
        (r"\bमैं\s+जाते\s+हैं\b", "मैं जाता हूँ", "'मैं' के साथ 'जाता हूँ' का प्रयोग करें।", SEV_MODERATE, "subject_verb_mismatch", "कर्ता-सहायक क्रिया अन्वय"),
        (r"\bआप\s+करो\b", "आप कीजिए / आप करें", "आदरसूचक 'आप' के साथ शिष्ट रूप 'कीजिए' या 'करें' का प्रयोग करें।", SEV_MODERATE, "honorific_agreement", "आदरसूचक अन्वय (Honorific)"),
    ],
    "ta": [
        # Honorific concordance
        (r"\b(அவர்|அவர்கள்|ஆசிரியர்|தலைவர்|பெரியவர்)\s+.*?\s+(போனான்|வந்தான்|செய்தான்|சொன்னான்)\b", "போனார் / வந்தார் / செய்தார் / சொன்னார்", "உயர் திணை மற்றும் மரியாதைப் பெயருக்கு பலர்பால்/மரியாதைப் பால் வினைமுற்று ('-ஆர் / -ஆர்கள்') அமைய வேண்டும்.", SEV_SERIOUS, "honorific_agreement", "திணை & மரியாதை பொருத்தம் (Honorific Concord)"),
        # Subject-verb agreement
        (r"\bநாங்கள்\s+.*?\s+(வந்தேன்|போனேன்|செய்தேன்)\b", "வந்தோம் / போனோம் / செய்தோம்", "தன்மையின் பன்மை எழுவாய் 'நாங்கள்' என்பதால் வினைமுற்று '-ஓம்' ('வந்தோம்') என அமைய வேண்டும்.", SEV_SERIOUS, "subject_verb_mismatch", "எழுவாய்-பயனிலை பொருத்தம் (Subject-Verb)"),
        (r"\bநான்\s+.*?\s+(வந்தோம்|போனோம்|செய்வோம்)\b", "வந்தேன் / போனேன் / செய்தேன்", "தன்மை ஒருமை எழுவாய் 'நான்' வினைமுற்று '-ஏன்' ('வந்தேன்') என அமைய வேண்டும்.", SEV_SERIOUS, "subject_verb_mismatch", "எழுவாய்-பயனிலை பொருத்தம் (Subject-Verb)"),
        (r"\bஅவன்\s+.*?\s+(வந்தாள்|போனாள்)\b", "வந்தான் / போனான்", "ஆண்பால் எழுவாய்க்கு ஆண்பால் வினைமுற்று அமைய வேண்டும்.", SEV_SERIOUS, "gender_agreement", "பால் பொருத்தம் (Gender Agreement)"),
        (r"\bஅவள்\s+.*?\s+(வந்தான்|போனான்)\b", "வந்தாள் / போனாள்", "பெண்பால் எழுவாய்க்கு பெண்பால் வினைமுற்று அமைய வேண்டும்.", SEV_SERIOUS, "gender_agreement", "பால் பொருத்தம் (Gender Agreement)"),
        # Spoken vs Formal oratorical
        (r"\bபண்ணிட்டு\b", "செய்துவிட்டு", "மேடைப் பேச்சில் பேச்சு வழக்கு 'பண்ணிட்டு' என்பதற்குப் பதிலாக 'செய்துவிட்டு' எனப் பேசுவது சிறப்பாகும்.", SEV_MINOR, "colloquial_slang", "பேச்சு வழக்குச் சொல்"),
        (r"\bசொல்லிட்டு\b", "கூறிவிட்டு / சொல்லிவிட்டு", "முறையான மேடைப் பேச்சில் 'கூறிவிட்டு' எனப் பயன்படுத்துங்கள்.", SEV_MINOR, "colloquial_slang", "பேச்சு வழக்குச் சொல்"),
    ],
    "zh": [
        # Measure word agreement (量词搭配)
        (r"一(个)\s*(书|电脑|车|汽车|飞机|马|鱼)\b", "一本/台/辆/架/匹/条 {1}", "汉语量词搭配不当。请根据名词使用专用量词：一本书、一台电脑、一辆汽车、一架飞机、一匹马、一条鱼，而非泛用'个'。", SEV_SERIOUS, "measure_word_error", "量词搭配不当 (Measure Word)"),
        (r"两(个)\s*(车|汽车|飞机|马)\b", "两辆/架/匹 {1}", "请使用准确专用量词：两辆汽车、两架飞机、两匹马。", SEV_SERIOUS, "measure_word_error", "量词搭配不当 (Measure Word)"),
        # Redundant negative (双重否定误用)
        (r"\b不没有\b", "没有", "双重否定词叠加错误：'不没有'属语法语病，请直接使用'没有'。", SEV_SERIOUS, "double_negative", "双重否定语病 (Redundant Negation)"),
        # Oral Stutter / Repetitive verbal tick (口头禅/口误重复)
        (r"\b然后然后\b", "然后", "连续重复连词'然后然后'，反映口头语言犹豫。请在句际进行清晰的气息停顿。", SEV_MINOR, "stutter_repetition", "口头重复与停顿 (Repetition)"),
        (r"\b那个那个\b", "那个", "连续填充词'那个那个'会稀释演讲权威感。请坚定表达或静默留白。", SEV_MINOR, "colloquial_slang", "填充词过多 (Verbal Tick)"),
        (r"\b就是说就是说\b", "也就是说", "连词口癖重复。正式演说建议使用'也就是说'或'换言之'。", SEV_MINOR, "colloquial_slang", "口头禅 (Colloquialism)"),
        # Verb-noun collocation (动宾搭配)
        (r"\b增加水平\b", "提高水平", "动宾搭配不当：'水平'通常搭配'提高'或'提升'，而非'增加'。", SEV_MODERATE, "preposition_error", "动宾搭配不当 (Collocation)"),
        (r"\b解决缺点\b", "克服缺点 / 解决问题", "动宾搭配不当：通常表述为'克服缺点'或'解决问题'。", SEV_MODERATE, "preposition_error", "动宾搭配不当 (Collocation)"),
    ],
    "ja": [
        # Particle errors (格助詞の誤用)
        (r"(東京|大阪|学校|会社|駅)\s*で\s*(行く|向かう|進む)\b", "{0} に / へ {1}", "移動の帰着点や方向を示す格助詞は「に」または「へ」です。「で」は手段や場所を表すため誤用となります。", SEV_SERIOUS, "particle_error", "格助詞の誤用 (Particle Error)"),
        (r"(ご飯|水|本|お茶)\s*に\s*(食べる|飲む|読む)\b", "{0} を {1}", "他動詞の直接の対象には格助詞「を」を用います。「に」は不適切です。", SEV_SERIOUS, "particle_error", "格助詞の誤用 (Particle Error)"),
        # Colloquialisms & slang in formal speech (改まった場での若者言葉・俗語)
        (r"\b超\b", "非常に / 極めて", "「超」はくだけた口語表現です。公式なスピーチでは「非常に」「極めて」をお使いください。", SEV_MINOR, "colloquial_slang", "口語・俗語 (Colloquial Slang)"),
        (r"\bマジで\b", "本当に / 誠に", "「マジで」は過度に砕けた俗語です。「本当に」「誠に」と発音しましょう。", SEV_MODERATE, "colloquial_slang", "口語・俗語 (Colloquial Slang)"),
        (r"\bやっぱ\b", "やはり / 予想通り", "促音化のくだけた表現です。「やはり」と端正に発音してください。", SEV_MINOR, "colloquial_slang", "促音短縮口語 (Slang)"),
        (r"\b全然いい\b", "問題ございません / 大丈夫です", "スピーチでの「全然いい」は稚拙な印象を与えます。「問題ございません」と洗練された表現を選びましょう。", SEV_MINOR, "colloquial_slang", "言葉遣い (Speech Polish)"),
    ],
    "it": [
        # Subject-verb agreement
        (r"\b(noi)\s+(è|ha|va|fa|dice)\b", "siamo / abbiamo / andiamo / facciamo / diciamo", "Il pronome plurale 'noi' richiede la prima persona plurale del verbo.", SEV_SERIOUS, "subject_verb_mismatch", "Accordo Soggetto-Verbo"),
        (r"\b(loro)\s+(è|ha|va|fa|parla)\b", "sono / hanno / vanno / fanno / parlano", "Il soggetto plurale 'loro' richiede il verbo alla 3ª persona plurale.", SEV_SERIOUS, "subject_verb_mismatch", "Accordo Soggetto-Verbo"),
        (r"\b(io)\s+(è|ha|va|siamo)\b", "sono / ho / vado", "Il pronome 'io' richiede la 1ª persona singolare.", SEV_SERIOUS, "subject_verb_mismatch", "Accordo Soggetto-Verbo"),
        (r"\b(la\s+gente)\s+(sono|hanno|vanno|fanno)\b", "la gente è / ha / va / fa", "'La gente' è un sostantivo collettivo singolare e concorda al singolare.", SEV_MODERATE, "subject_verb_mismatch", "Accordo Soggetto-Verbo"),
        # Gender agreement
        (r"\b(il|un)\s+(casa|mano|foto|notte|città|donna)\b", "la {1}", "'{1}' è femminile; utilizzare 'la/una {1}'.", SEV_MODERATE, "gender_agreement", "Accordo di Genere"),
        (r"\b(la|una)\s+(problema|tema|sistema|programma|giorno|uomo)\b", "il {1}", "'{1}' è maschile; utilizzare 'il/un {1}'.", SEV_MODERATE, "gender_agreement", "Accordo di Genere"),
        # Colloquialisms
        (r"\bboh\b", "non saprei / non è chiaro", "Interiezione informale 'boh'. In un discorso pubblico utilizzare 'non saprei' o 'non è chiaro'.", SEV_MINOR, "colloquial_slang", "Registro Oratorio Informale"),
    ],
    "pt": [
        # Subject-verb agreement
        (r"\b(nós)\s+(vai|foi|tem|faz|é|está)\b", "vamos / fomos / temos / fazemos / somos / estamos", "O pronome 'nós' exige verbo na primeira pessoa do plural (ex: 'nós vamos', não 'nós vai').", SEV_SERIOUS, "subject_verb_mismatch", "Concordância Sujeito-Verbo"),
        (r"\b(a\s+gente)\s+(vamos|fomos|temos|fazemos)\b", "a gente vai / foi / tem / faz", "A locução 'a gente' concorda na 3ª pessoa do singular ('a gente vai', não 'a gente vamos').", SEV_MODERATE, "subject_verb_mismatch", "Concordância Sujeito-Verbo"),
        (r"\b(eles|elas|vocês)\s+(é|está|tem|faz|vai)\b", "são / estão / têm / fazem / vão", "Sujeito plural exige verbo na 3ª pessoa do plural.", SEV_SERIOUS, "subject_verb_mismatch", "Concordância Sujeito-Verbo"),
        (r"\b(eu)\s+(é|vai|tem|faz|está)\b", "sou / vou / tenho / faço / estou", "O pronome 'eu' exige verbo na 1ª pessoa do singular.", SEV_SERIOUS, "subject_verb_mismatch", "Concordância Sujeito-Verbo"),
        # Gender concordance
        (r"\b(o|um)\s+(casa|vida|noite|cidade|mulher|pessoa)\b", "a {1}", "'{1}' é feminino; use 'a/uma {1}'.", SEV_MODERATE, "gender_agreement", "Concordância de Gênero"),
        (r"\b(a|uma)\s+(problema|sistema|tema|programa|dia|homem)\b", "o {1}", "'{1}' é masculino; use 'o/um {1}'.", SEV_MODERATE, "gender_agreement", "Concordância de Gênero"),
        # Preposition & Collocation
        (r"\bassistir\s+o\s+(filme|jogo|vídeo|debate)\b", "assistir ao {0}", "No sentido de ver/presenciar, o verbo 'assistir' é transitivo indireto: 'assistir ao {0}'.", SEV_MODERATE, "preposition_error", "Regência Verbal"),
        (r"\bchegar\s+em\s+(casa|escola|trabalho|são\s+paulo|paris)\b", "chegar a / ao", "Na norma culta oratória, verbos de movimento exigem a preposição 'a' ('chegar a casa').", SEV_MINOR, "preposition_error", "Regência Verbal"),
        # Slang & Colloquial apocope
        (r"\bpra\b", "para", "Forma reduzida coloquial 'pra'. Pronuncie 'para' na oratória formal.", SEV_MINOR, "colloquial_slang", "Registro Coloquial"),
        (r"\btô\b", "estou", "Apócope oral 'tô'. Articule 'estou' com clareza.", SEV_MINOR, "colloquial_slang", "Registro Coloquial"),
        (r"\btá\b", "está", "Apócope oral 'tá'. Articule 'está'.", SEV_MINOR, "colloquial_slang", "Registro Coloquial"),
        (r"\bcê\b", "você", "Forma reduzida 'cê'. Articule 'você'.", SEV_MINOR, "colloquial_slang", "Registro Coloquial"),
    ],
}


# ==============================================================================
# HELPER UTILITIES
# ==============================================================================

def split_into_sentences(text: str) -> List[str]:
    """Splits speech transcript into individual sentence units while preserving readability."""
    if not text:
        return []
    # Split on standard punctuation or long clause markers
    raw_sentences = re.split(r"(?<=[.?!])\s+", text.strip())
    sentences = [s.strip() for s in raw_sentences if s.strip()]
    if not sentences and text.strip():
        sentences = [text.strip()]
    return sentences


def find_token_timestamps(word_tokens: List[Dict[str, Any]], target_phrase: str, default_duration: float = 30.0) -> Tuple[float, float]:
    """
    Finds best matching timestamp range [start, end] for a matched phrase within word tokens.
    """
    if not word_tokens:
        return 0.0, min(3.0, default_duration)

    phrase_words = [re.sub(r"[^\w]", "", w).lower() for w in target_phrase.split() if re.sub(r"[^\w]", "", w)]
    if not phrase_words:
        return 0.0, min(3.0, default_duration)

    tok_words = [re.sub(r"[^\w]", "", t.get("word", "")).lower() for t in word_tokens]

    # Search for contiguous sub-sequence
    target_len = len(phrase_words)
    for i in range(len(tok_words) - target_len + 1):
        if tok_words[i : i + target_len] == phrase_words:
            start_t = word_tokens[i].get("start", 0.0)
            end_t = word_tokens[i + target_len - 1].get("end", start_t + 0.5)
            return round(start_t, 2), round(end_t, 2)

    # Partial match fallback (first word match)
    first_w = phrase_words[0]
    for i, tw in enumerate(tok_words):
        if tw == first_w:
            start_t = word_tokens[i].get("start", 0.0)
            end_idx = min(len(word_tokens) - 1, i + target_len)
            end_t = word_tokens[end_idx].get("end", start_t + 0.5 * target_len)
            return round(start_t, 2), round(end_t, 2)

    return 0.0, min(3.0, default_duration)


# ==============================================================================
# CORE GRAMMAR & SYNTACTIC ANALYSIS
# ==============================================================================

def analyze_grammar(
    transcript_words: List[Dict[str, Any]],
    full_text: str,
    duration: float,
    target_language: str = "en"
) -> Dict[str, Any]:
    """
    Deep grammatical & syntactic analysis engine for spoken delivery.
    Returns:
    - grammar_score: 0-100 score calibrated against detected faults
    - fluency_rating: Descriptive tier (Native/Mastery, Proficient, Developing, Urgent Remediation)
    - error_density: Errors per 100 spoken words
    - grammar_issues: Detailed list of issues with 4-question feedback
    - sentences: Sentence breakdown with syntax validation tags
    - corrected_transcript: Reconstructed clean transcript
    - stats: Breakdown of grammatical error categories
    """
    lang = target_language if target_language in ("en", "es", "fr", "de", "hi", "ta", "zh", "ja", "it", "pt") else "en"
    text = (full_text or "").strip()
    words = text.split()
    total_words = max(1, len(words))

    grammar_issues = []
    seen_spans = set()  # avoid duplicate overlapping matches

    # --------------------------------------------------------------------------
    # Check 1: Duplicate Spoken Words (Stutters / False Starts)
    # --------------------------------------------------------------------------
    for idx in range(len(words) - 1):
        w1 = re.sub(r"[^\w]", "", words[idx]).lower()
        w2 = re.sub(r"[^\w]", "", words[idx + 1]).lower()
        # Exclude valid repetitive words like 'that that' in specific clauses, or short filler bursts
        if w1 and w1 == w2 and len(w1) > 1 and w1 not in ("very", "really", "so"):
            dup_phrase = f"{words[idx]} {words[idx+1]}"
            s_t, e_t = find_token_timestamps(transcript_words, dup_phrase, duration)
            span_key = (round(s_t, 1), w1)
            if span_key not in seen_spans:
                seen_spans.add(span_key)
                grammar_issues.append({
                    "category": "grammar",
                    "type": "duplicate_word",
                    "error_type": "Duplicate Spoken Word / Stutter",
                    "original_text": dup_phrase,
                    "corrected_text": words[idx],
                    "start": s_t,
                    "end": e_t,
                    "severity": SEV_MINOR,
                    "points_deducted": 3.0,
                    "what": f"Duplicated word repetition ('{dup_phrase}')",
                    "why": f"Repeated '{w1}' in immediate succession at {s_t}s, indicating vocal hesitation or false start.",
                    "how": f"Commit to the word once. Pause silently before the phrase if you need time to structure your thought.",
                    "explanation": f"Inadvertently repeating '{w1}' disrupts rhythm and weakens perceived executive presence."
                })

    # --------------------------------------------------------------------------
    # Check 2: English Grammatical Pattern Rules
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # Check 2: English Grammatical Pattern Rules
    # Evaluated when language is English or when transcript contains English speech
    # --------------------------------------------------------------------------
    has_english_tokens = lang == "en" or lang == "auto" or any(w in text.lower().split() for w in ("the", "is", "are", "have", "has", "did", "we", "he", "she", "they", "i", "good", "morning", "to", "you", "gonna"))
    if has_english_tokens:
        all_pattern_groups = [
            ("Subject-Verb Agreement", SUBJECT_VERB_PATTERNS),
            ("Tense & Verb Form", TENSE_VERB_PATTERNS),
            ("Article & Determiner", ARTICLE_PATTERNS),
            ("Preposition & Collocation", PREPOSITION_PATTERNS),
            ("Double Negative", DOUBLE_NEGATIVE_PATTERNS),
            ("Pronoun Case & Structure", PRONOUN_PATTERNS),
            ("Colloquialism & Informal Slang", SLANG_PATTERNS),
        ]

        for group_name, patterns in all_pattern_groups:
            for pat_tuple in patterns:
                pat_regex = pat_tuple[0]
                replacement_tpl = pat_tuple[1]
                explanation_tpl = pat_tuple[2]
                severity = pat_tuple[3]
                issue_type = pat_tuple[4]

                for m in re.finditer(pat_regex, text, flags=re.IGNORECASE):
                    matched_str = m.group(0)
                    groups = m.groups()
                    try:
                        corrected_str = replacement_tpl.format(*groups) if groups else replacement_tpl
                        exp_str = explanation_tpl.format(*groups) if groups else explanation_tpl
                    except Exception:
                        corrected_str = replacement_tpl
                        exp_str = explanation_tpl

                    s_t, e_t = find_token_timestamps(transcript_words, matched_str, duration)
                    span_key = (round(s_t, 1), matched_str.lower())
                    if span_key not in seen_spans:
                        seen_spans.add(span_key)

                        # Calibrated point penalty by severity
                        pts = 6.0 if severity == SEV_SERIOUS else (4.0 if severity == SEV_MODERATE else 2.5)

                        grammar_issues.append({
                            "category": "grammar",
                            "type": issue_type,
                            "error_type": group_name,
                            "original_text": matched_str,
                            "corrected_text": corrected_str,
                            "start": s_t,
                            "end": e_t,
                            "severity": severity,
                            "points_deducted": pts,
                            "what": f"{group_name}: '{matched_str}' → '{corrected_str}'",
                            "why": exp_str,
                            "how": f"Replace '{matched_str}' with '{corrected_str}' for polished oratorical clarity.",
                            "explanation": exp_str
                        })

    # --------------------------------------------------------------------------
    # Check 3: Multilingual Rules (for non-English target languages)
    # --------------------------------------------------------------------------
    if lang in MULTILINGUAL_GRAMMAR_RULES:
        for rule_tuple in MULTILINGUAL_GRAMMAR_RULES[lang]:
            pat_regex = rule_tuple[0]
            replacement_tpl = rule_tuple[1]
            exp_str = rule_tuple[2]
            severity = rule_tuple[3]
            issue_type = rule_tuple[4]
            group_name = rule_tuple[5] if len(rule_tuple) > 5 else "Grammar & Syntax"

            for m in re.finditer(pat_regex, text, flags=re.IGNORECASE):
                matched_str = m.group(0)
                groups = m.groups()
                try:
                    corrected_str = replacement_tpl.format(*groups) if groups else replacement_tpl
                    exp_formatted = exp_str.format(*groups) if groups else exp_str
                except Exception:
                    corrected_str = replacement_tpl
                    exp_formatted = exp_str

                s_t, e_t = find_token_timestamps(transcript_words, matched_str, duration)
                span_key = (round(s_t, 1), matched_str.lower())
                if span_key not in seen_spans:
                    seen_spans.add(span_key)
                    pts = 6.0 if severity == SEV_SERIOUS else (4.0 if severity == SEV_MODERATE else 2.5)
                    grammar_issues.append({
                        "category": "grammar",
                        "type": issue_type,
                        "error_type": group_name,
                        "original_text": matched_str,
                        "corrected_text": corrected_str,
                        "start": s_t,
                        "end": e_t,
                        "severity": severity,
                        "points_deducted": pts,
                        "what": f"{group_name}: '{matched_str}' → '{corrected_str}'",
                        "why": exp_formatted,
                        "how": f"Use '{corrected_str}' for oratorical precision.",
                        "explanation": exp_formatted
                    })

    # --------------------------------------------------------------------------
    # Check 4: Spoken Run-On Sentences (> 28 words without breathing/punctuation)
    # --------------------------------------------------------------------------
    sentences_raw = split_into_sentences(text)
    for sent in sentences_raw:
        sent_words = sent.split()
        if len(sent_words) > 28:
            s_t, e_t = find_token_timestamps(transcript_words, " ".join(sent_words[:6]), duration)
            span_key = (round(s_t, 1), "run_on")
            if span_key not in seen_spans:
                seen_spans.add(span_key)
                grammar_issues.append({
                    "category": "grammar",
                    "type": "run_on_sentence",
                    "error_type": "Spoken Run-On / Overextended Sentence",
                    "original_text": sent[:80] + ("..." if len(sent) > 80 else ""),
                    "corrected_text": "Split into two balanced sentences (12–16 words each)",
                    "start": s_t,
                    "end": min(duration, s_t + len(sent_words) * 0.45),
                    "severity": SEV_MODERATE,
                    "points_deducted": 4.5,
                    "what": f"Run-on spoken sentence ({len(sent_words)} words)",
                    "why": f"Spoken sentence contains {len(sent_words)} words without structural punctuation or respiratory break, degrading listener retention.",
                    "how": "Split this compound thought into two punchy, self-contained statements.",
                    "explanation": "Long spoken run-ons fatigue listeners and cause vocal inflection to fall flat toward the end of phrases."
                })

    # --------------------------------------------------------------------------
    # Construct Sentence Breakdown & Reconstructed Corrected Text
    # --------------------------------------------------------------------------
    sentences_data = []
    corrected_full_text = text

    # Apply corrections from longest to shortest to avoid offset corruption
    sorted_issues_for_repl = sorted(grammar_issues, key=lambda x: len(x.get("original_text", "")), reverse=True)
    for iss in sorted_issues_for_repl:
        orig = iss.get("original_text", "")
        corr = iss.get("corrected_text", "")
        if orig and corr and orig in corrected_full_text and not corr.startswith("Split"):
            # Clean case-insensitive replacement of whole phrase
            pattern = re.compile(re.escape(orig), re.IGNORECASE)
            corrected_full_text = pattern.sub(corr, corrected_full_text, count=1)

    for idx, s in enumerate(sentences_raw, start=1):
        matching_faults = [iss for iss in grammar_issues if iss.get("original_text", "").lower() in s.lower()]
        s_words = s.split()
        s_t, e_t = find_token_timestamps(transcript_words, " ".join(s_words[:4]), duration) if s_words else (0.0, 0.0)

        # Highlight faults inside sentence for rich UI display
        highlighted_html = s
        for mf in matching_faults:
            orig = mf.get("original_text", "")
            if orig:
                sev_color = "#f43f5e" if mf.get("severity") == SEV_SERIOUS else ("#fbbf24" if mf.get("severity") == SEV_MODERATE else "#38bdf8")
                repl_span = f'<span class="grammar-error-inline" style="background:{sev_color}22; color:{sev_color}; text-decoration:line-through; font-weight:700; border-bottom:2px dashed {sev_color}; padding:0 3px; border-radius:3px;" title="{mf.get("what", "")}">{orig}</span> <span class="grammar-corr-inline" style="background:#10b98122; color:#10b981; font-weight:700; padding:0 4px; border-radius:3px;">({mf.get("corrected_text", "")})</span>'
                highlighted_html = highlighted_html.replace(orig, repl_span)

        sentences_data.append({
            "id": idx,
            "sentence": s,
            "highlighted_html": highlighted_html,
            "has_faults": len(matching_faults) > 0,
            "faults_count": len(matching_faults),
            "start": s_t,
            "end": e_t,
            "faults": matching_faults
        })

    # --------------------------------------------------------------------------
    # Calibrate Grammar Score & Fluency Rating
    # --------------------------------------------------------------------------
    error_count = len(grammar_issues)
    error_density = round((error_count / total_words) * 100.0, 1) if total_words > 0 else 0.0

    # Severity distribution
    sev_counts = {SEV_MINOR: 0, SEV_MODERATE: 0, SEV_SERIOUS: 0}
    for iss in grammar_issues:
        sev_counts[iss.get("severity", SEV_MODERATE)] += 1

    # Dynamic Grammar Score Deductions:
    # Baseline: 100
    # Minor faults: -3 pts each
    # Moderate faults: -6 pts each
    # Serious faults: -10 pts each
    # Density penalty compounding if error density > 4%
    density_mult = 1.0 + max(0.0, (error_density - 3.0) * 0.15)
    raw_deductions = (sev_counts[SEV_MINOR] * 3.0 + sev_counts[SEV_MODERATE] * 6.0 + sev_counts[SEV_SERIOUS] * 10.0) * density_mult
    grammar_score = int(max(30, min(100, round(100.0 - raw_deductions)))) if total_words >= 5 else 100

    if grammar_score >= 93:
        fluency_rating = "Pristine / Executive Grade"
        fluency_badge = "Excellent"
        fluency_color = "#10b981"
    elif grammar_score >= 82:
        fluency_rating = "Proficient / Minor Colloquialisms"
        fluency_badge = "Good"
        fluency_color = "#38bdf8"
    elif grammar_score >= 68:
        fluency_rating = "Developing / Frequent Syntax Slips"
        fluency_badge = "Needs Attention"
        fluency_color = "#fbbf24"
    else:
        fluency_rating = "Remedial / Multiple Structural Faults"
        fluency_badge = "Critical Polish Needed"
        fluency_color = "#f43f5e"

    # Category tally for breakdown
    stats_tally = {}
    for iss in grammar_issues:
        et = iss.get("error_type", "General Grammar")
        stats_tally[et] = stats_tally.get(et, 0) + 1

    return {
        "grammar_score": grammar_score,
        "fluency_rating": fluency_rating,
        "fluency_badge": fluency_badge,
        "fluency_color": fluency_color,
        "error_count": error_count,
        "total_words": total_words,
        "error_density_per_100_words": error_density,
        "severity_counts": {
            "minor": sev_counts[SEV_MINOR],
            "moderate": sev_counts[SEV_MODERATE],
            "serious": sev_counts[SEV_SERIOUS],
        },
        "points_deducted": round(raw_deductions, 1),
        "issues": sorted(grammar_issues, key=lambda x: (x.get("start", 0.0), x.get("severity", 1))),
        "sentences": sentences_data,
        "corrected_transcript": corrected_full_text,
        "error_type_stats": stats_tally,
        "summary": (
            f"Evaluated {total_words} spoken words across {len(sentences_raw)} sentences. "
            + (f"Identified {error_count} grammatical/structural opportunities (-{round(raw_deductions, 1)} pts). "
               if error_count > 0 else "Speech demonstrated immaculate grammatical syntax and professional diction. ")
            + f"Current fluency tier: {fluency_rating}."
        )
    }
