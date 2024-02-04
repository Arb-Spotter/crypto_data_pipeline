FROM python:3.10-slim

RUN apt update && apt install -y nodejs && apt install -y git

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY prisma/ /opt/dagster/app/prisma

RUN python3 -m prisma generate

COPY dags/ /opt/dagster/app/dags

COPY scripts/ /opt/dagster/app/scripts


ENV DAGSTER_HOME=/opt/dagster/dagster_home/

COPY dags/dagster.yaml $DAGSTER_HOME
COPY dags/workspace.yaml /opt/dagster/app

ENV PYTHONPATH="/opt/dagster/app"

WORKDIR /opt/dagster/app

RUN prisma generate


EXPOSE 3000

CMD ["sh", "-c", "prisma migrate deploy && dagster dev -h 0.0.0.0 -p 3000 -w workspace.yaml"]