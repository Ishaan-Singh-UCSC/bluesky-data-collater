from transformers import AutoTokenizer
# SRC: https://huggingface.co/learn/nlp-course/en/chapter2/4

class BlueSkyTokenizer:
    def __init__(self):
        return
    
    def convertToTokens_User_Tweet_Tuple(self, data):
        '''Tokenizer for BERT'''
        tokenized_data = []
        tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        for item in data:
            tokens = tokenizer.tokenize(item[1])
            ids = tokenizer.convert_tokens_to_ids(tokens)
            tokenized_data.append((item[0], ids))
        return tokenized_data
