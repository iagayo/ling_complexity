import spacy
import annotations
import re


def two_decimals(formula):
    result = round(formula, 2)
    return result

def syntactic_complexity_metrics(compObj):
    
    doc = annotations.getspacy_stanza(compObj)
    
    #sentences based on the .sents method
    sentences = list(doc.sents)
    
    #words based on tokens that are not punctuation
    words = [token.text for token in doc if token.is_punct != True]
    
    #t-units based on counts of instances of root and second conjunct clauses with subject. 
    tunits = [token for token in doc if token.dep_ == 'root' or (token.head.dep_ == 'conj' and (re.compile("(?:VERB|AUX)").match(token.head.pos_)) and (re.compile("(?:nsubj|csubj)").match(token.dep_)) and token.head.head.dep_ == 'root')]
    
    #complex t-unit: one containing at least one dependent clause
    ctunits = [token for token in doc if re.compile("(?:ccomp|csubj|relcl|advcl|acl|csubj)").match(token.dep_) and token.head.dep_ == 'root']
    
    #Iria: I change Rickard's definion of clause (clauses based on counts of subject relations) because PORT is a pro-drop language
    #clauses = [token for token in doc if token.dep_ == 'nsubj' or token.dep_ == 'csubj' or token.dep_ == 'nsubjpass']
    clauses = [token for token in doc if (re.compile("(?:root|ccomp|csubj|relcl|advcl|acl|csubj)").match(token.dep_)) and (re.compile("(?:VERB|AUX)").match(token.pos_))]
    
    #dependent clauses based on counts on subject relations but excluding the root relation and second conjunct clauses with subject 
    depclauses = [token for token in doc if re.compile("(?:ccomp|csubj|relcl|advcl|acl|csubj)").match(token.dep_) and (re.compile("(?:VERB|AUX)").match(token.pos_))]
    
    #complex noun phrases = noun phrase modified by adjective, relative clause or prepositional phrase, or that has an appositional phrase or a clause that constitutes a subject
    embeddednps = set()
    allcomplexnps = set()
    for token in doc:
        for child in token.children:
            for ancestor in token.ancestors:
                if ((child.dep_ == 'poss' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'nummod' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'relcl' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'amod' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'prep' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'appos' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'compound' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'acl' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or child.head.dep_ == 'csubj') and (ancestor.pos_ == 'NOUN' or ancestor.pos_ == 'PROPN'):
                    embeddednps.add(token)
                elif (child.dep_ == 'poss' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'nummod' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'relcl' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'amod' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'prep' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'appos' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'compound' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or (child.dep_ == 'acl' and (child.head.pos_ == 'NOUN' or child.head.pos_ == 'PROPN')) or child.head.dep_ == 'csubj':
                    allcomplexnps.add(token)
    #complexnps = allcomplexnps - embeddednps
    complexnps = allcomplexnps

    #coordinate phrases ("X and Y"). Counting instances of the cc relation, excluding coordinated clauses. 
    coorphrases = [token for token in doc if token.dep_ == 'cc' and token.head.dep_ != 'root' and token.head.dep_ != 'relcl' and token.head.dep_ != 'advcl' and token.head.dep_ != 'acl']
    
    #nonfinite phrases, including xcomp relations, csubj relations and advcl relations
    nonfinite = [token for token in doc if re.compile(".*(?:xcomp|acl:inf|acl:part|csubj).*").match(token.dep_)  and (token.pos_ == 'VERB' or token.pos_ == 'AUX')]
    
    verbphrases = [token for token in doc if token.pos_ == 'VERB']
    
    ########  Counting the measures ########
    
    return {

        #Sentences
        "sentences": len(sentences),

        #T-units
        "t-units": len(tunits),

        #Clauses
        "clauses": len(clauses),

        #Dependent clauses
        "dep_clauses": len(depclauses),

        #Complex noun phrases
        "complexnps": len(complexnps),

        #Coordinated phrases
        "coorphrases": len(coorphrases),

        #Non-finite phrases
        "nonfinite": len(nonfinite),

        #Words per sentence
        "mean_length_sentence": two_decimals(len(words)/len(sentences)),

        #Mean length of T-unit
        "mean_length-unit": two_decimals(len(words)/len(tunits)),

        #Mean length of clause
        "mean_length_clause": two_decimals((len(words)/len(clauses) if len(clauses) > 0 else 0)),

        #clauses per sentence
        "clauses_per sentence": two_decimals(len(clauses)/len(sentences) if len(clauses) > 0 else 0),

        #clauses per t-unit
        "clauses_per_t-unit": two_decimals(len(tunits)/len(clauses) if len(clauses) > 0 else 0),

        ##IMPLEMENT complex T-units per T-unit (CT/T)
        "complex_t-units_per_t-unit": two_decimals(len(ctunits)/len(tunits) if len(tunits) > 0 else 0),

        #dependent clauses per clause
        "dependent_clauses_per_clause": two_decimals(len(depclauses)/len(clauses) if len(clauses) > 0 else 0),

        #Dependent clause per T-unit
        "dependent_clause_per_t-unit": two_decimals(len(depclauses)/len(tunits) if len(tunits) > 0 else 0),

        #Coordinate phrases per clause
        "coordinate_phrases_per_clause": two_decimals((len(coorphrases)/len(clauses) if len(clauses) > 0 else 0)),
        
        #Coordinate phrases per t-unit
        "coordinate_phrases_per_t-units": two_decimals(len(coorphrases)/len(tunits) if len(tunits) > 0 else 0),

        #T-units per sentence
        "t-units_per sentence": two_decimals(len(tunits)/len(sentences)),

        #Complex noun phrases per clause
        "complex_noun_phrase_per_clause": two_decimals((len(complexnps)/len(clauses) if len(clauses) > 0 else 0)),
        
        #Complex noun phrases per t-unit
        "complex_noun_phrase_per_t-units": two_decimals(len(complexnps)/len(tunits) if len(tunits) > 0 else 0),

        #VPs per t-unit
        "verbalphrases_per_t-unit": two_decimals(len(verbphrases)/len(tunits) if len(tunits) > 0 else 0),

        #####these metrics are not in Lu 2011#####

        #Non-finite element per clause
        "nonfinite_phrases_per_clause": two_decimals((len(nonfinite)/len(clauses) if len(clauses) > 0 else 0)),
        
        #Non-finite element per t-unit
        "nonfinite_phrases_per_t-unit": two_decimals(len(nonfinite)/len(tunits) if len(tunits) > 0 else 0),
        
    }