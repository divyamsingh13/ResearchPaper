import pandas as pd
import numpy
import six.moves.cPickle as pickle
import textract
import os


class create_dataframe(object):

    def __init__(self,keyword,pdf_path,title,url):
        self.keyword=keyword
        self.pdf_path=pdf_path
        self.title=title
        self.url=url
    def dataframe(self):
        text=textract.process(self.pdf_path)
        text = str(text)
        print(text)
        if os.path.exists("dataframe.pkl"):
            dt = pd.read_pickle("dataframe.pkl")
        else:
            dt=pd.DataFrame()
        dt1=pd.DataFrame()
        print("writing to dataframe")
        dt1['keyword']=self.keyword
        print(text.find("Keywords:"))
        if(text.find("Keywords:")==-1):
            print("no keywords")
            dt1['keywords']=0
            print(self.url)
            return 0
        else:
            dt1['keywords'] = text[text.find("Keywords:") + len("Keywords:"):text.find("Introduction")]

        print(self.title)
        dt1['title']=self.title

        if(text.find("Conclusion")==-1 or text.find("References")==-1):
            print("no conclusion")
            dt1['conclusion']=0
            return 0
        else:
            dt1['conclusion']=text[text.find("Conclusion")+len("Conclusion"):text.find("References")]
        dt.append(dt1)
        dt.to_pickle("dataframe.pkl")

#updated file




