import requests
import jieba
import time
import json
from ner_client import BertClient


def get_named_entities(sentence):
    """识别句子中的命名实体"""
    with BertClient(show_server_config=False, check_version=False, check_length=False, mode='NER') as bc:
        start_t = time.perf_counter()
        # sentence = '要深入学习贯彻习近平中国特色社会主义思想'
        rst = bc.encode([list(sentence)], is_tokenized=True)
        tag_list =rst[0]
        result_dict = extract_entities_from_ner_result(sentence, tag_list) 
        print(time.perf_counter() - start_t)
        return result_dict

def extract_entities_from_ner_result(sentence, tag_list):
    """抽取BIO标注结果中的命名实体"""
    result_dict = {}
    for tag_index, tag in enumerate(tag_list):
        entity = ""
        if tag[0] == "B":
            entity += sentence[tag_index]
            end_index = tag_index
            for i in range(tag_index+1, len(tag_list)):
                if tag_list[i][0] == "O" or tag_list[i][0] == "B":
                    break
                entity += sentence[i]
                end_index = i
            tag = tag[2:5]
            if tag not in result_dict.keys():
                result_dict[tag] = []
            result_dict[tag].append(sentence[tag_index:end_index+1])
    return result_dict

def get_semantic_role_labels(sentence):
    """识别句子中的语义角色"""
    url = "http://127.0.0.1:8068/srl/api"
    seg_list = jieba.cut(sentence, cut_all=False)
    sentence = "/".join(seg_list)  # 精确模式
    # text = "提醒/我/三点/去/东门/拿/快递/。"
    param = {'sentence':sentence}
    response = requests.post(url, data=param)
    result_list = json.loads(response.text)
    return result_list
    
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
    articles = response.json()['articles']

    for news in articles:
        title = news['title']
        title = strip_title(title)
        print(title)
        print(get_semantic_role_labels(title))
        print(get_named_entities(title))
