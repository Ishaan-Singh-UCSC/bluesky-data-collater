# https://medium.com/analytics-vidhya/text-summarization-using-bert-gpt2-xlnet-5ee80608e961

from summarizer import Summarizer

class TextSummarizer:
    '''Use this Class to summarize text with bert'''
    def __init__(self):
        self.bert_model = Summarizer()
        
    def summarize_Tweets(self, data, numcores = 1):
        '''Summarizes an array of tweets with BERT
        Takes the tweets as a list of tuples, (anything, "{text to summarize}")
        and returns a list of tuples: (anything, "{text to summarize}", "{text summary}")'''
        summaries = []
        for tweet in data:
            bert_summary = ''.join(self.bert_model(tweet[1], min_length=5))
            # print("BERT SUMMARY:", bert_summary)
            summaries.append((tweet[0],tweet[1],bert_summary))
            
        return summaries