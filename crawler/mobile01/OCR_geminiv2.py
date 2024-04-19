import streamlit as st
import json
import requests
import PIL.Image
from io import BytesIO
import os
from dotenv import load_dotenv
import google.generativeai as genai
import tempfile
from google.protobuf import wrappers_pb2
from pathlib import Path

# 加載環境變量並配置Google API
config_path = ''

with open(config_path, 'r') as f:
    config = json.load(f)
your_openai_key = config['GOOGLE_API_KEY']
genai.configure(api_key=your_openai_key)

model = genai.GenerativeModel('gemini-pro-vision')
# Streamlit 用戶界面
st.title('JSON檔案圖片OCR處理工具')

uploaded_file = st.file_uploader("選擇一個JSON檔案進行上傳", type='json')
text_input = """你是一個熟悉電腦零組件的品牌與型號的專家，如：CPU, 記憶體, 顯示卡, 儲存裝置, 電源供應器, 散熱器, 機殼等。你了解自組電腦的零件清單通常包含哪些零件。
The user you are helping speaks Traditional Chinese and comes from Taiwan.
請將以下來自台灣的自組電腦零組件清單裡的品牌與型號等文字辨識出來，若是辨識品牌與型號遇到困難或看不清楚的，以及辦識的品牌與型號結果不含英文與數字的型號的，請給低的 confidence probability。
OCR 辨識結果只要留品名（品牌與型號), quantity, subtotal. 
Your response MUST be in JSON format with follow this structure:
'''
[
    {
       "name": "brand name and model name",
       "quantity": X,
       "subtotal": X,
    "confidence_probability": X
      },
    {
       "name": "brand name and model name",
       "quantity": X,
       "subtotal": X,
    "confidence_probability": X
      }
] 
'''
Hard requirements that must be followed:
 - IMPORTANT: The response must be in JSON format.
 - IMPORTANT: The total price should not be included in the response.
 - IMPORTANT: The values in the JSON must be in language zh-TW.
 - IMPORTANT: The keys in the JSON must be in language English.
 - IMPORTANT: JSON 裡不要出現 "零件清單" 的 key.
 - IMPORTANT: JSON 裡不要出現 "總計" 的 key.
 - IMPORTANT: JSON 裡不要出現 "items" 的 key.
 - IMPORTANT: JSON 裡不要出現 "total" 的 key.

"""
def process_content(content):
    for i, item in enumerate(content):
        if isinstance(item, str) and item.startswith('img:') and not item.endswith('.gif'):
            url = item[4:]
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url  # 或者 'https://', 依照实际情况而定
            try:
                response = requests.get(url)
                response.encoding = 'utf-8'
                if response.status_code == 200:
                    img = PIL.Image.open(BytesIO(response.content))
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                        img_path = tmpfile.name
                        img.save(img_path)
                    img_end = PIL.Image.open(img_path)

                    try:
                        ocr_response = model.generate_content([text_input, img_end])
                        content[i] = ocr_response.text
                        print(ocr_response.text)
                
                    except Exception as e:
                        print(f"處理 OCR 請求時發生未預期的錯誤：{e}")

                    os.remove(img_path)
                else:
                    print("圖像 URL 請求失敗，狀態碼:", response.status_code)
            except requests.exceptions.RequestException as e:
                print(f"請求圖像 URL 時發生錯誤：{e}")
            except PIL.UnidentifiedImageError as e:
                print(f"解析圖像時發生錯誤：{e}")
            except Exception as e:
                print(f"處理圖像時發生未預期的錯誤：{e}")


def process_content_old(content):
    for i, item in enumerate(content):
        if isinstance(item, str) and item.startswith('img:') and not item.endswith('.gif'):
            url = item[4:]
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url  # 或者 'https://' 依據實際情況而定
            response = requests.get(url)
            if response.status_code == 200:
                img = PIL.Image.open(BytesIO(response.content))
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                    img_path = tmpfile.name
                    img.save(img_path)
                img_end = PIL.Image.open(img_path)
                ocr_response = model.generate_content([text_input, img_end])

                content[i] = ocr_response.text
                print(ocr_response.text)
                
                os.remove(img_path)


if uploaded_file is not None:
    data = json.load(uploaded_file)
    # 獲取上傳檔案的名稱（不包括擴展名）
    uploaded_file_name = Path(uploaded_file.name).stem
    modified_file_name = f"{uploaded_file_name}_ocr.json"  # 加上 _ocr.json
    
    if st.button('處理JSON檔案'):
        with st.spinner('正在處理...'):
            for post in data:
                process_content(post['content'])
                for reply in post.get('replayDetail', []):
                    process_content(reply['content'])
            st.success('處理完成！')
            st.download_button(
                label="下載處理後的JSON文件",
                data=json.dumps(data, ensure_ascii=False, indent=4),
                file_name=modified_file_name,  # 使用修改後的檔案名
                mime='application/json'
            )