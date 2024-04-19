# Note
請先完成最基本的單元測試，例如10-20筆的資料，在自己的環境測試沒問題，才來上大量測試。
大量測試的假設是，程式本身邏輯上的問題，它的用途為有效評價語言模型的能力。
所以如果要整合前，請先完成最基本的單元測試，評估測試的部分不適合用來debug，不建議在這此查找問題。

# Evaluation system

You can do three kinds of tasks here.

1. Test a new dataset and run the evaluation
2. Make new methods or algorithm
3. Design a new evaluation formula

## Run the evaluation

You can just open Evaluation.ipynb.

Or on you terminal run python file.
```
$ python evaluation.py --test_dataset_path data/test_dataset.json --config_path config.json
```

## Make new methods or algorithm
You can change the object you want to instead of the method.
For example, if you want try a new general QAs chat, just instead the general_chain 
```
# Old
predict = general_chain.invoke({"question": f"{question}"})
# New
predict = general_chain.invoke({"question": f"{question}"})
```

## Design new evaluation formula

If you have a new idea or more reasonable formula, you want to implement.
Just write your ideas at 評估 and 分數計算 blocks.
```
# Old evaluation

score = 10 if answer == predict else 0

# New evaluation
score = sql_int_eva(predict) # your design

```



