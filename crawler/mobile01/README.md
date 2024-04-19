--python--

##準備
-先確保套件都正確安裝，可以在console中輸入以下
pip install -r requirements.txt

##檔案說明
1. cut_name_gptv3.py
-使用gpt-3.5做品名切割，將原價屋上面紛亂的品名進行LLM切割至乾淨的型號：
ex.【狂】華碩 PRIME B760M-K D4-CSM + Intel i3-14100【4核/8緒】至3/31止->華碩 PRIME B760M-K D4-CSM + Intel i3-14100
-需要：gpt3.5 api 設定於config檔案內：'OpenAI_api_key' = ''
-輸入：json
-輸出：json
-使用需圖形化介面的電腦使用streamlit
使用：於console輸入：  streamlit run cut_name_gptv2.py

2. OCR_geminiv2.py 
-讀取mobile01爬取下來的json檔案，回應中的img連結進行OCR辨識同時已格式化方式重新填入json檔案中
-需要：gemini api 設定於config檔案內：'GOOGLE_API_KEY' = ''
-還未申請請於以下網址申請：https://ai.google.dev/
-輸入：json
-輸出：json
-使用需圖形化介面的電腦使用streamlit
使用：於console輸入：  streamlit run OCR_gemini.py
