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
        print(text)
        if os.path.exists("dataframe.pkl"):
            dt = pd.read_pickle("dataframe.pkl")
        else:
            dt=pd.DataFrame()
        print("writing to dataframe")
        dt['keyword']=self.keyword
        print(text.find("Keywords:"))
        if(text.find("Keywords:")==-1):
            print("no keywords")
            dt['keywords']=0
            return 0
        else:
            dt['keywords'] = text[text.find("Keywords:") + len("Keywords:"):text.find("Introduction")].split(',')

        print(self.title)
        dt['title']=self.title

        if(text.find("Conclusion")==-1 or text.find("References")==-1):
            print("no conclusion")
            dt['conclusion']=0
            return 0
        else:
            dt['conclusion']=text[text.find("Conclusion")+len("Conclusion"):text.find("References")]
        dt.to_pickle("dataframe.pkl")






