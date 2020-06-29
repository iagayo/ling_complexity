import nltk.tokenize
import sys
import annotations, descriptive, diversity, sophistication, syntax
import csv
import warnings
warnings.filterwarnings("ignore")
import timeit


def text(text):
    comp = Complexity()
    return comp.text(text)

class Complexity:
    def __init__(self):
        self.tokens=[]
        self.types=[]
        self.postag=[]

    def text(self, text):
        self.doc = []
        self.annotations = []
        self.tokens=[]
        self.types=[]
        self.words = []
        self.postag=[]


        self.text = text
        self.doc = annotations.getstanza(self)
        self.annotations = annotations.get_annotations(self)
        self.tokens = descriptive.get_tokens(self)
        self.types = descriptive.get_types(self)
        self.words = descriptive.get_words(self)
        self.postag = annotations.getpos(self)
        self.lextokens = diversity.lex_tokens(self)



        self.word_count = descriptive.get_numbwords(self)
        self.sentence_count = descriptive.get_numbsent(self)
        self.avg_word_per_sentence = descriptive.avg_word_per_sentence(self)

        return self
    
    def get_metrics(self):
    	metrics = []
    	desc = descriptive.descriptive_metrics(self)
    	metrics.append(desc)
    	morpho = annotations.getpos_counts(self)
    	metrics.append(morpho)
    	ld = diversity.diversity_metrics(self)
    	metrics.append(ld)
    	soph = sophistication.sophistication_metrics(self)
    	metrics.append(soph)
    	syntm = syntax.syntactic_complexity_metrics(self)
    	metrics.append(syntm)
    	return metrics

