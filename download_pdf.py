import requests
import bs4
import os
import sys
import pandas as pd
from create_dataframe import create_dataframe
'''retrival of paper id and title'''
class download_pdf(object):
    def __init__(self,keyword,count=100):
        self.keyword=keyword
        self.count=count
    def search_by_keyword(self,search='Search',d={},count1=0):
        keyword1=self.keyword
        data={"keyword":keyword1,"submit":search}
        try:
            response=requests.post(url="https://www.ijsr.net/search_index_results.php",data=data)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        soup=bs4.BeautifulSoup(response.text)
        soup=soup.find("div",{"id":"middle"})
        soup=soup.find_all("table")
        soup=soup[1:51]
        for table in soup:
            row=table.find("tr")
            col=row.find_all("td")
            title=col[0].a.font.text
            version=col[0].a['href']
            country=col[1].em.font.text
            paper_id=col[2].find("input",attrs={"name":"paper_id"})['value']
            if(paper_id[0].isdigit()):
                continue
            else:
                count1+=1
            d[paper_id]=[title,country,version]
        if(count1<self.count):
            return self.search_by_keyword(search="Search Again",count1=count1,d=d)
        else:
            print(count1)
            print(keyword1)
            return d
    def download(self,dict):
        keyword=self.keyword
        print("hfcgf",len(dict.keys()))
        for i in dict.keys():

            version=dict[i][2]
            v=version.rfind("/")
            v=version[:v+1]+i+".pdf"
            try:
                response=requests.get(url=v)
                response.raise_for_status()
            except requests.exceptions.Timeout:
                print("timeout")
                break
            except requests.exceptions.HTTPError as err:
                print("url not found continuing",v)
                continue
            pdf_name = dict[i][0]+".pdf"
            pdf_path = os.path.join("pdfs",keyword,pdf_name)
            if not os.path.exists(pdf_path):
                if not os.path.exists(os.path.dirname(pdf_path)):
                    os.makedirs(os.path.dirname(pdf_path))
                pdf_file = open(pdf_path, "wb")
                pdf_file.write(response.content)
                pdf_file.close()
                print("pdf created")
                print(v)
                print(response.content)
                d=create_dataframe(keyword=keyword,pdf_path=pdf_path,title=dict[i][0],url=v)
                d.dataframe()

    def display_dataframe(self):
        if os.path.exists("dataframe.pkl"):
            dt = pd.read_pickle("dataframe.pkl")
            print(dt)
        else:
            print("dataframe does not exist")
    def search_by_all(self,arr):
        if os.path.exists("dataframe.pkl"):
            dt = pd.read_pickle("dataframe.pkl")

        else:
            print("dataframe does not exist")
            return 0
        for index,row in dt.iterrows():
            if(set(arr)<=set(row['keywords'].split(','))):
                print(row['title'])

keywords=["heart"]
for i in keywords:
    d=download_pdf(i)
    d1=d.search_by_keyword()
    d.download(d1)
    d.display_dataframe()

