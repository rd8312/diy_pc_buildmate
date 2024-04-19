from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl
import json
import time
import os
import re

from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

from langchain.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import JSONLoader
from langchain.chains import ConversationalRetrievalChain
from threading import Thread
from units import StreamingGradioCallbackHandler, job_done, q ,Logger

from chains import make_chain, make_memory, Chain_manager
from units import find_item, find_index
from langchain.memory import ConversationBufferMemory

config_path = 'config/app_config.json'
with open(config_path, 'r') as f:
    config = json.load(f)

os.environ['OPENAI_API_KEY'] = config['OpenAI_api_key']
log_path = config['log_path']
logger = Logger(log_path)

SQL_PROMPT = config['GPTs']['SQL']['prompt']
REFUSE_MESSAGE = config['GPTs']['Refuse']['message']

@cl.on_chat_start
async def on_chat_start():
        
    chain_manager = Chain_manager(config)  
    
    classifier_chain, _ = chain_manager.make_chain('Classifier')
    cl.user_session.set("classifier_chain", classifier_chain)
    
    general_chain, _ = chain_manager.make_chain('General')
    cl.user_session.set("expert_chain", general_chain)
    
    db_chain, _ = chain_manager.make_chain('SQL')
    cl.user_session.set("db_chain", db_chain)
    
    # retrieve_chain, _ = chain_manager.make_chain('Retrieve')
    retrieve_chain, _ = chain_manager.make_chain('Retrieve')
    cl.user_session.set("retrieve_chain", retrieve_chain)
    
    consultant_chain, memory = chain_manager.make_chain('Consultant')
    cl.user_session.set("consultant_chain", consultant_chain)
    
    cl.user_session.set("memory", memory)
    cl.user_session.set("logger", logger)
    consultant_mode = False
    cl.user_session.set("consultant_mode", consultant_mode)
    

@cl.on_message
async def on_message(message: cl.Message):
    
    classifier_chain = cl.user_session.get("classifier_chain")
    expert_chain = cl.user_session.get("expert_chain")
    db_chain = cl.user_session.get("db_chain")
    retrieve_chain = cl.user_session.get("retrieve_chain")
    consultant_chain = cl.user_session.get("consultant_chain")
    
    logger = cl.user_session.get("logger")
    memory = cl.user_session.get("memory")
    consultant_mode = cl.user_session.get("consultant_mode")
    
    msg = cl.Message(content="")
    
    system_switch = False
    if message.content == '1' or message.content == '啟動顧問諮詢':
        consultant_mode = True
        system_switch = True
    elif message.content == '0' or message.content == '關閉顧問諮詢':
        consultant_mode = False
        system_switch = True
        
    input_message = {"question": message.content}
    answer = ''
    
    if system_switch == False:
        if consultant_mode == False:
            question_class = classifier_chain.invoke(input_message)
            question_class = re.findall('\d', question_class)[0]
        elif consultant_mode == True:
            question_class = '6'
    elif system_switch == True:
        question_class = '7'

    if question_class == '1':
        async for chunk in expert_chain.astream(
            input_message,
            config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
        ):
            await msg.stream_token(chunk)
            answer += chunk
    
    elif question_class == '2':
        
        result = db_chain.invoke(message.content+SQL_PROMPT)
        msg.content = result['result']
        msg.update()
        answer = result['result']
    
    elif question_class == '4':
        
        # predict = retrieve_chain.invoke(message.content)
        # predict = '這邊有找到一則與您需求相近的清單給您：\n' + predict
        
        # msg.content = predict
        # msg.update()
        # answer = predict
        docs_searched = retrieve_chain.get_docs_searched(message.content)
        input_message = {"background_context":docs_searched ,"user_question":message.content}
            
        async for chunk in retrieve_chain.chain.astream(
            input_message,
            config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
        ):
            await msg.stream_token(chunk)
            answer += chunk
            
    elif question_class == '5':
        msg.content = REFUSE_MESSAGE
        msg.update()
        answer = REFUSE_MESSAGE
        
    elif question_class == '6':

        async for chunk in consultant_chain.astream(
            input_message,
            config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
        ):
            await msg.stream_token(chunk)
            answer += chunk
        memory.save_context(input_message, {"answer": answer})
        
    elif question_class == '7':
        if consultant_mode == True:
            system_message = '現在為您開啟顧問諮詢'
        elif consultant_mode == False:
            system_message = '現在為您開啟一般模式'
        msg.content = system_message
        msg.update()
        answer = system_message
        
    else:
        raise f"未知錯誤訊息：{question_class}"


    cl.user_session.set("consultant_mode", consultant_mode)
    await msg.send()
    logger.record(message.content, answer, question_class)
    print('=' * 20)
    print(f'專家諮詢: {consultant_mode}')
    print(f'User_message: {message.content}')
    print(f'Class: {question_class}')
    print(f'Answer: {answer}')
    print(f'Timestamp: {time.time()}')
    print('=' * 20)

@cl.on_chat_end
async def on_chat_end():
    logger = cl.user_session.get("logger")
    logger.save_json()
    
    memory = cl.user_session.get("memory")
    
    for m in memory.chat_memory.messages:
        print(m.content)