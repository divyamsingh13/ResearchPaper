import pandas as pd
import numpy
import six.moves.cPickle as pickle
import textract
import os


class create_dataframe(object):

    def __init__(self,keyword,pdf_path,title):
        self.keyword=keyword
        self.pdf_path=pdf_path
        self.title=title
    def dataframe(self):
        text=textract.process(self.pdf_path)
        text = str(text)

        if os.path.exists("dataframe.pkl"):
            dt = pd.read_pickle("dataframe.pkl")
        else:
            dt=pd.DataFrame()

        dt['keyword']=self.keyword
        dt['keywords']=text[text.find("Keywords:")+len("Keywords:"):text.find("Introduction")].split(',')
        dt['title']=self.title
        dt.to_pickle("dataframe.pkl")
        print("creating")




