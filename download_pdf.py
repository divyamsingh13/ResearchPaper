import requests
import bs4
import os
'''retrival of paper id and title '''
def search_by_keyword(keyword1):
    data={"keyword":keyword1,"submit":"Search"}

    response=requests.post(url="https://www.ijsr.net/search_index_results.php",data=data)

    soup=bs4.BeautifulSoup(response.text)
    soup=soup.find("div",{"id":"middle"})
    soup=soup.find_all("table")
    soup=soup[1:51]
    d={}

    for table in soup:
        row=table.find("tr")
        col=row.find_all("td")
        title=col[0].a.font.text
        version=col[0].a['href']
        country=col[1].em.font.text
        paper_id=col[2].find("input",attrs={"name":"paper_id"})['value']
        if(paper_id[0].isdigit()):
            continue
        d[paper_id]=[title,country,version]
    return d

'''retrival of downloaded papers'''
def download(dict,keyword):
    for i in dict.keys():
        print(i)

        version=dict[i][2]
        v=version.rfind("/")
        v=version[:v+1]+i+".pdf"
        response=requests.get(url=v)
        pdf_name = dict[i][0]+".pdf"
        pdf_path = os.path.join("pdfs",keyword,pdf_name)
        if not os.path.exists(pdf_path):

            if not os.path.exists(os.path.dirname(pdf_path)):
                os.makedirs(os.path.dirname(pdf_path))
            pdf_file = open(pdf_path, "wb")
            pdf_file.write(response.content)
            pdf_file.close()

keywords=['heart','artifical intelligence']
for i in keywords:
    d=search_by_keyword(i)
    download(d,i)
