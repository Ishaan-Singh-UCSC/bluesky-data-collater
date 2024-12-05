import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from src.JSONParser import JSONParser
import timeit

fp = "Data/data.json"
parser = JSONParser()
parser.parse_json_file_with_path(fp)
text = parser.large_string

# Preprocessing
sentences = sent_tokenize(text)
words = word_tokenize(text.lower())
stop_words = set(stopwords.words('english'))

# Word frequency
word_freq = FreqDist(w for w in words if w not in stop_words and w.isalnum())

# Sentence scoring
sentence_scores = {}
for sentence in sentences:
    for word in word_tokenize(sentence.lower()):
        if word in word_freq:
            if sentence not in sentence_scores:
                sentence_scores[sentence] = 0
            sentence_scores[sentence] += word_freq[word]

# Generate summary
summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:2]
summary = ' '.join(summary_sentences)
print(summary)
