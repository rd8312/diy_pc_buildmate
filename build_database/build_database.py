import sqlite3  

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--database_path', dest='db_path')
    parameter_args = parser.parse_args()

    db_path = parameter_args.db_path
    
    conn = sqlite3.connect(db_path)  
    
    print("Opened database successfully")  

    # %%
    # 建立表格 
    cursor = conn.cursor()

    table_name = 'Product'
    conn.execute(f'''CREATE TABLE {table_name} 
        (ID INT PRIMARY KEY     NOT NULL, 
        NAME          TEXT      NOT NULL, 
        PRICE         INT, 
        COMPANY         TEXT);''')  

    # %%
    # 拉資料進表格
    import sqlite3  
    
    conn = sqlite3.connect(db_path)  
    print("Opened database successfully")  

    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (1, 'B760M-K-CSM', 10590, '華碩')")
    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (2, 'H610M-E',2290,'微星')")
    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (3, 'B760M-D2H',3090,'技嘉')")
    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (4, 'H770-PRO',6590,'華碩')")

    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (5, 'Kingston-Beast-16GB',1520,'金士頓')")
    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (6, 'ADATA-16GB',1599,'威剛')")
    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (7, 'Crucial-8G',729,'美光')")
    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (8, 'Crucial-32GB',2699,'美光')")

    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (9, 'i7-14900K',20400,'Intel')")
    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (10, 'i7-14700KF',13200,'Intel')") 
    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (11, 'R5-7600X',7950,'AMD')") 
    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (12, 'R9-7900X',15150,'ADM')") 

    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (13, 'ZOTAC-GT730',2350,'ZOTAC')")
    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (14, 'MSI-GT710',1790,'微星')")
    conn.execute(f"INSERT INTO {table_name} (ID,NAME,PRICE,COMPANY) VALUES (15, 'GIGABYTE-RTX4070Ti',24900,'技嘉')")

    conn.commit()  
    print("Records inserted successfully")  
    conn.close()  

    # %%



