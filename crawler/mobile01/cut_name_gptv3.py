import streamlit as st
import pandas as pd
import openai
import os
import json

config_path = ''

with open(config_path, 'r') as f:
    config = json.load(f)
your_openai_key = config['OpenAI_api_key']


def process_csv(data, api_key, prompt_template):
    system_prompt = "你是一個了解電腦相關產品型號的專家"
    client = openai.OpenAI(api_key=api_key)
    for index, row in data.iterrows():
        prompt = prompt_template.format(row['name'])
        message = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt},
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message,
            temperature=0
        )
        data.loc[index, 'cut_name'] = response.choices[0].message.content.strip()
        st.write(f"正在處理：{row['name']}")
        st.write(f"切割結果：{response.choices[0].message.content.strip()}")
    return data

st.title('品名切割器')

# 定義多個prompt模板
prompt_templates = {
    "CPU、GPU、主板":
    """請簡化以下產品型號的名稱，只保留產品的主要型號，忽略後面的規格描述和附加信息。
例如，將'華碩 Pro WS W790E-SAGE SE(EEB/8DDR5/2Intel 10G+Realtek 1Gb)14+1+1功率級'簡化為'華碩 Pro WS W790E-SAGE SE'
並將'【狂】華碩 PRIME B760M-K D4-CSM + Intel i7-14700【20核/28緒】至3/31止'簡化為'華碩 PRIME B760M-K D4-CSM + Intel i7-14700
將'華碩 PRIME H610M-K D4-CSM(M-ATX/1A1H/Realtek 1Gb/註冊四年/2DIMM)6+1+1相'簡化為'華碩 PRIME H610M-K D4-CSM'。
將'微星 RTX4070TI GAMING X SLIM 12G(2745MHz/30.7cm/註冊五年/三風扇)'簡化為'微星 RTX4070TI GAMING X SLIM 12G'。
另外如果品牌名稱原本為英文，則不要翻譯，原本為中文，則保留
請按照這個規則簡化下列產品型號
{}
""",
    "散熱": 
    """請簡化以下產品型號的名稱，只保留產品的主要型號，忽略後面的規格描述和附加信息。
例如，將'利民 M.2 2280 TYPE A B SSD 固態硬碟散熱片/鋁合金/單雙面皆適用'簡化為'利民 M.2 2280 TYPE A B SSD 固態硬碟散熱片'
並將'酷碼 NotePal U2 Plus【黑】散熱墊 / 專利風扇可任意變換位置.支援 17吋'簡化為'酷碼 NotePal U2 Plus【黑】散熱墊'
將'快睿 C1 下吹式散熱器/6mm導管*6/14mm風扇/高7.4cm【WXHZ】送LGA1700扣具'簡化為'快睿 C1 下吹式散熱器'。
將'Montech AP3 散熱膏/4公克/附刮刀/導熱係數 5.99W/mK'簡化為'Montech AP3 散熱膏'。
將'Montech Metal DT24 Premium 6導管/高15.8/雙塔雙扇/全黑化/ARGB鋁質上蓋【WXHZ】'簡化為'Montech Metal DT24 Premium'
將'喬思伯 CR3000 黑 散熱器/7導管/高16/雙塔雙扇/ARGB/TDP:260【WXHZ】'簡化為'喬思伯 CR3000 黑 散熱器'
另外如果品牌名稱原本為英文，則不要翻譯，原本為中文，則保留
請按照這個規則簡化下列產品型號
{}
""",
       "硬碟": 
    """請簡化以下產品型號的名稱，只保留產品的主要型號，忽略後面的規格描述和附加信息。
例如，將'UMAX S330 240GB /2.5吋 讀:520MB寫:450MB/3D NAND Flash【三年保】'簡化為'UMAX S330 240GB /2.5吋'
並將'十銓 T-ForceZ540黑武士(石墨烯)1TB/Gen5 PCIe 5.0/讀:11700M/寫:9500M(五年保)'簡化為'十銓 T-ForceZ540黑武士(石墨烯)1TB/Gen5 PCIe 5.0'
將'Seagate FireCuda 540 1TB/Gen5 PCIe 5.0(火梭魚)讀:9500/寫:8500/TLC【五年保】'Seagate FireCuda 540 1TB/Gen5 PCIe 5.0'。
將'三星 Samsung 990 EVO 1TB/PCIe 4.0 x4/5.0 x2/讀:5000/寫:4200/五年保*星睿奇'簡化為'三星 Samsung 990 EVO 1TB/PCIe 4.0 x4/5.0 x2'。
將'Toshiba 2TB【S300系列】【監控碟】128MB/5400轉/三年保(HDWT720UZSVA)'簡化為'Toshiba 2TB【S300系列】【監控碟】'
將'Toshiba 8TB【S300 Pro系列】【監控碟】256MB/7200轉/三年保(HDWT380UZSVA)'簡化為'Toshiba 8TB【S300 Pro系列】【監控碟】'
另外如果品牌名稱原本為英文，則不要翻譯，原本為中文，則保留
請按照這個規則簡化下列產品型號
{}
""",
       "RAM": 
    """請簡化以下產品型號的名稱，只保留產品的主要型號，忽略後面的規格描述和附加信息。
例如，將'UMAX 單條8GB DDR5-5600/CL46【具XMP、EXPO參數】'簡化為'UMAX 單條8GB DDR5-5600/CL46'
並將'威剛 64GB(雙通32GB*2) DDR5 6000 XPG Lancer/CL30 黑【具XMP、EXPO參數】'簡化為'威剛 64GB(雙通32GB*2) DDR5 6000 XPG Lancer/CL30 黑'
將'金士頓 64GB(雙通32GB*2) DDR5-6000/CL36 FURY Beast 白 (獸獵者)【具雙參數】'簡化為'金士頓 64GB(雙通32GB*2) DDR5-6000/CL36 FURY Beast 白'。
將'芝奇 G.SKILL 幻光戟 64GB(雙通32GB*2) D4-3200 CL16 黑銀 F4-3200C16D-64GTZR限量~'簡化為'芝奇 G.SKILL 幻光戟 64GB(雙通32GB*2) D4-3200 CL16 黑銀'。
將'金士頓 NB 4GB DDR3L-1600 低電壓(KVR16LS11/4)(512*8)'簡化為'金士頓 NB 4GB DDR3L-1600 低電壓'
將'美光 Micron Crucial 16GB(雙通8GB*2) DDR4-3200(1024*8)'簡化為'美光 Micron Crucial 16GB(雙通8GB*2) DDR4-3200'
另外如果品牌名稱原本為英文，則不要翻譯，原本為中文，則保留
請按照這個規則簡化下列產品型號
{}
""", 
    "機殼": # 機殼有許多搭售的部分目前沒有使用prompt解決
    """請簡化以下產品型號的名稱，只保留產品的品牌+型號+顏色，如果沒有顏色請不要自己加入，另外請忽略忽略後面的規格描述和附加信息。
例如，將'COUGAR CONQUER(5LMR) 顯卡長35/CPU高19/玻璃透側/ATX 特價原價$8990！'簡化為'COUGAR CONQUER(5LMR)'
並將'樹昌 TI-U202S 2U工業機殼/CPU高5.5/ATX(不含滑軌)/支援ATX電供(限深14cm)'簡化為'樹昌 TI-U202S 2U工業機殼'
將' 視博通 小尖兵 PRO 黑 顯卡長29/CPU高18/雙面透側/前置Type-C/M-ATX'簡化為'視博通 小尖兵 PRO 黑'。
將'旋剛 RGB SLIDER 流影者 黑 顯卡長33.5/CPU高15.7/玻璃透側/RGB面板燈條/ATX'簡化為'旋剛 RGB SLIDER 流影者 黑'。
將'Antec Performance 1 FT 黑/玻璃透側/E-ATX+Antec NE1000G M ATX3.0/金牌/PCIe 5.0'簡化為'Antec Performance 1 FT 黑'
另外如果品牌名稱原本為英文，則不要翻譯，原本為中文，則保留
請按照這個規則簡化下列產品型號
{}
""",
    "螢幕": 
    """請簡化以下產品型號的名稱，只保留產品的品牌+型號另外請忽略忽略後面的規格描述和附加信息。
例如，將'【主機搭購】BenQ GW2475H(1A2H/5ms/IPS/無喇叭)不閃屏.低藍光.護眼螢幕▼下殺到 3/18 23:59'簡化為'BenQ GW2475H'
並將'ACER KA222Q B(1A1H/1ms/VA/無喇叭)低藍光.不閃屏 *尾盤 【活動↓↓↓】'簡化為'ACER KA222Q B'
將'【任搭】PHILIPS 242E2FA(1A1H1P/1ms/IPS/含喇叭/FreeSync)四邊無框.不閃爍 *尾盤'簡化為'PHILIPS 242E2FA'。
另外如果品牌名稱原本為英文，則不要翻譯，原本為中文，則保留
請按照這個規則簡化下列產品型號
{}
""",
    "電源": 
    """請簡化以下產品型號的名稱，只保留產品的品牌、型號、瓦數，另外請忽略忽略後面的規格描述和附加信息。
例如，將'海韻 S12III-500W 銅牌/智慧溫控風扇/5年保'簡化為'海韻 S12III-500W'，
將'Apexgaming GTR-850M(850W) 雙8/金牌/全模/ATX3.0(PCIe 5.0)/全日系/10年 原價$3990'簡化為'Apexgaming GTR-850M(850W)'，
將'華碩 PRIME 750W Gold 雙8/金牌/全模組/ATX3.0(PCIe 5.0)/雙滾珠風扇/8年保'簡化為'華碩 PRIME 750W Gold'，
將'海盜船 RM850x SHIFT(850W) 雙8/金牌/側面接頭/全模組/ATX3.0(PCIe 5.0)/10年'簡化為'海盜船 RM850x SHIFT(850W)'。
另外如果品牌名稱原本為英文，則不要翻譯，原本為中文，則保留
請按照這個規則簡化下列產品型號
{}
""",
}

# 讓用戶選擇一個prompt模板
selected_template = st.selectbox('選擇一個提示模板', list(prompt_templates.keys()))

# 上傳CSV檔案
uploaded_file = st.file_uploader("選擇一個CSV檔案", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    file_name, file_extension = os.path.splitext(uploaded_file.name)

# 處理檔案的按鈕
if st.button('處理檔案'):
    if uploaded_file is not None and your_openai_key:
        processed_data = process_csv(data, your_openai_key, prompt_templates[selected_template])
        download_file_name = f"{file_name}_cut_name{file_extension}"
        st.write(processed_data)
        st.download_button(label="下載更新後的CSV檔案",
                           data=processed_data.to_csv(index=False).encode('utf-8'),
                           file_name=download_file_name,
                           mime='text/csv')
    else:
        st.error("請確保所有欄位都已填寫並上傳了一個CSV檔案。")
