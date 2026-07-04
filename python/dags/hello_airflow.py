from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

def extract_data() -> dict[str, int]:
    print("Extracting data...")
    return {"orders": 100, "customers": 2500}

def transform_data(**context):
    """
    Transforms the extracted data by calculating the average orders per customer 
    """
    task_instance = context["ti"] # get the task instance from the context 


    data = task_instance.xcom_pull(task_ids = "extract_data") # pulls the data from the extract_data task

    orders = data["orders"]
    revenue = data["revenue"]
    avg_order_value = revenue / orders

    print(f"Average order value: {avg_order_value}")
    
    return {
        "orders": orders,
        "revenue": revenue,
        "avg_order_value": avg_order_value
    }

def load_data(**context):
    task_instance  = context["ti"]
    transformed_data = task_instance.xcom_pull(task_ids = "transform_data")

    print("Loading data..")
    print(transformed_data)



with DAG(
        dag_id = "hello_airflow_etl",
        description = "A simple ETL pipeline in Airflow",
        start_date = datetime(2024, 1, 1),
        schedule = None,
        catchup = False,
        tags = ["example", "etl"],
        ) as dag:

    extract_task = PythonOperator(  # create a PythonOperator to run the extract_data function
        task_id = "extract_data",
        python_callable = extract_data,
    )

    transform_task = PythonOperator(
        task_id = "transform_data",
        python_callable = transform_data,
    )

    load_task = PythonOperator(
        task_id = "load_data",
        python_callable = load_data,
    )

    extract_task >> transform_task >> load_task # set the task dependencies
    
    
