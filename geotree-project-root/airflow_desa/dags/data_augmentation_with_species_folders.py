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

default_args = {
    'owner': 'MLOps',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 20),
    'retries': 1,
}

dag = DAG(
    'data_augmentation_with_species_folders',
    default_args=default_args,
    description='DAG para crear imágenes espejadas e inclinadas manteniendo carpetas por especie',
    schedule_interval=None,
)

def augment_images():
    """
    Función para generar imágenes espejadas e inclinadas, y almacenarlas en carpetas correspondientes por especie.
    """
    for root, dirs, files in os.walk(IMAGE_DIR):
        for filename in files:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                # Ruta completa del archivo original
                file_path = os.path.join(root, filename)
                img = Image.open(file_path)

                # Obtener la subcarpeta de la especie
                relative_path = os.path.relpath(root, IMAGE_DIR)
                species_folder = os.path.join(OUTPUT_DIR, relative_path)

                # Crear la carpeta de salida si no existe
                if not os.path.exists(species_folder):
                    os.makedirs(species_folder)

                # Crear imagen espejada
                mirrored_img = ImageOps.mirror(img)
                # Guardar la imagen espejada en la carpeta correspondiente
                mirrored_img.save(os.path.join(species_folder, f"mirrored_{filename}"))
                
                # Crear imagen inclinada (rotada)
                angle = random.randint(-30, 30)  # Rotación aleatoria entre -30 y 30 grados
                rotated_img = img.rotate(angle)
                # Guardar la imagen rotada en la carpeta correspondiente
                rotated_img.save(os.path.join(species_folder, f"rotated_{angle}_{filename}"))
                
                print(f"Imágenes aumentadas guardadas en: {species_folder}")

# Define la tarea para aumentar los datos
augment_images_task = PythonOperator(
    task_id='augment_images',
    python_callable=augment_images,
    dag=dag,
)

augment_images_task
