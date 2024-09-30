# dags/train_cnn.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.docker_operator import DockerOperator
import mlflow
import mlflow.keras
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Define el DAG
default_args = {
    'owner': 'MLOps',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'train_cnn',
    default_args=default_args,
    description='DAG para entrenar un modelo CNN y registrar en MLFlow',
    schedule_interval='@daily',  # Cambia según sea necesario
)

def train_model():
    # Cargar datos
    # Aquí deberías cargar tus datos de entrenamiento. Esto es solo un ejemplo.
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

    # Definir el modelo CNN
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    # Entrenar el modelo
    model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

    # Registrar el modelo en MLFlow
    mlflow.start_run()
    mlflow.keras.log_model(model, 'model')
    mlflow.log_params({'epochs': 5})
    mlflow.end_run()

def save_data():
    # Aquí puedes incluir código para guardar y preparar los datos si es necesario
    pass

# Define las tareas
save_data_task = PythonOperator(
    task_id='save_data',
    python_callable=save_data,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

# Define el flujo de tareas
save_data_task >> train_model_task
