# Wikipedia data
## Installation
```
pip install -r requirements.txt
```
## Download the Chinese Wikipedia data
selet `zhwiki-20240201-pages-articles-multistream.xml` file
- [zhwiki/latest/](https://dumps.wikimedia.org/zhwiki/latest/)

## Quickstart
### Preprocessing
```
python wiki_preprocessing.py
```


# Save the Chinese Wikipedia data into MongoDB
## Installation
- [MongoDB Community Server](https://www.mongodb.com/try/download/community)
    ```
    Version 4.0.28
    Platform Windows x64
    Package msi
    ```

## Quickstart
### save data into MongoDB
- change the file path assigned to `your_txt_path` in `wiki_db.py`, and than run the command:
    ```
    python wiki_db.py
    ```
### save database
    ```
    $ mongodump -d wikidatabase -o ./dump
    ```
# Wikipedia database for search
- see `wiki_langchain_MongoDB.ipynb` file

# Wikipedia database Q&A llm
- see `wiki_langchain_QA.ipynb` file
