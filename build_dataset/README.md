
## Dataset specification

The first thing is a specification.
There are three types of data.

- General QAs 
    1. class = 1
    2. question = # the question

- SQL QAs
    1. class = 2
    2. question = # the question
    3. answer = # the right value
    4. answer_type = # answer type like int, str, float

- Retrieve QAs
    1. class = 4
    2. question

Put the data into a list and save it to the JSON file.

```python
# Dataset architecture
dataset['data_list'] = ["Place your data"]
```

## Build the test dataset
It provides three test datasets in Make_test_dataset.ipynb.

We already have plenty of general data in General_QAs.json.

So we get 70 data from General_QAs.json. And build RAG and DB test datasets.

So, it is our content of the test data.
1. General QAs 70
2. SQL QAs 20 (include 5 error data)
3. Retrieve QAs 10

Feel free to test any ideas you want.
