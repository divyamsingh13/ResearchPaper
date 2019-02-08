
keywords=["heart"]
if os.path.exists("dataframe.pkl"):
    dt = pd.read_pickle("dataframe.pkl")
else:
    dt=pd.DataFrame()

for i in keywords:
    d=download_pdf(i)
    d1=d.search_by_keyword()
    df=d.download(d1)
    dt=dt.append(df)
print(dt.shape)
dt.to_pickle("dataframe.pkl")