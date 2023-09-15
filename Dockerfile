FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

RUN pip install dagster-webserver dagster-postgres

# Copy your code and workspace to /opt/dagster/app
COPY dags/ /opt/dagster/app/

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Copy dagster instance YAML to $DAGSTER_HOME
COPY dags/dagster.yaml /opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

EXPOSE 3000


ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]
