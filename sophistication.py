from __future__ import division
import annotations, descriptive
import string,re,sys,os,random
from math import sqrt,log

# adjust minimum sample size here
standard=50

# Returns the keys of dictionary d sorted by their values
def sort_by_value(d):
    items=d.items()
    backitems=[ [v[1],v[0]] for v in items]
    backitems.sort()
    return [ backitems[i][1] for i in range(0,len(backitems))]

def word_ranks():
	worddict={}
	#wordlistfile=open("/Users/galvan/clul_computer/complexity/frequency_lists_vocabulary/pt_ppa.txt","r") #pt
	wordlistfile=open("./resources/vocabulary/pt_ppa.txt","r") #pt
	wordlist=wordlistfile.readlines()
	wordlistfile.close()
	for word in wordlist:
		wordinfo=word.strip()
		if not wordinfo or "Total words" in wordinfo:
			continue
	infolist=wordinfo.split()
    #I consider words and not lemmas to establish sophistication metrics, contrary to Lu
	lemma=infolist[0]
	frequency=float(infolist[1])
	worddict[lemma]=worddict.get(lemma,0)+frequency
	wordranks=sort_by_value(worddict)
	
	return wordranks


def sophistication_metrics(compObj):

	wordranks = word_ranks()
	
	l_lextokens = compObj.lextokens
	lextokens = [item for sublist in l_lextokens for item in sublist]
	slextokens = [token for token in lextokens if (not token in wordranks[-2000:])]

	words = compObj.words
	wordtypes = set(words)
	swordtypes = [token for token in wordtypes if (not token in wordranks[-2000:])]

	verbtokens = l_lextokens[2]
	sverbtokens = [token for token in verbtokens if (not token in wordranks[-2000:])]
	verbtypes = set(verbtokens)
	sverbtypes = list(set(sverbtokens))

	###calculate metrics###
	#ls1
	try:
		ls1 = round((len(slextokens)/float(len(lextokens))),2)
	except ZeroDivisionError:
		ls1 = 0

	#ls2
	ls2 = len(swordtypes)/float(len(wordtypes))

	#vs1
	try:
		vs1 = len(sverbtypes)/float(len(verbtokens))
	except ZeroDivisionError:
		vs1 = 0

	#vs2
	try:
		vs2 = (len(sverbtypes)*len(sverbtypes)/float(len(verbtokens)))
	except ZeroDivisionError:
		vs2 = 0

	#cvs1
	try:
		cvs1 = len(sverbtypes)/sqrt(2*(len(verbtokens)))
	except ZeroDivisionError:
		cvs1 = 0

	#adguiraud
	adguiraud = len(swordtypes) / sqrt(len(words))

	s_metrics = {
				'ls1': round(ls1, 2),
				'ls2': round(ls2, 2),
				'vs1': round(vs1, 2),
				'vs2': round(vs2,2),
				'cvs1': round(cvs1,2),
				'adguiraud': round(adguiraud, 2)
				}
	
	return s_metrics
	


	