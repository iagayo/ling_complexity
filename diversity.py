from lexicalrichness import LexicalRichness as lr
import descriptive, annotations, sophistication
from math import sqrt, log

####diverstiy variables#####

def lex_tokens(compObj):
    dicts = compObj.annotations
    nountokens = []
    adjtokens = []
    verbtokens = []
    advtokens = []
    for x in dicts:
        for dic in x:
            try:
                if dic['upos'] == 'NOUN':
                    nountokens.append(dic['text'].lower())
                elif dic['upos'] == 'ADJ':
                    adjtokens.append(dic['text'].lower())
                elif dic['upos'] == 'VERB':
                    verbtokens.append(dic['text'].lower())
                elif dic['upos'] == 'ADV':
                    advtokens.append(dic['text'].lower())
            except:
                continue
    lextokens = [nountokens, adjtokens,verbtokens,advtokens]
    compObj.lextokens = lextokens
    
    return lextokens

###metrics###
def diversity_metrics(compObj): 
    lex = lr(compObj.text)
    words = lex.words
    types = lex.terms
    type_token_ratio = lex.ttr
    root_ttr = lex.rttr
    correct_ttr = lex.cttr
    measure_textual_lexical_diversity = lex.mtld(threshold=0.72)
    maas = lex.Maas
    if words <= 25:
        mean_segmental_ttr = 0
        moving_average_ttr = 0
        measure_textual_lexical_diversity = 0
        hpergeometric_distribution_diversity = 0
    elif words > 25:
        mean_segmental_ttr = lex.msttr(segment_window=25)
        moving_average_ttr = lex.mattr(window_size=25)
    if words <= 42:
        hpergeometric_distribution_diversity = 0
    elif words > 42:
        hpergeometric_distribution_diversity = lex.hdd(draws=42)

    l_lextokens = compObj.lextokens
    lextokens = [item for sublist in l_lextokens for item in sublist]
    lextypes = set(lextokens)

    nountokens = l_lextokens[0]
    nountypes = set(nountokens)
    
    adjtokens = l_lextokens[1]
    adjtypes = set(adjtokens)

    verbtokens = l_lextokens[2]
    verbtypes = set(verbtokens)

    advtokens = l_lextokens[3]
    advtypes = set(advtokens)

    nwords = compObj.word_count
    nwordtypes = len(set(compObj.words))

    #lexical variation
    lv =round((len(lextypes)/float(len(lextokens))), 2)

    #noun variation
    try:
        nv = round(len(nountypes)/float(len(nountokens)), 2)
    except ZeroDivisionError:
        nv = 0

    #adj variation
    adjv = round(len(adjtypes)/float(len(lextokens)), 2)

    #adv variation
    advv = round(len(advtypes)/float(len(lextokens)), 2)

    #modifier variation
    modv = round((len(advtypes)+len(adjtypes))/float(len(lextokens)), 2)

    #verb variation
    try:
        vv1 = round(len(verbtypes)/float(len(verbtokens)), 2)
    except ZeroDivisionError:
        vv1 = 0

    #vv2
    vv2 = round(len(verbtypes)/float(len(lextokens)), 2)

    #squared vv1
    try:   
        svv1 = round(len(verbtypes)*len(verbtypes)/float(len(verbtokens)), 2)
    
    except ZeroDivisionError:
        svv1=0

    #corrected vv1
    try:
        cvv1 = round(len(verbtypes)/sqrt(2*len(verbtokens)), 2)
    
    except ZeroDivisionError:
        cvv1 = 0

    #bilog ttr
    logttr = log(nwordtypes)/log(len(compObj.words))

    #uber
    try:
        uber = (log(nwords,10)*log(nwords,10))/log(nwords/float(nwordtypes),10)
    except ZeroDivisionError:
        uber = 0

    d_metrics = {
                "lexical_variation": round(lv,2),
                "verb_variation": round(vv1, 2),
                "verb_variation2": round(vv2, 2),
                "squared_verbvariation": round(svv1,2),
                "corrected_verbvariation": round(cvv1, 2),
                "noun_variation": round(nv, 2),
                "adjective_variation": round(adjv, 2),
                "adverb_variation": round(advv, 2),
                "modifier_variation": round(modv, 2),
                "ttr": round(type_token_ratio, 2),
                "root_ttr": round(root_ttr, 2),
                "corrected_ttr": round(correct_ttr,2),
                "bilogarithm_ttr": round(logttr, 2),
                "uber_index": round(uber, 2),
                "moving_avrg_ttr": round(moving_average_ttr, 2),
                "mean_segmental_ttr": round(mean_segmental_ttr, 2),
                "hdd": round(hpergeometric_distribution_diversity, 2),
                "maas": round(maas, 2),
                "mtld": round(measure_textual_lexical_diversity, 2)
                }
    return d_metrics





