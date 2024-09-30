from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os
from PIL import Image

# Rutas de entrada y salida
INPUT_PATH = '/opt/airflow/dags/data/training/images/trees'
OUTPUT_PATH = '/opt/airflow/dags/data/processed/images/trees'
IMAGE_SIZE = (224, 224)  # Tamaño deseado para las imágenes

# Función para procesar las imágenes
def preprocess_images():
    # Crear el directorio de salida si no existe
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    # Recorrer todas las carpetas de especies
    for species_folder in os.listdir(INPUT_PATH):
        species_input_path = os.path.join(INPUT_PATH, species_folder)
        species_output_path = os.path.join(OUTPUT_PATH, species_folder)
        
        # Crear la carpeta de salida si no existe
        if not os.path.exists(species_output_path):
            os.makedirs(species_output_path)
        
        # Recorrer cada imagen dentro de la carpeta de la especie
        for image_file in os.listdir(species_input_path):
            image_input_path = os.path.join(species_input_path, image_file)
            
            # Procesar solo archivos de imagen
            if image_file.endswith(('.jpg', '.png', '.jpeg')):
                try:
                    img = Image.open(image_input_path)
                    # Convertir a RGB si es necesario
                    img = img.convert('RGB')
                    # Redimensionar la imagen
                    img = img.resize(IMAGE_SIZE)
                    # Guardar la imagen preprocesada
                    image_output_path = os.path.join(species_output_path, image_file)
                    img.save(image_output_path)
                    print(f'Processed: {image_input_path}')
                except Exception as e:
                    print(f'Error processing {image_input_path}: {e}')

# Definir el DAG de Airflow
default_args = {
    'owner': 'MLOps',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 24),
    'retries': 1,
}

with DAG(
    'image_preprocessing_dag',
    default_args=default_args,
    description='DAG for image preprocessing',
    schedule_interval=None,  # Ejecutar manualmente
    catchup=False
) as dag:

    # Tarea de procesamiento de imágenes
    preprocess_images_task = PythonOperator(
        task_id='preprocess_images',
        python_callable=preprocess_images
    )
