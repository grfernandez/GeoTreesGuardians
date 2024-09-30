#!/bin/bash

# Define the Docker Compose directories
APP_DIR="geotree-project-root"
AIRFLOW_DIR="$APP_DIR/airflow_desa"
MLFLOW_DIR="$APP_DIR/mlflow"
ELK_DIR="$APP_DIR/stack-elk"

# Define the Docker network for mlflow
NETWORK_NAME="geotreeguardians_network"

# Function to start docker-compose in a specified directory
start_docker_compose() {
  local dir=$1
  echo "Starting docker-compose in $dir"
  if [ "$dir" = "$AIRFLOW_DIR" ]; then
    echo "Starting docker-compose airflow"
     #(cd "$dir" && docker compose build --no-cache && docker compose up -d)
     (cd "$dir" && docker compose up -d)
  else
    (cd "$dir" && docker compose up -d)
  fi  
}

# Set up Airflow environment
setup_airflow() {
  echo "Setting up Airflow environment..."
  if [ ! -d "$AIRFLOW_DIR" ]; then
    mkdir "$AIRFLOW_DIR"
    cd "$AIRFLOW_DIR"
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.3/docker-compose.yaml'
    mkdir -p ./dags ./logs ./plugins ./config
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    cat .env
    docker compose up airflow-init
   else
     cd "$AIRFLOW_DIR"
     echo -e "AIRFLOW_UID=$(id -u)" > .env
     cat .env
     docker compose build airflow-init --no-cache
     docker compose up airflow-init
     echo "Airflow environment already set up."
   fi
}

# Create the network for mlflow if it doesn't exist
if ! docker network ls | grep -q "$NETWORK_NAME"; then
  echo "Creating Docker network: $NETWORK_NAME"
  docker network create "$NETWORK_NAME"
fi

# Set up Airflow

setup_airflow

cd ../..

# Start the Docker Compose services
start_docker_compose "$AIRFLOW_DIR"
start_docker_compose "$APP_DIR"
start_docker_compose "$MLFLOW_DIR"
#start_docker_compose "$ELK_DIR"

echo "All Docker Compose services have been started."

bash ./welcome.sh