
from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.email_operator import EmailOperator
import pandas as pd
import os
import sys
print(os.path.abspath("includes.............................."))
sys.path.append(os.path.abspath("includes"))

from loader import Warehouse
wr = Warehouse()


def run_loader(**context):
    data = pd.read_csv("~/data/extracted.csv")
    print(f"..................  {data.columns}")
    try:
        conn, cur = wr.DBConnect()
        print("Connected successfully!")
    except Exception as e:
        print(f"error...: {e}")
    
def create_db(**context):
    try:
        new_db = wr.createDB("warehouse")
        print("succesfully created new db {}".format(new_db))
    except Exception as e:
        print(f'error...: {e}')

def create_table(**context):
    try:
        wr.createTables("warehouse", "~/includes/schema.sql")
        print("successfully created tables!")
    except Exception as e:
        print(f'error...: {e}')

def load_data_to_table(**context):
    try:
        df = pd.read_csv("~/data/extracted.csv")
        df.drop(["Unnamed: 0"], axis=1, inplace=True)
        wr.insert_into_warehouse(dbName = 'mydatabase', df = df, table_name='elt')
    except Exception as e:
        print(f'error...: {e}')

default_args = {"owner":"airflow","start_date":datetime(2021,3,7)}
with DAG(dag_id="workflow",default_args=default_args,schedule_interval='@daily', catchup=False) as dag:

    connecting = PythonOperator(
        task_id = "create_connection",
        python_callable = run_loader,
        provide_context=True
        )

    new_db = PythonOperator(
        task_id = "create_new_db",
        python_callable = create_db,
        provide_context=True
    )

    new_table = PythonOperator(
        task_id = "create_new_table",
        python_callable = create_table,
        provide_context=True
    )

    fill_table = PythonOperator(
        task_id = "fill_table",
        python_callable = load_data_to_table,
        provide_context=True
    )

connecting >> new_db >> new_table >> fill_table
