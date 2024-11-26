# https://github.com/MaartenGr/KeyBERT

from keybert import KeyBERT

class KeywordExtractor:
    '''Use th is class to extract keywords from a string'''
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