from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable

from units import StreamingGradioCallbackHandler, job_done, q ,Logger

from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

from langchain.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import JSONLoader
from langchain.chains import ConversationalRetrievalChain

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from operator import itemgetter

import json
import os
        
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable

from units import StreamingGradioCallbackHandler, job_done, q ,Logger

from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

from langchain.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import JSONLoader
from langchain.chains import ConversationalRetrievalChain

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from operator import itemgetter

import json
import os

from langchain.memory import ConversationBufferMemory
from operator import itemgetter
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from langchain.document_loaders import JSONLoader
from units import find_item, find_index

import pickle
import faiss
import pickle
import numpy as np
from openai import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import JSONLoader

def make_chain(GPT_config, memory_link=None):

    GPT_name = GPT_config['GPT_name']
    GPT_class = GPT_config['class']
    temperature = GPT_config['temperature']
    model_name = GPT_config['model_name']
    prompt = GPT_config['prompt']
    llm_gpt_3_5 = ChatOpenAI(temperature=temperature, model=model_name, streaming=True)
    
    if GPT_class == 'conversation':
        
        prompt = ChatPromptTemplate.from_template(prompt)

        if memory_link:
            memory_chain = memory_link
            prompt = ChatPromptTemplate.from_messages([MessagesPlaceholder(variable_name="chat_history"), prompt])
            chain = memory_chain | prompt | llm_gpt_3_5 | StrOutputParser()
        else:
            chain = prompt | llm_gpt_3_5 | StrOutputParser()
    
    elif GPT_class == 'query':
        
        db_path = GPT_config['database_path']
        return_direct = GPT_config['return_direct']
        sample_rows = GPT_config['sample_rows']
        verbose = GPT_config['verbose']
        
        db = SQLDatabase.from_uri(f"sqlite:///{db_path}", sample_rows_in_table_info=sample_rows)
        chain = SQLDatabaseChain.from_llm(llm_gpt_3_5, db, verbose=verbose, use_query_checker=True, return_direct=return_direct)

    elif GPT_class == 'rag':
        
        db_path = GPT_config['database_path']
        jq_schema = GPT_config['JQ_SCHEMA']
        
        loader = JSONLoader(file_path=db_path ,jq_schema=jq_schema, text_content=False)
        index = VectorstoreIndexCreator().from_loaders([loader])
        
        if memory_link:
            memory = memory_link
            chain = ConversationalRetrievalChain.from_llm(llm=llm_gpt_3_5,retriever=index.vectorstore.as_retriever(),
                                                    return_source_documents=True, memory=memory)
        else:
            chain = ConversationalRetrievalChain.from_llm(llm=llm_gpt_3_5,retriever=index.vectorstore.as_retriever(),
                                                    return_source_documents=True)

    return chain

def make_memory():
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')
    memory_chain = RunnablePassthrough.assign(
            chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("chat_history"))

    return memory, memory_chain

class Chain_manager():
    
    def __init__(self, config):
        
        self.config = config
        self.gpts = config['GPTs']
        
    def make_chain(self, chain_name):
        
        if self.gpts.get(chain_name):
            return self.build_chain(chain_name)
        else:
            return None, None
        
    def build_chain(self, chain_name):
        
        chain_data = self.gpts[chain_name]
        self.chain_data = self.gpts[chain_name]
        GPT_class =  chain_data['class']
        temperature =  chain_data['temperature']
        model_name =  chain_data['model_name']
        prompt =  chain_data['prompt']
        using_memory =  chain_data.get('using_memory')
        streaming =  chain_data.get('streaming', False)
        if using_memory:
            memory, memory_chain = self.make_memory()
        else:
            memory = None
        
        llm_gpt_3_5 = ChatOpenAI(temperature=temperature, model=model_name, streaming=streaming)
        
        if GPT_class == 'conversation':
            
            reinforce_prompt_path = chain_data.get('reinforce_prompt_path', False)
            if reinforce_prompt_path: prompt = self.reinforce_prompt(prompt)
            
            prompt = ChatPromptTemplate.from_template(prompt)

            if using_memory:
                prompt = ChatPromptTemplate.from_messages([MessagesPlaceholder(variable_name="chat_history"), prompt])
                chain = memory_chain | prompt | llm_gpt_3_5 | StrOutputParser()
            else:
                chain = prompt | llm_gpt_3_5 | StrOutputParser()
        
        elif GPT_class == 'query':
            
            db_path = chain_data['database_path']
            return_direct = chain_data['return_direct']
            sample_rows = chain_data['sample_rows']
            verbose = chain_data['verbose']
            
            db = SQLDatabase.from_uri(f"sqlite:///{db_path}", sample_rows_in_table_info=sample_rows)
            chain = SQLDatabaseChain.from_llm(llm_gpt_3_5, db, verbose=verbose, use_query_checker=True, return_direct=return_direct)

        elif GPT_class == 'rag1':
            
            chain = Retrieve_1(chain_data)
            
        elif GPT_class == 'rag':

            chain = Retrieve_2(chain_data)
            
        return chain, memory
    
    def make_memory(self):
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')
        memory_chain = RunnablePassthrough.assign(
                chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("chat_history"))

        return memory, memory_chain
    def reinforce_prompt(self, prompt):
        
        predefine_prompt = """
        The following are prepared QAs that you should know about computer assembly.
        Q: 組裝電腦最好的工具是什麼？ A: 就是用 BuildMate，它是基於 LLM 發展的組裝電腦助手!
        """
        
        reinforce_prompt_path = self.chain_data['reinforce_prompt_path']
        with open(reinforce_prompt_path, 'r', encoding='utf-8') as file: file_content = file.read()
        
        return predefine_prompt + file_content + prompt
    
    

