from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List, Union
from queue import SimpleQueue
from langchain.schema import LLMResult
from threading import Thread
from queue import Queue
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import sys
import re

job_done = object() 
q = SimpleQueue()

class StreamingGradioCallbackHandler(BaseCallbackHandler):
    """Callback handler - works with LLMs that support streaming."""

    def __init__(self, q: SimpleQueue):
        self.q = q

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""
        while not self.q.empty():
            try:
                self.q.get(block=False)
            except SimpleQueue.empty:
                continue
            
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.q.put(token)
        # sys.stdout.write(token)
        # sys.stdout.flush()

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        self.q.put(job_done)

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Run when LLM errors."""
        self.q.put(job_done)

import json
import os
import time

class Logger:
    
    def __init__(self, root_path):
        
        self.root_path = root_path
        self.name = ''
        self.folder_name, self.log_name = self.get_time_text()
        self.folder_name = os.path.join(self.root_path, self.folder_name)
        self.log_name = os.path.join(self.folder_name, self.log_name) + '.json'
        self.records = {}
        
        if os.path.isdir(self.folder_name) == False:
            os.makedirs(self.folder_name)
    
    def record(self, user_message, response, message_class):
        
        record = {}
        record['question'] = user_message
        record['message_class'] = message_class
        record['answer'] = response
        
        _, time_text = self.get_time_text()
        record['time'] = time_text
        
        self.records[time.time()] = record
    
    def save_json(self):
        
        with open(self.log_name, 'w') as rm:
            json.dump(self.records, rm, indent=4)
            
    def get_time_text(self):
        
        time_stamp = time.time() 
        struct_time = time.localtime(time_stamp)
        log_name = time.strftime("%Y-%m-%d %H-%M-%S", struct_time)

        year = struct_time.tm_year
        month = struct_time.tm_mon
        day = struct_time.tm_mday

        folder_name = f'{year}_{month}_{day}'
        
        return folder_name, log_name
    
def evaluation_check(message):
    check_signals = ['evaluation:', 'score:', '\n']
    error = 0
    for signal in check_signals: 
        if signal not in message:
            error+=1
    if error:
        return True
    else:
        return False
    
def get_evaluation_score(message):
    
    evaluation_m, score_m = '', ''
    for m in message.split('\n'):
        if 'evaluation:' in m:
            evaluation_m = m.replace('evaluation:','')
        if 'score:' in m:
            score_m = m.replace('score:','')
            score_m = score_m.replace('分','')
    return evaluation_m, score_m
        
def get_time_text():
    
    time_stamp = time.time() 
    struct_time = time.localtime(time_stamp)
    log_name = time.strftime("%Y-%m-%d %H-%M-%S", struct_time)

    year = struct_time.tm_year
    month = struct_time.tm_mon
    day = struct_time.tm_mday

    folder_name = f'{year}_{month}_{day}'
    
    return folder_name, log_name

def find_item(data, index):
    return next((item for item in data if item['index'] == index), False)

def find_index(answer):

    matched_sequence = re.search(r'序號\d+', answer)

    if matched_sequence:
        extracted_sequence = matched_sequence.group(0) 
        recommend_index = extracted_sequence.replace('序號', '')
    else:
        answer = answer.split('序號')[1]
        all_matched_numbers = re.findall(r'\d+', answer)
        recommend_index = all_matched_numbers[0] if all_matched_numbers else None
    
    return recommend_index



