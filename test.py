import pandas as pd
import spacy
import nltk
from nltk.corpus import wordnet
from itertools import product
from collections import defaultdict

d=defaultdict(list)
df =pd.read_csv("dataframe.csv")
l=list(df.columns.values)
s=df["keywords"]
#print(s)
temp1=list(list())

for i in s:
    try:
        i=i.split("\\n")
        bkwas=(i[0].split())
        temp=[]
        for k in bkwas:
            if(len(str(k))>2):
                temp.append(k)
        if(len(temp)>1):
            temp1.append(temp)
    except:
        continue

df["keywords"]=pd.Series(temp1)


# here all the \n is removed
# now here only the code begins

s=df["keywords"]
it=0
for i in s:   # now here dict is made of url
    try:
        for j in i:
            try:
                d[j].append(df["url"][it])
            except:
                continue
        it += 1
    except:
        it += 1
        continue



all_keywords=[]
for i in s:
    try:
        for k in i:
            if(len(str(k))>2):
                all_keywords.append(k)
    except:
        continue

user_input=["Kidney","layer","food"]
final=set()

for i in user_input:
    for j in all_keywords:
        w1=wordnet.synsets(i)
        w2=wordnet.synsets(j)    #use semantic analysis
        if w1 and w2:
            temp=w1[0].wup_similarity(w2[0])
            try:
                if(temp>float(0.75)):
                    #print(j)
                    final.add(j)
            except:
                continue

#print(final)
if(len(final)<=3):
    print("Sorry Sir ...pls give us some more keywords")
else:
    print("Sir we think You should read following papers for your research work")
    for i in final:
        print(d[i])
























