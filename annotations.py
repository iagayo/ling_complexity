import spacy
import stanza
from spacy_stanza import StanzaLanguage


nlp = stanza.Pipeline('pt', processors='tokenize,mwt,pos,lemma,depparse', use_gpu=True, pos_batch_size=200, package='gsd')
snlp = StanzaLanguage(nlp)
#nlp = spacy.load('pt_core_news_sm')
#nlp = StanzaLanguage(snlp)

#annotate with spaCy or Stanza

def getspacy(compObj):
	doc = nlp(compObj)
	results = []
	for token in doc:
		dic = {
				"text": token.text,
				"lemma": token.lemma_,
				"upos": token.pos_,
				"tag": token.tag_,
				"dep": token.dep_,
				"head": token.head.dep_
				}
		results.append(dic)
	fresults = []
	fresults.append(results)       
	return fresults

def getspacy_stanza(compObj):
	doc = snlp(compObj.text)
	return doc

def getstanza(compObj):
	doc = nlp(compObj.text)
	compObj.doc = doc
	return doc

def get_annotations(compObj):
	doc = compObj.doc
	dicts = doc.to_dict()
	compObj.annotations = dicts
	return dicts

####get metrics####
def getpos(compObj):
	pos=[]
	for x in compObj.annotations:
		for dic in x:
			for k,v in dic.items():
				if k == 'upos' and v != 'PUNCT':
					pos.append(v)
	compObj.postag = pos
	return pos

def getpos_counts(compObj):
	pos = compObj.postag
	words = len(pos)
	nouns = pos.count('NOUN')
	verbs = pos.count('VERB') + pos.count('AUX')
	adjs = pos.count('ADJ')
	advs = pos.count('ADV')
	content = nouns+verbs+adjs+advs 
	
	pos_metrics = {
	"noun_density": round((nouns/float(words))*100, 2),
	"verb_density": round((verbs/float(words))*100, 2),
	"adj_density": round((adjs/float(words))*100, 2),
	"adv_density": round((advs/float(words))*100, 2),
	"content_density": round((content/float(words))*100, 2)
	}
	return pos_metrics