class Retrieve_1():
    
    def __init__(self, retrieve_config):
        
        self.retrieve_config = retrieve_config
        db_path = retrieve_config['database_path']
        jq_schema = retrieve_config['JQ_SCHEMA']
        
        with open(db_path, 'r') as f:
            self.recommend_data = json.load(f)
        self.RECOMMEND_PROMPT = retrieve_config['prompt']
        llm_gpt_3_5 = ChatOpenAI(temperature=0.0, model='gpt-3.5-turbo', streaming=True)
        
        
        loader = JSONLoader(file_path=db_path ,jq_schema=jq_schema, text_content=False)
        index = VectorstoreIndexCreator().from_loaders([loader])
        
        chain = ConversationalRetrievalChain.from_llm(llm=llm_gpt_3_5,retriever=index.vectorstore.as_retriever(),
                                                return_source_documents=True, memory=None)
        
        self.chain = chain
    
    def invoke(self, message):
        
        message = message + self.RECOMMEND_PROMPT
        result = self.chain.invoke({"question": message, 'chat_history':[]}) 

        recommend = result['answer']
        recommend_index = find_index(recommend)
        if recommend_index == None: raise '找不到序號+數字'
        recommend_item = find_item(self.recommend_data, recommend_index)
        if recommend_item == False:raise 'JSON中沒有該序號的資料'
        
        predict = recommend_item['items']
        
        return predict


class Retrieve_2():
    
    def __init__(self, retrieve_config):
        

        self.retrieve_config = retrieve_config
        embedding_data = retrieve_config['embedding_data']
        json_path = retrieve_config['json_path']
        jq_schema = retrieve_config['JQ_SCHEMA']
        prompt = retrieve_config['prompt']
        self.document_num = retrieve_config['document_num']
        self.embedding_model_name = retrieve_config['embedding_model_name']

        with open(embedding_data, 'rb') as f:
            embeddings = pickle.load(f)
            embeddings = np.array(embeddings, dtype=np.float32)
            
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings)

        loader = JSONLoader(
            file_path = json_path,
            jq_schema = jq_schema,
            json_lines=True, text_content=True)

        documents_load = loader.load()
        self.documents = []
        for d in documents_load:
            self.documents.append(d.page_content)
        
        llm_gpt_3_5 = ChatOpenAI(temperature=0.0, model='gpt-3.5-turbo', streaming=True)
        prompt = ChatPromptTemplate.from_template(prompt)

        self.chain = prompt | llm_gpt_3_5 | StrOutputParser()
    
    def invoke(self, message):
        
        query_embedding = self.embedding_model(message)
        distances, indices = self.index.search(np.array([query_embedding], dtype=np.float32), self.document_num)
        docs_searched = [self.documents[i] for i in indices[0]]

        input_message = {"background_context":docs_searched ,"user_question":message}
        response = self.chain.invoke(input_message)

        return response
    
    def get_docs_searched(self, message):
        
        query_embedding = self.embedding_model(message)
        distances, indices = self.index.search(np.array([query_embedding], dtype=np.float32), self.document_num)
        docs_searched = [self.documents[i] for i in indices[0]]

        return docs_searched

    def embedding_model(self, text):
        
        client = OpenAI()
        response = client.embeddings.create(
            input=text,
            model=self.embedding_model_name
        )

        return response.data[0].embedding  