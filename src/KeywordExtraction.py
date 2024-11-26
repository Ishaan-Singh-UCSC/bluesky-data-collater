# https://github.com/MaartenGr/KeyBERT

from keybert import KeyBERT

class KeywordExtractor:
    '''Use this class to extract keywords from a string'''
    def __init__(self):
        # Excludes commonwords
        self.kw_model = KeyBERT()
    
    def keyword_extraction(self, data, numKeywords=10):
        '''Data: the text as a single string
        NumKeywords: keywordss to find (top_n)
        keyphrase_range: the number of words in the phrases. Minimum and maixmum'''
        keywords = self.kw_model.extract_keywords(data, keyphrase_ngram_range=(1, 3), 
                                                  top_n=numKeywords)
        return keywords

    def keyword_extraction2(self, data, numKeywords=10):
        '''Data: the text as a single string
        NumKeywords: keywordss to find (top_n)
        keyphrase_range: the number of words in the phrases. Minimum and maixmum
        This version has 1 keyword and more diversity'''
        keywords = self.kw_model.extract_keywords(data, keyphrase_ngram_range=(1, 1), 
                                                  top_n=numKeywords, use_mmr=True, diversity=0.7)
        return keywords
    
    def keyword_extraction3(self, data, numKeywords=10):
        '''Data: the text as a single string
        NumKeywords: keywordss to find (top_n)
        keyphrase_range: the number of words in the phrases. Minimum and maixmum
        This version has 1 keyword and more diversity'''
        keywords = self.kw_model.extract_keywords(data, keyphrase_ngram_range=(1, 2), 
                                                  top_n=numKeywords, use_mmr=True, diversity=0.5)
        return keywords
    
    def keyword_extraction4(self, data, numKeywords=10):
        '''Data: the text as a single string
        NumKeywords: keywordss to find (top_n)
        keyphrase_range: the number of words in the phrases. Minimum and maixmum
        This version has 1 keyword and more diversity'''
        keywords = self.kw_model.extract_keywords(data, keyphrase_ngram_range=(1, 1), 
                                                  top_n=numKeywords, use_mmr=True, diversity=0.4)
        return keywords