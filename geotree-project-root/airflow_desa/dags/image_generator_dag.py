from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
from PIL import Image, ImageOps
import random

# Directorio de imágenes original
IMAGE_DIR = '/opt/airflow/dags/data/processed/images/trees'
# Directorio para guardar las imágenes aumentadas
OUTPUT_DIR = '/opt/airflow/dags/data/processed/images/augmented_trees'

# Verifica si el directorio de salida existe, si no, créalo
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

default_args = {
    'owner': 'MLOps',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 20),
    'retries': 1,
}

dag = DAG(
    'image_generator_dag',
    default_args=default_args,
    description='DAG para crear imágenes espejadas e inclinadas para aumentar los datos',
    schedule_interval=None,  # Puedes ajustar el schedule si necesitas que sea periódico
)

def augment_images():
    """
    Función para generar imágenes espejadas e inclinadas
    """
    for root, dirs, files in os.walk(IMAGE_DIR):
        for filename in files:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, filename)
                img = Image.open(file_path)
                
                # Crear imagen espejada
                mirrored_img = ImageOps.mirror(img)
                # Guardar la imagen espejada
                mirrored_img.save(os.path.join(OUTPUT_DIR, f"mirrored_{filename}"))
                
                # Crear imagen inclinada (rotada)
                angle = random.randint(-30, 30)  # Rotación aleatoria entre -30 y 30 grados
                rotated_img = img.rotate(angle)
                # Guardar la imagen inclinada
                rotated_img.save(os.path.join(OUTPUT_DIR, f"rotated_{angle}_{filename}"))
                
                print(f"Imagen aumentada guardada: {filename}")

# Define la tarea para aumentar los datos
augment_images_task = PythonOperator(
    task_id='augment_images',
    python_callable=augment_images,
    dag=dag,
)

augment_images_task
