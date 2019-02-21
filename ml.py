import pandas as pd
import re
import heapq
import nltk
from nltk.tokenize import sent_tokenize
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer

class ml(object):
    def __init__(self,df):
        self.df=df

    def summarize1(self,df):
        #refer https://stackabuse.com/text-summarization-with-nltk-in-python/

        df1=df[(df.conclusion !=  '') & (df.conclusion != 0)]
        df1['conclusion'].fillna("not available",inplace=True)
        df.fillna('0',inplace=True)
        stopwords = nltk.corpus.stopwords.words('english')
        for row in df['conclusion']:
            if row=='0' or row=='':
                continue
            # Removing Square Brackets and Extra Spaces
            print(row)
            article_text = re.sub(r'\[[0-9]*\]', ' ', row)
            article_text = re.sub(r'\s+', ' ', article_text)

            # Removing special characters and digits
            formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
            formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
            #find list of sentences
            sentence_list = nltk.sent_tokenize(article_text)
            #Find Weighted Frequency of Occurrence
            word_frequencies = {}
            for word in nltk.word_tokenize(formatted_article_text):
                if word not in stopwords:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
            maximum_frequncy = max(word_frequencies.values())
            for word in word_frequencies.keys():
                word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

            #calculate sentence score
            sentence_scores = {}
            for sent in sentence_list:
                for word in nltk.word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                        if len(sent.split(' ')) < 30:
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequencies[word]
                            else:
                                sentence_scores[sent] += word_frequencies[word]

            #to find summary
            summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
            summary = ' '.join(summary_sentences)
            print("summary",summary)

    def summarize2(self,df):
        #using pagerank algo
        #for reference see https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
        #Shorter sentences come thru textrank which does not in case of n-gram based.
        word_embeddings = {}
        f = open('glove.6B.100d.txt', encoding='utf-8')
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            word_embeddings[word] = coefs
        f.close()


        for row in df['conclusion']:
            if row=='0' or row=='':
                continue

            sentences = []
            sentences.append(sent_tokenize(row))
            sentences = [y for x in sentences for y in x]
            # remove punctuations, numbers and special characters
            clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

            # make alphabets lowercase
            clean_sentences = [s.lower() for s in clean_sentences]
            stop_words = stopwords.words('english')

            def remove_stopwords(sen):
                sen_new = " ".join([i for i in sen if i not in stop_words])
                return sen_new

            clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
            sentence_vectors = []
            for i in clean_sentences:
                if len(i) != 0:
                    v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()]) / (len(i.split()) + 0.001)
                else:
                    v = np.zeros((100,))
                sentence_vectors.append(v)
            # similarity matrix
            sim_mat = np.zeros([len(sentences), len(sentences)])
            for i in range(len(sentences)):
                for j in range(len(sentences)):
                    if i != j:
                        sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1, 100), sentence_vectors[j].reshape(1, 100))[0, 0]
            nx_graph = nx.from_numpy_array(sim_mat)
            scores = nx.pagerank(nx_graph)
            ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
            for i in range(10):
                print(ranked_sentences[i][1])
    def summarize3(self,df):
        #http://ai.intelligentonlinetools.com/ml/text-summarization/
        for row in df['conclusion']:
            if row=='0' or row=='':
                continue

            print('Summary:')
            print(summarize(str(row), ratio=0.01))

            print('\nKeywords:')

            # higher ratio => more keywords
            print(keywords(str(row), ratio=0.01))
    def summarize4(self,df):
        #http://ai.intelligentonlinetools.com/ml/text-summarization/
        LANGUAGE = "english"
        SENTENCES_COUNT = 10
        stopwords = nltk.corpus.stopwords.words('english')
        for row in df['conclusion']:
            if row=='0' or row=='':
                continue
            parser = PlaintextParser(row, Tokenizer(LANGUAGE))
            print("--LsaSummarizer--")
            summarizer = LsaSummarizer()
            summarizer = LsaSummarizer(Stemmer(LANGUAGE))
            summarizer.stop_words = get_stop_words(LANGUAGE)
            for sentence in summarizer(parser.document, SENTENCES_COUNT):
                print(sentence)

            print("--LuhnSummarizer--")
            summarizer = LuhnSummarizer()

            summarizer.stop_words = stopwords.words('english')
            for sentence in summarizer(parser.document, SENTENCES_COUNT):
                print(sentence)

            print("--EdmundsonSummarizer--")
            summarizer = EdmundsonSummarizer()
            words = ("deep", "learning", "neural")
            summarizer.bonus_words = words

            words = ("another", "and", "some", "next",)
            summarizer.stigma_words = words

            words = ("another", "and", "some", "next",)
            summarizer.null_words = words
            for sentence in summarizer(parser.document, SENTENCES_COUNT):
                print(sentence)

if __name__=="__main__":
    df=pd.read_csv("dataframe.csv")
    m=ml(df)
    m.summarize()