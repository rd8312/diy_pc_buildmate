from gensim.corpora.wikicorpus import extract_pages, filter_wiki
import bz2file
import re
import opencc
from tqdm import tqdm
import codecs
import pandas as pd

# s2twp: 簡體中文 -> 繁體中文 (台灣, 包含慣用詞轉換)
openCC = opencc.OpenCC('s2twp.json')

def wiki_replace(d):
    s = d[1]
    s = re.sub(':*{\|[\s\S]*?\|}', '', s)
    s = re.sub('<gallery>[\s\S]*?</gallery>', '', s)
    s = re.sub('(.){{([^{}\n]*?\|[^{}\n]*?)}}', '\\1[[\\2]]', s)
    s = filter_wiki(s)
    s = re.sub('\* *\n|\'{2,}', '', s)
    s = re.sub('\n+', '\n', s)
    s = re.sub('\n[:;]|\n +', '\n', s)
    s = re.sub('\n==', '\n\n==', s)
    s = u'【' + d[0] + u'】\n' + s
    return openCC.convert(s) 

def wiki_process(input_file, save_path):
    # wikicorpus解析
    wiki = extract_pages(bz2file.open(input_file))
    # 處理並輸出
    i = 0
    f = codecs.open(save_path, 'w', encoding='utf-8')
    w = tqdm(wiki, desc=u'已取得0篇文章')
    for d in w:
        if not re.findall('^[a-zA-Z]+:', d[0]) and d[0] and not re.findall(u'^#', d[1]):
            s = wiki_replace(d)
            f.write(s+'\n\n\n')
            i += 1
            if i % 100 == 0:
                w.set_description(u'已取得%s篇文章'%i)
    
    f.close()

if __name__ == '__main__':
    input_file = ".\zhwiki-20240201-pages-articles-multistream.xml.bz2"  # bz2文件存放位置
    save_path = 'zhwiki.txt'   # txt文件保存位置
    wiki_process(input_file,save_path)
