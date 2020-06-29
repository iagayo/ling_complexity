# ling_complexity

This library generates a series of metrics related to linguistic complexity for European Portuguese.
The metrics have been used in studies dealing with linguistic complexity.

The set of lexical sophistication metrics is based on Lu 2012 and the set of syntactic metrics on Lu 2011. <br />
Sophistication is calculated using a list of frequencies extracted from [Procura-PALavras (P-PAL)](http://p-pal.di.uminho.pt/tools). The list comprises words with a frequency > 0.0006. <br />
Syllabes are counted using [LX Syllabifier](http://lxsyllabifier.di.fc.ul.pt/). <br />

Complexity can be used with other languages simply adding a new vocabulary list (modify the sophistication.py module) and an appropriate syllabizer (modify the descriptive.py module).  <br />

For readability, the library uses the Flesch reading ease adaptation for Brazilian Portuguese developed by Martins 1996. It basically consists on a shift of 42 points on the result of the original Flesch reading ease formula to compensate for the fact that words in Portuguese typically have a bigger number of syllables. This is the formula:  <br />

FleschPT= 248.835−(1.015×ASL)−(84.6×ASW) <br />

being ASL the average sentence length in words, and ASW the average number of syllables per word. <br />

### Basic Usage
```python
>>> import Complexity as comp
>>> objcomp = comp.text("Esta é uma frase de teste.")
>>> objcomp = comp.text("""
Quando a noite desce e sepulta dentro do manto o perfil austero do castelo de
Fuentes, Fronteira desperta.
Range primeiro a porta do Valentim, e sai por ela, magro, fechado numa roupa
negra de bombazina, um vulto que se perde cinco ou seis passos depois.
A seguir, aponta à escuridão o nariz afilado do Sabino. Parece um rato a surgir
do buraco. Fareja, fareja, hesita, bate as pestanas meia dúzia de vezes a
acostumar­se às trevas, e corre docemente a fechadura do cortelho.
O Rala, de braço bambo da navalhada que o D. José, em Lovios, lhe mandou à
traição, dá sempre uma resposta torta à mãe, quando já no quinteiro ela lhe
recomenda não sei quê lá de dentro.
O Salta, que parece anão, esgueira­se pelos fundos da casa, chega ao cruzeiro,
benze­se, e ninguém lhe põe mais a vista em cima.
A Isabel, sempre com aquele ar de quem vai lavar os cueiros de um filho, sai
quando o relógio de Fuentes, longe e soturnamente, bate as onze. Aparece no
patamar como se nada fosse, toma altura às estrelas, se as há, e some­se
na negrura como os outros.
""")
>>> objcomp.get_metrics()
[{'number_of_tokens': 246, 'number_of_types': 133, 'number_of_words': 210, 'number_of_sentences': 9, 'average_word_lenght': 3.98, 'average_numbword_sentence': 23.33, 'average_numbsyllable_word': 1.84, 'readability_fleschport': 69.25}, {'noun_density': 19.52, 'verb_density': 15.24, 'adj_density': 3.33, 'adv_density': 6.19, 'content_density': 44.29}, {'lexical_variation': 0.93, 'verb_variation': 0.87, 'verb_variation2': 0.29, 'squared_verbvariation': 23.52, 'corrected_verbvariation': 3.43, 'noun_variation': 1.0, 'adjective_variation': 0.08, 'adverb_variation': 0.12, 'modifier_variation': 0.2, 'ttr': 0.7, 'root_ttr': 9.7, 'corrected_ttr': 6.86, 'bilogarithm_ttr': 0.91, 'uber_index': 26.31, 'moving_avrg_ttr': 0.94, 'mean_segmental_ttr': 0.94, 'hdd': 0.88, 'maas': 0.01, 'mtld': 143.49}, {'ls1': 1.0, 'ls2': 1.0, 'vs1': 0.87, 'vs2': 23.52, 'cvs1': 3.43, 'adguiraud': 9.04}, {'sentences': 9, 'words': 210, 't-units': 10, 'clauses': 20, 'dep_clauses': 12, 'complexnps': 8, 'coorphrases': 7, 'nonfinite': 2, 'mean_length_sentence': 23.33, 'mean_length-unit': 21.0, 'mean_length_clause': 10.5, 'clauses_per sentence': 2.22, 'clauses_per_t-unit': 0.5, 'complex_t-units_per_t-unit': 0.5, 'dependent_clauses_per_clause': 0.6, 'dependent_clause_per_t-unit': 1.2, 'coordinate_phrases_per_clause': 0.35, 'coordinate_phrases_per_t-units': 0.7, 't-units_per sentence': 1.11, 'complex_noun_phrase_per_clause': 0.4, 'complex_noun_phrase_per_t-units': 0.8, 'verbalphrases_per_t-unit': 3.1, 'nonfinite_phrases_per_clause': 0.1, 'nonfinite_phrases_per_t-unit': 0.2}]
```

# Dependencies
Complexity requires [NLTK](http://www.nltk.org/) and the [Stanza NLP Library](https://stanfordnlp.github.io/stanza/) with the Portuguese gsd model for the linguistic annotations. <br />
It can be used with a different NLP Library like SpaCy. <br />
In order to do that, SpaCy should be installed and the annotations.py module should be modified. <br />

# Set of implemented metrics:

### Descriptive: basic counts of features. <br />
- number of tokens <br />
- number of types <br />
- number of words <br />
- average word lenght <br />
- average number of syllables per word <br />
- flesch readability index (adapted to Portuguese) <br />

## Part-Of-Speech <br />
- noun density <br />
- verb density <br />
- adj density <br />
- adv density <br />
- lexical density <br />

### Lexical Diversity <br />
- lexical variation <br />
- verb variation <br />
- verb variation2 <br />
- squared verb variation <br />
- corrected verb variation <br />
- noun variation <br />
- adjective variation <br />
- adverb variation <br />
- modifier variation <br />
- TTR <br />
- root TTR <br />
- corrected TTR <br />
- bilogarithm TTR <br />
- Uber index <br />
- moving average TTR <br />
- mean segmental TTR <br />
- HD-D <br />
- Maas <br />
- MTLD <br />

### Lexical Sophistication <br />
- lexical sophistication1 (ls1) <br />
- lexical sophistication2 (ls2) <br />
- verbal sophistication1 (vs1) <br />
- verbal sophistication2 (vs2) <br />
- corrected verbal sophistication (cvs1) <br />
- Adguiraud <br />
 
### Syntactic Sophistication <br />
- number of sentences <br />
- number of t-units <br />
- number of clauses <br />
- number of  dep clauses <br />
- number of complexnps <br />
- number of coorphrases <br />
- number of nonfinite clauses <br />
- mean length sentence <br />
- mean length t-unit <br />
- mean length clause <br />
- clauses per sentence <br />
- clauses per t-unit <br />
- complex t-units per t-unit <br />
- dependent clauses per clause <br />
- dependent clauses per t-unit <br />
- coordinate phrases per clause <br />
- coordinate phrases per t-units <br />
- t-units per sentence <br />
- complex noun phrases per clause <br />
- complex noun phrases per t-units <br />
- verbalphrases per t-unit <br />
- nonfinite phrases per clause <br />
- nonfinite phrases per t-unit <br />

## References

T. B. Martins, C. M. Ghiraldelo, M. d. G. V. Nunes, and O. N. de Oliveira Junior, Readability formulas applied to textbooks in Brazilian Portuguese. IcmscUsp, 1996.  <br />

Lu, X. (2012). The relationship of lexical richness to the quality of ESL learners’ oral narratives. Modern Language Journal, 96(2), 190–208.  <br /> https://doi.org/10.1111/j.1540-4781.2011.01232_1.x   <br />

Lu, X. (2011) A corpus-based evaluation of syntactic complexity measures as indices of college-level ESL writers' language development. TESOL Quarterly, 45(1), 36–62.

