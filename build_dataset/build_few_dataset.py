if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--test_dataset_path', dest='test_dataset_path')
    parameter_args = parser.parse_args()

    test_dataset_path = parameter_args.test_dataset_path
    
    import sys
    from pathlib import Path
    sys.path.append('.')

    import os
    import json
    from chains import Chain_manager

    import re
    
    config_path = 'config/few_config.json'
    with open(config_path, 'r') as f: config = json.load(f)
    os.environ['OPENAI_API_KEY'] = config['OpenAI_api_key']

    chain_manager = Chain_manager(config)
    question_splitter, _ = chain_manager.make_chain('Question_Splitter')
    
    qa_index = 1
    only_for_classification = False

    def get_time_text():
        
        import time
        time_stamp = time.time() 
        struct_time = time.localtime(time_stamp)
        log_name = time.strftime("%Y-%m-%d %H-%M-%S", struct_time)

        year = struct_time.tm_year
        month = struct_time.tm_mon
        day = struct_time.tm_mday

        folder_name = f'{year}_{month}_{day}'
        
        return folder_name, log_name

    def make_dataset(only_for_classification):
        
        _, build_dataset_time = get_time_text()
        time_number = build_dataset_time.replace('-','').replace(' ','')

        dataset = {}
        dataset['name'] = 'test_dataset'
        dataset['build_dataset_time'] = build_dataset_time
        dataset['build_dataset_time_number'] = time_number
        dataset['only_for_classification'] = only_for_classification
        dataset['data_list'] = []
        dataset['token'] = 0
        
        score_data = {}
        score_data['Classifier'] = 0
        score_data['General'] = 0
        score_data['SQL'] = 0
        score_data['Retrieve'] = 0
        
        dataset['score_data'] = score_data
        dataset['Classifier Accuracy'] = 0
        
        return dataset
        
    test_set = make_dataset(only_for_classification)

    # General
    data = {}
    data['qa_index'] = str(qa_index)
    qa_index += 1
    data['class'] = '1'
    data['question'] = '網友詢問有哪些機殼類型特別注重散熱？'
    data['only_for_classification'] = only_for_classification
    
    test_set['data_list'].append(data)

    # SQL
    data = {}
    data['qa_index'] = str(qa_index)
    qa_index += 1
    data['class'] = '2'
    data['question'] = 'B760M-K-CSM多少錢呀？'
    data['answer'] = '10590'
    data['answer_type'] = 'int'
    data['only_for_classification'] = only_for_classification
    test_set['data_list'].append(data)

    # 推薦
    data = {}
    data['qa_index'] = str(qa_index)
    qa_index += 1
    data['class'] = '4'
    data['question'] = '請提供一組清單，是40K左右 遊戲機'
    data['only_for_classification'] = only_for_classification
    test_set['data_list'].append(data)


    # 顧問諮詢    
    question = '30000文書機的電腦'
    inputs =  {"question": question}
    answer = question_splitter.invoke(inputs)
    question_childs = re.findall(r'\d+\.\s*(.*)', answer)
    
    data = {}
    data['qa_index'] = str(qa_index)
    qa_index += 1
    data['class'] = '6'
    data['question'] = question
    data['question_childs'] = question_childs
    data['answer_childs'] = []
    data['only_for_classification'] = only_for_classification
    
    test_set['data_list'].append(data)

    with open(test_dataset_path, 'w') as file:
        json.dump(test_set, file, ensure_ascii=False, indent=4)

    print(f'Build dataset successfully!\nDataset path: {config_path}')


