

JQ_SCHEMA = 'to_entries|map("\(.key): \(.value)")|.[]'

JQ_SCHEMA_2 = '.[] | "清單序號\(.index) 清單：\(.question)"'

EXPERT_PROMPT = "你現在是一位電腦配件的專家，你會針對我的問題產生專業的電腦配件回覆。以下為我的輸入：{question}"

CLASSIFY_PROMPT_FIRST =  "輸入的資訊會對應四種類別， \
                          1 詢問電腦一般知識的問題 \
                          2 查詢電腦零件的價格或者公司名稱，或者比較電腦零件的問題 \
                          3 詢問推薦組合、清單的問題 \
                          4 詢問尚未被定義的類別 \
                          請根據輸入的資訊，辨識出該問題會哪一種問題 \
                          輸入的資訊:{question} \
                          辨識完成後，請輸出該問題序列的數字，表明類別，\
                          輸出：數字 "
                    
REFUSE_MESSAGE = '這個問題超出了小X能回答的範圍，請嘗試詢問其他PC DIY問題～'

SQL_PROMPT = "如果 SQLResult 的後面沒有任何數字或資料，請回覆：查無資料"

CLASSIFY_PROMPT_SECOND = """
你是一個電腦問題的分類器。請你把輸入的問題做出分類
[問題定義]
"1": "詢問電腦與零件知識的問題。",
"2": "查詢特定型號的資訊，而非產品名稱，例如價格、公司名稱",
"4": "一台電腦或者一份清單"
"5": "詢問與電腦、零件無關的問題"
[範例]
1.詢問電腦與零件知識的問題。
    (1).電腦配置中的主板選擇為何重要？ (2).什麼是貓扇? (2).白色的機殼有什麼優點？
2.查詢特定型號的資訊，而非產品名稱，例如價格、公司名稱
    (1).RTX4070價格多少? (2). i7-14700請問是哪家公司的產品？
4.想要一台電腦或者一份清單
    (1).詢問一般娛樂需求的電腦 (2).想要繪圖需求的電腦 (3).30K遊戲機的組套詢問
5.詢問與電腦、零件無關的問題
    (1).現在養樂多一瓶多少錢？ (2).貓比較可愛還是狗比較可愛？
[提示]
1.機殼的問題請分到類別1 2.CPU的規格問題請分到類別1

問題：{question}
回覆：1,2,4,5 其中一個數字
"""

EVALUATION_PROMPT = \
"""
    你現在是一位電腦配件的專家，你現在要對下列的 Answer 作出評估。 
    關於評估，你可以參考 Question，接著查看 Answer。

    [以下為輸入資料]
    Question:{question}
    Answer:{answer}
    
    [格式]
    輸出:[填寫你的評論] 說出你的看法，評論這個 Answer 的優劣。
    
    [範例]
    輸出:關於主機板與CPU的組合問題，這個評論很實用。
"""

RECOMMEND_EVA_PROMPT= \
"""
    你現在是一位電腦配件的專家，你現在要對下列的 Recommend 作出評估。 
    關於評估，你可以參考 Question，接著查看 Recommend

    [以下為輸入資料]
    Question:{question}
    Recommend:{predict}
    
    [格式]
    輸出:[填寫你的評論] 說出你的看法，評論這個 Recommend 的優劣。
    
    [範例]
    輸出:關於提出的 question，這個 recommend 很實用。
"""

SCORER_PROMPT = \
"""
    你現在是一位電腦配件的專家，你現在要對下列的 Evaluation ，做出評分，並且給出一個數字。 
    關於評估，你參考了 Answer, Question，接著查看 Evaluation。
    
    [以下為輸入]
    Question:{question}
    Answer:{answer}
    Evaluation:{evaluation}
    
    看完 Question,Answer, Evaluation，1~10給出一個數字，分數越代表品質越好，分數越低代表品質越差。
    
    [格式]
    score:[1~10]
    [範例]
    score:3
"""

RECOMMEND_PROMPT = '，另外請提供該清單的序號給我，例如：序號3。請限定在30字內'

