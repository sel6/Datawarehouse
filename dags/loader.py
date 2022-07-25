import pandas as pd
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.email_operator import EmailOperator


  def DBConnect(dbName=None):
        """
        A function to connect to SQL database
        """
        mydb = cu.connect(host='localhost', user='root',
                          password='Selam@0102.',
                             database=dbName, buffered=True)
        cursor = mydb.cursor()
        return mydb, cursor
    def createDB(dbName: str) -> None:
        """
        A function to create SQL database
        """
        mydb, cursor = self.DBConnect()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
        mydb.commit()
        cursor.close()
    def createTables(dbName: str) -> None:
        """
        A function to create SQL table
        """
        mydb, cursor = self.DBConnect(dbName)
        sqlFile = 'schema.sql'
        fd = open(sqlFile, 'r')
        readsqlFile = fd.read()
        fd.close()
        sqlCommands = readsqlFile.split(';')
        for command in sqlCommands:
            try:
                result = cursor.execute(command)
            except Exception as e:
                print('command skipped: ', command)
                print(e)
        mydb.commit()
        cursor.close()
        
    def insert_into_warehouse(dbName: str, df: pd.DataFrame, table_name: str) -> None:
        """
        A function to insert values in SQL table
        """
        mydb, cursor = self.DBConnect(dbName)
        for _, row in df.iterrows():
            sqlQuery = f"""INSERT INTO {table_name} 
            (track_id, cars, traveled_d, avg_speed, lat, lon,
                        speed, lon_acc, lat_acc, time)
                  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9])
            try:
                cursor.execute(sqlQuery, data)
                mydb.commit()
                print('Data inserted successfully')
            except Exception as e:
                mydb.rollback()
                print('Error: ', e)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['kabodshekinah@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    "start_date": datetime(2022, 7, 20, 2, 30, 00),
    'retry_delay': timedelta(minutes=5)
}

with DAG(
        "load_dag",
        default_args=default_args,
        schedule_interval="0 * * * *",
        catchup=False,
) as dag:
    connect_db_op = PythonOperator(
        task_id="connectDB", 
        python_callable=DBConnect
    )
    insert_op = MySQLOperator(
        task_id="insert_into_warehouse",
        mysql_conn_id="mysql_conn_id",
        sql="/mysql/schema.sql",
        dag=dag
        
    )
connect_db_op >> insert_op
