import pandas as pd
import numpy as np
import re
df=pd.read_csv(r'F:\dataset\ip102_v1.1\classes.txt',header=None,names=['res'])
df['res']=df['res'].apply(lambda x:" ".join(x.split()))
def re_num(df):
    df['id']=df['res'].apply(lambda x:re.findall('\d+',x))
    df['id']=df['id'].apply(lambda x:"".join(x))
    df['name']=df['res'].apply(lambda x:re.findall('\D+',x))
    df['name'] = df['name'].apply(lambda x: "".join(x))
    df.drop('res',axis=1,inplace=True)


re_num(df)
df.to_csv(r'F:\dataset\classes.csv',index=None)
print(df.head(3))