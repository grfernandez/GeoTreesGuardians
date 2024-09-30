FROM apache/airflow:2.8.3

# Cambiar a usuario root para instalar paquetes
USER root

# Copiar el archivo de requisitos al contenedor
COPY requirements.txt /requirements.txt

RUN apt update
#RUN apt upgrade -y || true
RUN python -m pip install --upgrade pip
# Instalar las dependencias desde el archivo requirements.txt
#RUN pip install --no-cache-dir -r /requirements.txt || true


# Cambiar de nuevo al usuario airflow
USER airflow
RUN pip install --no-cache-dir -r /requirements.txt