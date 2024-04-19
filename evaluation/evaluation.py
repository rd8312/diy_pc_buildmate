# %% [markdown]
# ## 套件與資料載入

# %%
# Import packages
import sys
sys.path.append('.')
# sys.path.append('.')

from tqdm import tqdm
import re

import ast
from langchain.callbacks import get_openai_callback

import json
import os

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--config_path', dest='config_path')
    parameter_args = parser.parse_args()

    config_path = parameter_args.config_path

    # config_path = '../config/evaluation_config.json'

    with open(config_path, 'r') as f:
        config = json.load(f)
    os.environ['OPENAI_API_KEY'] = config['OpenAI_api_key']

    test_dataset_path = config['test_dataset_path']
    with open(test_dataset_path, 'r') as f:
        test_set = json.load(f)
        
    only_for_classification = test_set['only_for_classification']
    SQL_PROMPT = config['GPTs']['SQL']['prompt']

    # %%
    from chains import make_chain, make_memory, Chain_manager

    chain_manager = Chain_manager(config)
    classifier_chain, _ = chain_manager.make_chain('Classifier')
    general_chain, _ = chain_manager.make_chain('General')
    db_chain, _ = chain_manager.make_chain('SQL')
    retrieve_chain, _ = chain_manager.make_chain('Retrieve')
    consultant_chain, memory = chain_manager.make_chain('Consultant') # Netizen Consultant

    comment_chain, _ = chain_manager.make_chain('Comment')
    score_chain, _ = chain_manager.make_chain('Score')
    recommend_eva_chain, _ = chain_manager.make_chain('Recommend_evaluation')
    consultant_comment_chain, _ = chain_manager.make_chain('Consultant_Comment')

    # %% [markdown]
    # ## 預測

    # %%
    import time
    time1 = time.time()


    classifier_error_examples = []

    with get_openai_callback() as cb:
        
        for data in tqdm(test_set['data_list'], desc='模型預測'):
            
            question_class = data['class']
            question = data['question']
            
            if question_class != '6':
                predict_class = classifier_chain.invoke({"question": f"{question}"})
                predict_class = re.findall('\d', predict_class)[0]
            elif question_class == '6':
                predict_class = '6'
            
            data['predict_class'] = predict_class
            
            if predict_class == '6':
                try:
                    question_childs = data['question_childs']
                    memory.clear()
                    conversation = ''
                    for question in question_childs:
                        input_message = {"question": f"{question}"}
                        answer = consultant_chain.invoke(input_message)  
                        memory.save_context(input_message, {"answer": answer})
                        
                        data['answer_childs'].append(answer)
                        conversation += f'諮詢的問題：{question}\n諮詢的回覆：{answer}\n'
                    data['predict'] = conversation
                except Exception as e:
                    print(f'預測程式錯誤\nChain {predict_class}\n錯誤原因：{e}')
            
            elif only_for_classification:
                pass
            
            elif question_class == predict_class:
                
                try:
                    
                    if predict_class == '1':
                        
                        predict = general_chain.invoke({"question": f"{question}"})                
                    
                    if predict_class == '2':
                        question = question + SQL_PROMPT
                        return_data = db_chain.invoke(question)
                        if return_data['result']:
                            predict = ast.literal_eval(return_data['result'])[0][0]
                        else:
                            predict = ''
                        
                    if predict_class == '4':
                        
                        predict = retrieve_chain.invoke(question)
                        predict = '這邊有找到一則與您需求相近的清單給您：\n' + predict
                        
                    data['predict'] = predict
                
                except Exception as e:
                    print(f'預測程式錯誤\nChain {predict_class}\n錯誤原因：{e}')
            else:
                classifier_error_examples.append(question)
                print(f'[分類錯誤]問題：{question}\n真實類別：{question_class}\n預測類別：{predict_class}')

    time2 = time.time()
    process_time = time2 - time1

    # %% [markdown]
    # ## 評估

    # %%
    classifier_error_examples = []

    for data in tqdm(test_set['data_list'], desc='模型評分'):
        
        question_class = data['class']
        predict_class = data['predict_class']
        
        if predict_class == '6':
            question = data['question']
            predict = data['predict']
            try:
                question = '想要一台' + question
                evaluation = consultant_comment_chain.invoke({"question": f"{question}", "predict": f"{predict}"})
                score = score_chain.invoke({"question": f"{question}", "answer": f"{predict}", "evaluation": f"{evaluation}"})
                score = re.findall(r'\d+', score)[0]
                data['evaluation'] = evaluation
                data['score'] = score
            except Exception as e:
                print(f'評估過程發生錯誤\n錯誤原因：{e}')
                
        elif only_for_classification:
            pass
        
        elif question_class == predict_class:
            question = data['question']
            predict = data['predict']
            try:
                
                if predict_class == '1':
                    
                    evaluation = comment_chain.invoke({"question": f"{question}", "answer": f"{predict}"})
                    evaluation = evaluation.replace('輸出:', '').replace(' ', '')
                    
                    score = score_chain.invoke({"question": f"{question}", "answer": f"{predict}", "evaluation": f"{evaluation}"})
                    score = re.findall(r'\d+', score)[0]
                        
                if predict_class == '2':
                    
                    answer = data['answer']
                    answer_type = data['answer_type']

                    # 更複雜的計分規則，可以來討論，例如型號與名稱，可以接受模糊比對
                    
                    if answer_type == 'error':
                        if answer == '':
                            score = 10
                        else:
                            score = 0
                    elif predict == '':
                        score = 0
                    elif answer_type == 'int':
                        if int(answer) == int(predict):
                            score = 10
                        else:
                            score = 0
                    elif answer_type == 'str':
                        if answer in predict or answer in predict:
                            score = 10
                        else:
                            score = 0
                    
                    evaluation = ''
                    
                    if score == 0:
                        print(f'\n[SQL Error]\nType: {answer_type}\nQuestion: {question}\nAnswer: {answer}\nPredict: {predict}\n')
                    
                if predict_class == '4':
                    
                    evaluation = recommend_eva_chain.invoke({"question": f"{question}", "predict": f"{predict}"})
                    score = score_chain.invoke({"question": f"{question}", "answer": f"{predict}", "evaluation": f"{evaluation}"})
                    score = re.findall(r'\d+', score)[0]
                    
            except Exception as e:
                print(f'評估過程發生錯誤\n錯誤原因：{e}')
            data['evaluation'] = evaluation
            data['score'] = score
            
        else:
            error_example = {}
            data['score'] = 0
            classifier_error_examples.append(data)
            
    if classifier_error_examples and only_for_classification: print(classifier_error_examples)

    # %% [markdown]
    # ## 分數計算

    # %%
    classifier_predict = 0
    consultant_num = 0

    class_1_scores = []
    class_2_scores = []
    class_4_scores = []
    class_6_scores = []
    
    total_response_count = 0
    data_1_5_num = 0

    for data in test_set['data_list']:
        
        data_class = data['class'] 
        predict_class = data['predict_class'] 
        
        
        if predict_class == data_class:
            
            if predict_class == '6':
                data_score = data['score'] 
                class_6_scores.append(data_score)
                consultant_num += 1
                for answer in data['answer_childs']:
                    total_response_count += len(answer)
                    data_1_5_num += 1
                
            elif only_for_classification:
                classifier_predict += 1
            else:
                classifier_predict += 1
                data_score = data['score'] 
                
                if data_class == '1':
                    class_1_scores.append(data_score)
                    total_response_count += len(data['predict'])
                    data_1_5_num += 1
                elif data_class == '2':
                    class_2_scores.append(data_score)
                elif data_class == '4':
                    class_4_scores.append(data_score)

    if classifier_predict:
        classifier_accuracy = int(classifier_predict / (len(test_set['data_list']) - consultant_num) *100) 
        classifier_average = float(classifier_predict / (len(test_set['data_list']) - consultant_num) * 10) 
    else:
        classifier_accuracy, classifier_average = 0, 0
        
    if classifier_average:
        test_set['Classifier Accuracy'] = classifier_accuracy
        test_set['score_data']['Classifier'] = classifier_average
        print(f'Classifier Score: {classifier_average}')

    if class_1_scores:
        class_1_average = sum([int(num) for num in class_1_scores]) / len(class_1_scores)
        test_set['score_data']['General'] = class_1_average
        print(f'General Score: {class_1_average} ')
        
    if class_2_scores:
        class_2_average = sum([int(num) for num in class_2_scores]) / len(class_2_scores)
        test_set['score_data']['SQL'] = class_2_average
        print(f'SQL Score: {class_2_average} ')
        
    if class_4_scores:
        class_4_average = sum([int(num) for num in class_4_scores]) / len(class_4_scores)
        test_set['score_data']['Retrieve'] = class_4_average
        print(f'Retrieve Score: {class_4_average} ')
        
    if class_6_scores:
        class_6_average = sum([int(num) for num in class_6_scores]) / len(class_6_scores)
        test_set['score_data']['Consultant'] = class_6_average
        print(f'Consultant Score: {class_6_average} ')

    
    test_set['Response count'] = total_response_count
    test_set['token'] = cb.total_tokens
    test_set['cost'] = cb.total_cost
    test_set['Inference time'] = process_time
    test_set['Data 1 and 5 num'] = data_1_5_num
    print('='*25)
    print(f'Response count: {total_response_count}')
    print(f'Data 1 and 5 num: {data_1_5_num}')
    print(f'Cost: {round(cb.total_cost, 15)}')
    print(f'Token: {cb.total_tokens}')
    print(f'Inference time', process_time)
    print('='*25)

    # %% [markdown]
    # ## 紀錄儲存

    # %%
    from units import get_time_text

    _, evaluation_datetime = get_time_text()
    test_set['Evaluation datetime'] = evaluation_datetime
    report_path = config['report_path']
    evaluation_json_path = f'{report_path}/{evaluation_datetime}.json'

    with open(evaluation_json_path, 'w') as rm:
        json.dump(test_set, rm, ensure_ascii=False, indent=4)
        
    print(f'Report path : {evaluation_json_path}')

    # %%



