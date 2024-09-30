FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos dentro del contenedor
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Establece el directorio de trabajo
WORKDIR /app

# Copia el resto de la aplicación
COPY ./app /app

# Expone el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Establece la variable de entorno para habilitar el modo de depuración
ENV FLASK_ENV=development

# Configura el comando por defecto para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]

