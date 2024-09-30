# dags/train_cnn.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.utils import plot_model
import mlflow
import mlflow.keras


# Definir la ruta relativa a la carpeta 'dags'
#IMAGE_DIR = '/opt/airflow/dags/data/training/images/trees'
IMAGE_DIR = '/opt/airflow/dags/data/processed/images/trees'
#IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'data', 'training', 'images', 'trees')
# Ruta a los modelos
MODEL_DIR = '/opt/airflow/dags/models'
#MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

#if not os.path.exists(IMAGE_DIR):
#    raise FileNotFoundError(f"No se encontró el directorio de imágenes: {IMAGE_DIR}")

# Define el DAG
default_args = {
    'owner': 'MLOps',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 20),
    'retries': 1,
}

dag = DAG(
    'Identify_tree_species',
    default_args=default_args,
    description='DAG para entrenar un modelo CNN y registrar en MLFlow',
    schedule_interval='@daily',
)

def train_cnn_model():
    
    # Configuración de MLFlow
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("CNN_Identify_Tree_Specie")

    with mlflow.start_run() as run:
        # Parámetros
        img_height = 224
        img_width = 224
        batch_size = 32
        epochs = 20
        num_classes = len(os.listdir(IMAGE_DIR))  # Número de especies (carpetas)
        print("Cantidad de especies: " + str(num_classes))
        modelDescri = "CNN" 
        #num_classes = 3
        # Logging de parámetros en MLFlow

        mlflow.log_param("img_height", img_height)
        mlflow.log_param("img_width", img_width)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("c_species", num_classes)
        mlflow.log_param("model", modelDescri)
        #mlflow.description("Training CNN Model for identify tree species")

        # Generadores de datos con aumento
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        val_datagen = ImageDataGenerator(rescale=1./255)

        # Cargar las imágenes desde las carpetas
        train_generator = train_datagen.flow_from_directory(
            IMAGE_DIR,
            target_size=(img_height, img_width),
            batch_size=batch_size,
            class_mode='categorical'
        )

        validation_generator = val_datagen.flow_from_directory(
            IMAGE_DIR,
            target_size=(img_height, img_width),
            batch_size=batch_size,
            class_mode='categorical'
        )

        # Definir la arquitectura del modelo CNN
        model = Sequential([
            #Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
            Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
            MaxPooling2D(pool_size=(2, 2)),
            
            #Conv2D(64, (3, 3), activation='relu'),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
                      
            Conv2D(256, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),

            Flatten(),
            Dense(512, activation='relu'),
            #Dense(1024, activation='relu'),
            Dropout(0.5),
            #Dropout(0.4),
            Dense(num_classes, activation='softmax')  # Clasificación multicategoría
        ])
        

        #plot_model(model, to_file='cnn_model.png', show_shapes=True, show_layer_names=True)

        # Compilar el modelo
        #model.compile(optimizer=Adam(lr=0.001),
        #              loss='categorical_crossentropy',
        #              metrics=['accuracy'])
        model.compile(optimizer=Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'], run_eagerly=True)
        #model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'], run_eagerly=True)

        # Callbacks para guardar el mejor modelo y detener el entrenamiento si no mejora
        checkpoint = ModelCheckpoint(MODEL_DIR + '/identify_trees.h5', monitor='val_loss', save_best_only=True, mode='min')
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, mode='min')

        # Entrenar el modelo
        history = model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // batch_size,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=validation_generator.samples // batch_size,
            callbacks=[checkpoint, early_stopping]
        )

        # Cargar el mejor modelo y evaluarlo
        best_model = tf.keras.models.load_model(MODEL_DIR + '/identify_trees.h5')
        val_loss, val_acc = best_model.evaluate(validation_generator)

        # Loguear las métricas de evaluación en MLFlow
        mlflow.log_metric("Validation Loss", val_loss)
        mlflow.log_metric("Validation Accuracy", val_acc)

        # Guardar el modelo en MLFlow
        #mlflow.keras.log_model(best_model, MODEL_DIR + "/CNN_Identify_Tree_Specie")
        #mlflow.keras.log_model(keras_model=model, artifact_path="models/CNN_Identify_Tree_Specie", 
        #                   registered_model_name="CNN_Identify_Tree_Specie", 
        #                   keras_module=tf.keras, keras_version="2.4.0")
       # mlflow.tensorflow.log_model(tf_model=model, artifact_path="models/CNN_Identify_Tree_Specie", 
        #                    registered_model_name="CNN_Identify_Tree_Specie")

        print(f"Validation Loss: {val_loss}, Validation Accuracy: {val_acc}")

def save_data():
    # Aquí puedes incluir código para guardar y preparar los datos si es necesario
    pass

# Define las tareas
save_data_task = PythonOperator(
    task_id='save_data',
    python_callable=save_data,
    dag=dag,
)

train_cnn_model_task = PythonOperator(
    task_id='train_cnn_model',
    python_callable=train_cnn_model,
    dag=dag,
)

# Define el flujo de tareas
save_data_task >> train_cnn_model_task
