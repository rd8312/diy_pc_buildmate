# RAG Documentation

This document outlines the steps to set up and utilize the RAG (Retrieval-Augmented Generation) application, focusing on leveraging the *faiss-cpu* Python library for efficient data retrieval and the process of generating responses using a specific class designed for interaction.
A Jupyter notebook (`RAG_integration_clean.ipynb`) is provided for guiding the RAG.

## Setup

### Install Required Python Library

To ensure the necessary Python packages are installed, especially for handling vector data efficiently, install the `faiss-cpu` library using the following command:

```bash
!pip install faiss-cpu
```

## Data Preparations

### Documents and Embeddings

For the RAG application, a crucial component involves the documents it uses for information retrieval and the subsequent embeddings that represent these documents in a vector space. The embeddings allow for efficient querying to find the most relevant information as input for generating responses. The setup requires the following two assets:

- **Documents File**: `combined_ptt_mobile01_documents_all_ptt_smaller_v2.jsonl`
- The corpus utilized for this project consists of discussion articles from the PC shopping section of PTT, Taiwan's largest BBS and mobile01.

- **Embeddings File**: `embedding_data.pkl` (Download URL: https://drive.google.com/file/d/1taua4QUEXPfZLExjYTuIzBkIMphtKGr-/view?usp=sharing)

These files contain the necessary data for the application, where `combined_ptt_mobile01_documents_all_ptt_smaller_v2.jsonl` includes the text content of documents and `embedding_data.pkl` contains the pre-computed embeddings of these documents.

### Description of the documents

The `combined_ptt_mobile01_documents_all_ptt_smaller_v2.jsonl` file is a curated collection containing discussions about PC hardware component selections. These discussions are extracted from two major sources:

- **PTT's PC Shopping Discussion Section**: PTT, Taiwan's largest Bulletin Board System (BBS), hosts a dedicated section for PC shopping. This section is a vibrant community of enthusiasts and experts who share advice, experiences, and recommendations on various PC components necessary for assembling computers.

- **Mobile01's DIY Computer Assembly Forum**: Mobile01 is another popular platform in Taiwan that features discussions on a wide range of topics, including technology. The DIY Computer Assembly forum within Mobile01 facilitates the exchange of insights, tips, and guidance on selecting the right components for custom PC builds.

### Utilizing Faiss for Efficient Querying

To handle the embeddings, the [Faiss](https://github.com/facebookresearch/faiss) library is used for its efficient searching capabilities in large datasets. The procedure involves:

1. Loading the embeddings from `embedding_data.pkl` into the Faiss index.
2. Using Faiss to execute queries against the index to find the most relevant documents based on textual input.

The embedding model used for generating these embeddings is **text-embedding-3-small**.

## Generating Responses 

### ChatOpenAI Class

To facilitate the generation of responses based on user input and the relevant information retrieved from the documents, the `ChatOpenAI` class is used.

**Class Name**: `ChatOpenAI()`

This class is responsible for taking a query, finding relevant information using the previously mentioned setup with Faiss, and then generating a natural language response that incorporates this information.
**Model Version**: `gpt-3.5-turbo`
    - The `gpt-3.5-turbo` is the specific version of the GPT model used for response generation. It offers a balanced trade-off between performance and computational resource requirements.


## Usage Instructions

To utilize the RAG model for your natural language processing tasks, instantiate the `ChatOpenAI()` class and use it to generate responses based on your specific query inputs. The class will automatically handle the retrieval of relevant documents and leverage the GPT model to generate coherent and contextually relevant responses.


# Fine-Tuning Large Language Models Using the OpenAI Platform
- Document: Approaches to Developing LLM Applications in Specific Domains.pdf (Download url: https://drive.google.com/file/d/1ghMLhmqpLT_xwjv_A0xwm-_15sjOfx1p/view?usp=drive_link)

  
# Fine-tuning MediaTek Research Breeze-7B for PC Hardware Assembly Domain

## Project Overview

This project focuses on enhancing the response capabilities of the base Breeze-7B model in the specific domain of PC hardware assembly. Our goal is to fine-tune the model so that it can provide valuable recommendations when users inquire about purchasing components for assembling a computer. These recommendations should highlight components that are recently available on the market and have favorable reviews.

A unique feature of this project is the use of Taiwanese culture-specific corpora, allowing the fine-tuning process to be conducted on consumer-grade GPUs with the 7B model.

## Model Details

- **Base Model**: Breeze-7B
  - An open-source language model derived from Mistral-7B, Breeze-7B is crafted to enhance language understanding and chatbot capabilities, specifically targeting Traditional Chinese.
  - **base_model_id**: `"MediaTek-Research/Breeze-7B-Instruct-v0_1"`

## Corpus

- **Source**: The corpus utilized for this project consists of discussion articles from the PC shopping section of PTT, Taiwan's largest BBS.
- **Language**: Traditional Chinese, reflective of Taiwan's linguistic nuances.
- **Volume**: A total of 2,500 entries.
- **File Name**: `ptt_train_game_len_remove_rule_4_2500.jsonl`.

## Fine-tuning Approach

The fine-tuning process employs QLoRA, significantly reducing VRAM usage. This advancement allows the project to proceed on consumer-grade GPUs, such as the GeForce RTX 4090 with only 24GB of VRAM.

- **Training Duration**: 3 epochs, approximately 3 hours.

## Environment Setup

A Jupyter notebook (`breez7b_fine-tuning_clean.ipynb`) is provided for guiding the fine-tuning process. To prepare your environment, the following packages need to be installed:

```bash
!pip install -q -U bitsandbytes
!pip install -q -U git+https://github.com/huggingface/transformers.git
!pip install -q -U git+https://github.com/huggingface/peft.git
!pip install -q -U git+https://github.com/huggingface/accelerate.git
!pip install -q -U datasets scipy ipywidgets
!pip install -q trl xformers wandb datasets einops sentencepiece
```

## Objectives

By fine-tuning the MediaTek Research Breeze-7B model with Taiwan's largest BBS discussions on PC shopping, our project aims to achieve:

1. Enhanced model response quality in Traditional Chinese, specifically tailored to the PC hardware assembly domain.
2. Provision of up-to-date and positively reviewed component recommendations, assisting users in making informed decisions for their PC assembly needs.

The use of advanced fine-tuning techniques coupled with culturally rich and domain-specific corpora ensures that the improved Breeze-7B model serves as a valuable asset for users seeking guidance in the complex landscape of PC hardware assembly.


# PTT Crawler
- Download URL： https://raw.githubusercontent.com/HowardNTUST/Marketing-Data-Science-Application/master/%E7%95%B6STP%E3%80%8C%E8%A1%8C%E9%8A%B7%E7%AD%96%E7%95%A5%E3%80%8D%E9%81%87%E5%88%B0%E8%B3%87%E6%96%99%E7%A7%91%E5%AD%B8/STP%E8%B3%87%E6%96%99%E7%A7%91%E5%AD%B8_%E7%B3%BB%E5%88%972-%E3%80%90%E8%B3%87%E6%96%99%E8%92%90%E9%9B%86%E3%80%91%20Python%E7%B6%B2%E8%B7%AF%E7%88%AC%E8%9F%B2%E5%B0%88%E6%A1%88%E5%B0%8E%E5%90%91%E6%95%99%E5%AD%B8/ptt.py
  

