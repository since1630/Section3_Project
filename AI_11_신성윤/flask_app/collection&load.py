import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import sqlite3
import time
import os
import seaborn as sns
import numpy as np
import pickle


# 한국은행 경제통계시스템에서 json파일 추출
def json_extract(code , code_1):
    url = f'http://ecos.bok.or.kr/api/StatisticSearch/01KMMYPUUJUY1462YFP6/json/kr/1/140/{code}/MM/2012/2022/{code_1}'
    resp = requests.get(url)
    time.sleep(1)
    html = resp.content.decode('utf-8', 'replace')
    soup = BeautifulSoup(html, 'html.parser')
    json_file = json.loads(soup.text)
    
    return json_file


# 받은 json파일을 Mongo DB 에 저장하는 함수
def mongo_save(COLLECTION_NAME,db_name,json_file):
    
    HOST = 'cluster0.cvd37.mongodb.net'
    USER = 'since1630'
    PASSWORD = '*****'
    DATABASE_NAME = 'Section3_Project'
    COLLECTION_NAME = f'{COLLECTION_NAME}'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
    DB_FILENAME = f'{db_name}'
    DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)
    
    client = MongoClient(MONGO_URI)
    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]
    collection.insert_many([json_file])
    print('Mongo DB Atlas 에 json 파일 저장 완료')



# m1_value = json_extract('010Y002','AAAA17')
# mongo_save('m1_value','m1_value.db',m1_value)

# chaekwon_value = json_extract('028Y001','BEEA42')
# mongo_save('chaekwon_value','chaekwon_value.db',chaekwon_value)

# call_value = json_extract('028Y001','BEEA16')
# mongo_save('call_value','call_value.db',call_value)

# koribor_3month = json_extract('028Y001','BEEA20')
# mongo_save('koribor_3month','koribor_3month.db',koribor_3month)

# economic_growth_rate = json_extract('901Y001','AI1AA')
# mongo_save('economic_growth_rate','economic_growth_rate.db', economic_growth_rate)

# mingan_consume = json_extract('901Y001','AI1AB')
# mongo_save('mingan_consume','mingan_consume.db', mingan_consume)

# facility_stock = json_extract('901Y001','AI1AC')
# mongo_save('facility_stock','facility_stock.db' , facility_stock)

# construct_stock = json_extract('901Y001','AI1AD')
# mongo_save('construct_stock','construct_stock.db', construct_stock)

# make_avr = json_extract('901Y001','AI1AH')
# mongo_save('make_avr','make_avr.db', make_avr)

# employer_rate = json_extract('901Y001','AI1AK')
# mongo_save('employer_rate','employer_rate.db', employer_rate)

# base_inflation = json_extract('901Y001','AI1BC')
# mongo_save('base_inflation','base_inflation.db',base_inflation)

# dollar_save = json_extract('901Y001','AI1DC')
# mongo_save('dollar_save','dollar_save.db',dollar_save)

# base_usa_interest = json_extract('I10Y014','US')
# mongo_save('base_usa_interest','base_usa_interest.db',base_usa_interest)

# usa_ppi = json_extract('I10Y021','US')
# mongo_save('usa_ppi','usa_ppi.db', usa_ppi)

# kosdaq_value = json_extract('028Y015','2090000')
# mongo_save('kosdaq_value','kosdaq_value.db',kosdaq_value)


def create_table(db_name):
    
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    cur.execute("""
        DROP TABLE IF EXISTS macro_economic;
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS macro_economic(
            dollar_save INTEGER,
            facility_stock INTEGER,
            economic_growth_rate INTEGER,
            m1_value INTEGER,
            base_usa_interest INTEGER,
            treasury_bonds_3year INTEGER,
            base_inflation INTEGER,
            usa_ppi INTEGER,
            kosdaq_value INTEGER,
            koribor_3month INTEGER,
            private_consumption_rate INTEGER,
            interest_rate INTEGER,
            employer_rate INTEGER,
            construct_stock INTEGER,
            kospi_value INTEGER,
            make_avr INTEGER,
            time VARCHAR(20) NOT NULL PRIMARY KEY
        );
    """)
    
    conn.commit()
    

create_table('macro_economic.db')

def pre_insert(db_name):
    HOST = 'cluster0.cvd37.mongodb.net'
    USER = 'since1630'
    PASSWORD = '*****'
    DATABASE_NAME = 'Section3_Project'
    COLLECTION_NAME = 'kospi_value'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
    DB_FILENAME = f'{db_name}'
    DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)

    client = MongoClient(MONGO_URI)
    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]
    
    collection_list = list(collection.find())[0]['StatisticSearch']['row']
    value_final = []
    
    for x in range(len(collection_list)-1):
        value = []
        value_final.append(value)
        for j in database.list_collection_names():
            collection = database[j]
            value.append(list(collection.find())[0]['StatisticSearch']['row'][x]['DATA_VALUE'])
        value.append(list(collection.find())[0]['StatisticSearch']['row'][x]['TIME'])


            
    return value_final
        
        
    
value_final = pre_insert('macro_economic.db')

def table_insert(db_name , value_final):
    
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    for i in value_final:
        cur.execute("""
            INSERT OR IGNORE INTO macro_economic(
            dollar_save,
          facility_stock,
          economic_growth_rate,
          m1_value,
          base_usa_interest,
          treasury_bonds_3year,
          base_inflation,
          usa_ppi,
          kosdaq_value,
          koribor_3month,
          private_consumption_rate,
          interest_rate,
          employer_rate,
          construct_stock,
          kospi_value,
          make_avr,
          time)
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
        """, i)
        
    conn.commit()
    cur.close()
    conn.close()


table_insert('macro_economic.db',value_final)
