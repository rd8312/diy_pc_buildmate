from datetime import datetime
import configUtil
import json
import codecs
import os


def getFileName(args, config):
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    topicName = configUtil.getTopicName(args, config)
    return topicName + "_" + dt_string

def saveJson(topics, fileName):
    # 目標目錄路徑
    output_dir = "./output"
    
    # 檢查目標目錄是否存在；如果不存在，則創建它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 構建完整的檔案路徑
    file_path = os.path.join(output_dir, fileName + ".json")
    
    # 使用codecs.open來處理檔案寫入，確保編碼為utf-8
    with codecs.open(file_path, mode="w", encoding="utf-8") as f:
        # 使用json.dump來將topics對象轉換為json格式並寫入檔案
        # 保持縮進為4，確保非ASCII字符不進行轉義，並提供一個lambda函數來處理無法直接序列化的對象
        json.dump(topics, f, indent=4, ensure_ascii=False, default=lambda x: x.__dict__)
