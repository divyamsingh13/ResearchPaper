import pandas as pd
import re
import heapq
import nltk

class ml(object):
    def __init__(self,df):
        self.df=df

    def summarize1(self):
        #refer https://stackabuse.com/text-summarization-with-nltk-in-python/
        df=self.df
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



if __name__=="__main__":
    df=pd.read_csv("dataframe.csv")
    m=ml(df)
    m.summarize()