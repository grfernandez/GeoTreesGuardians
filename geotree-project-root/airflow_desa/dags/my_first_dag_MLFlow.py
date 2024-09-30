from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import mlflow

def test_mlflow_connection(**kwargs):
    # Configura la URI del servidor de MLFlow
    mlflow.set_tracking_uri("http://mlflow:5000")

    # Inicia un nuevo experimento en MLFlow
    mlflow.set_experiment("Test_Connection_Experiment2")

    with mlflow.start_run():
        # Loguea un parámetro y una métrica de prueba
        mlflow.log_param("test_param", "param_value")
        mlflow.log_metric("test_metric", 0.123)
        
        # Mensaje de log para confirmar la conexión
        print("MLFlow Test: Logged a test parameter and metric!")

# Definir el DAG
default_args = {
    'owner': 'MLOps',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 1),
    'retries': 1,
  
}


with DAG('my_first_dag_MLFlow', default_args=default_args, schedule_interval='@once') as dag:
    test_task = PythonOperator(
        task_id='my_first_dag_MLFlow',
        python_callable=test_mlflow_connection,
        provide_context=True
    )
