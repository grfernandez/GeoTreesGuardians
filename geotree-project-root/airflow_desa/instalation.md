cd ~
mkdir airflow_desa
cd airflow_desa
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.3/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
cat .env
docker compose up airflow-init
docker compose up