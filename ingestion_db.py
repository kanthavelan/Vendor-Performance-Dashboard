import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time 

logging.basicConfig(
    filename = "datainv/logs/ingestion_db.log",
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine('sqlite:///datainv/inventory.db')

#Ingest the dataframe into DB
def ingest_db(df,table_name,engine):
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)

def load_raw_data():
    start = time.time()
    for file in os.listdir('datainv/data/'):
        if '.csv' in file:
            df = pd.read_csv('datainv/data/'+file)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
    end = time.time()
    total_time = (end-start)/60
    logging.info("------------Ingestion Complete---------------")
    
    logging.info(f'Total time taken {total_time} minutes')
    
if __name__ == '__main__':
    load_raw_data()