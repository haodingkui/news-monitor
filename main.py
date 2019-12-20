import requests
import jieba
import time


def get_named_entities(title):
    """识别新闻标题中的命名实体"""
    pass

def get_semantic_role_labels(title):
    """识别新闻标题中的语义角色"""
    pass
    
def strip_title(title):
    """去掉新闻标题的来源等杂项信息"""
    if "-" in title:
            index = title.index('-')
            title = title[0:index]
    if "_" in title:
        _index = title.index('_')
        title = title[0:_index]
    title = title.replace(" ","")
    return title

if __name__ == "__main__":
    url = ('https://newsapi.org/v2/top-headlines?'
            'country=cn&'
            'apiKey=786a622dd39f434ab9cbf00dc9a4f68d')
    response = requests.get(url)
    articles = response.json()['articles']、

    for news in articles:
        title = news['title']
        title = strip_title(title)
        print(title)

