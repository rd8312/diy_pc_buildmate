import json
from pymongo import MongoClient

# 連接到 MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['wikidatabase']
collection = db['collection']

import pandas as pd
from tqdm import tqdm

# txt_path: 文本文件的路徑
txt_path = 'zhwiki.txt'

def wiki_clean_and_format(txt_path):
    # 初始化结果列表
    res = []
    error_num = 0
    doc_id = 1
    count = 0

    # 打開檔案
    with open(txt_path, 'r', encoding='utf-8') as file:
        articles = ''
        title = None
        for line in tqdm(file):
            try:
                # 檢查是否為標題行
                if '【' in line and '】' in line:
                    # 如果之前已經處理過文章，保存它
                    if title:
                        res.append({'id': doc_id, 'title': title, 'articles': articles})
                        # 批次儲存
                        if len(res) == 100:
                            collection.insert_many(res)
                            res = []
                        doc_id += 1
                        articles = ''  # 重置文章内容
                    # 提取標題
                    title = line[line.index('【')+1:line.index('】')]
                elif '*' in line or '==' in line:  # 標題或子標題忽略
                    continue
                else:
                    articles += line.strip()
            except Exception as e:
                error_num += 1
                continue

        # 保存最後一篇文章
        if title:
            res.append({'id': doc_id, 'title': title, 'articles': articles})
            count += 1

        if count % 10 == 0:
            collection.insert_many()

    print(f"Processed with {error_num} errors.")
    # return res

if __name__ == '__main__':
    # 使用函數並儲存到MongoDB
    wiki_clean_and_format(txt_path)
