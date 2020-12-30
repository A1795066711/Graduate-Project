# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 09:06:42 2020

@author: dell
"""

import pandas as pd 
import jieba

df_news = pd.read_table('val.txt',names=['theme','cause','process','influence' , 'learnFrom' ],encoding='utf-8')
df_news = df_news.dropna() # 去除缺失值行
df_news.head()

content = df_news.content.values.tolist()
print (type(content)) # <class 'list'>

print(content[1000])

content_S = []
for line in content:
    current_segment = jieba.lcut(line)
    if len(current_segment) > 1 and current_segment != '\r\n': #换行符
        content_S.append(current_segment)
content_S[1000]

df_content=pd.DataFrame({'content_S':content_S})
df_content.head()

stopwords=pd.read_csv("stopwords.txt",index_col=False,sep="\t",quoting=3,names=['stopword'], encoding='utf-8')
stopwords.head(5)

def drop_stopwords(contents,stopwords):
    contents_clean = []
    all_words = []
    for line in contents:
        line_clean = []
        for word in line:
            if word in stopwords:
                continue
            line_clean.append(word) # 没过滤掉的加入到列表
            all_words.append(str(word)) # 做词云用的列表
        contents_clean.append(line_clean)
    return contents_clean,all_words
    #print (contents_clean)
        

contents = df_content.content_S.values.tolist()   # 分词后正文转列表 
stopwords = stopwords.stopword.values.tolist()  # 通用词转列表
contents_clean,all_words = drop_stopwords(contents,stopwords)

df_content=pd.DataFrame({'contents_clean':contents_clean})
df_content.head()

df_all_words=pd.DataFrame({'all_words':all_words})
df_all_words.head()