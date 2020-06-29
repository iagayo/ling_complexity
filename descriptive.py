import nltk.tokenize
import annotations
import os, sys
import re
from collections import Counter
sys.path.append("./resources/syllabifier/")
import silabificador



def get_tokens(compObj):
	#dicts = annotations.getspacy(compObj.text)
	#dicts = annotations.getstanza(compObj.text)
	dicts = compObj.annotations
	tokens = []
	for x in dicts:
		for dic in x:
			for k,v in dic.items():
				if k == 'upos':
					tokens.append(dic['text'])
	compObj.tokens = tokens
	return tokens

def get_types(compObj):
	types = set(compObj.tokens)
	compObj.types = types
	return types

def get_numbtokens(compObj):
	"""returns the number of tokens using get_tokens for the number of tokens"""
	numbtokens = len(compObj.tokens)
	return numbtokens


def get_words(compObj):
	#dicts = annotations.getspacy(compObj.text)
	#dicts = annotations.getstanza(compObj.text)
	dicts = compObj.annotations
	tokenwords = []
	for x in dicts:
		for dic in x:
			for k,v in dic.items():
				if k == 'upos' and v != 'PUNCT':
					tokenwords.append(dic['text'])
	compObj.words = tokenwords
	return tokenwords

def get_numbwords(compObj):
	numbwords= len(compObj.words)
	compObj.word_count = numbwords
	return numbwords

def get_tokenwordtypes(compObj):
	tokenwordtypes = set(compObj.words)
	return tokenwordtypes

def get_numbtypes(compObj):
	numbtypes = len(compObj.types)
	return numbtypes


###descriptive metrics###############
def avgWordlength(compObj):
	counts = Counter(compObj.words)
	avgwordlength = float(sum(len(w)*c for w,c in counts.items())) / compObj.word_count
	return avgwordlength


def get_numbsent(compObj):
	""""returns number of sentences based on NLTK"""
	tokenized_sentences = nltk.sent_tokenize(compObj.text.lower())
	numbsent = len(tokenized_sentences)
	compObj.sentence_count = numbsent
	return numbsent	


def avg_word_per_sentence(compObj):
	"""returns average number of words per sentence"""
	avgwordsent = compObj.word_count / compObj.sentence_count
	return avgwordsent	




def getSyllables(compObj):
	"""returns number of syllables per word using separasílabas"""
	numbsyllable=0
	for w in compObj.words:
		try:
			resultado = silabificador.silabifica(w)
			resultado = resultado[1:len(resultado)-1]
			resultado = resultado.replace('!', ' !')
			resultado = resultado.replace('?', ' ?')
			resultado = resultado.replace(';', ' ;')
			resultado = resultado.replace(',', ' ,')
			resultado = resultado.replace(':', ' :')
			resultado = resultado.replace('.', ' .')
			number = resultado.count('|')
			numbsyllable += number+1
		except:
			continue
	return numbsyllable


def avgSyllWord(compObj):
	"""returns average syllables/word"""
	syllab_count = getSyllables(compObj)
	avgsyllabword= (syllab_count / compObj.word_count)
	return avgsyllabword

########READABILITY##########

def readability(compObj):
	asw = avgSyllWord(compObj)
	aws = compObj.avg_word_per_sentence
	return 248.835 - 84.6 * (asw) - 1.015 * (aws)



#### final function that gathers all the descriptive results

def descriptive_metrics(compObj):
	flesch_port = readability(compObj)

	desc_metrics = {

	#"Tokens": compObj.tokens,
	#"Words": compObj.words,
	#"Types": compObj.types,
	"number_of_tokens": get_numbtokens(compObj),
	"number_of_types": get_numbtypes(compObj),
	"number_of_words": compObj.word_count,
	"number_of_sentences": compObj.sentence_count,
	"average_word_lenght": round(avgWordlength(compObj), 2),
	"average_numbword_sentence": round(compObj.avg_word_per_sentence,2),
	"average_numbsyllable_word": round(avgSyllWord(compObj),2),
	"readability_fleschport": round(flesch_port,2),
	}

	return desc_metrics