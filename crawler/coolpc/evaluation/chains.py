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

