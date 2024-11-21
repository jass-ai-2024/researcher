FROM python:3.12-slim as base
LABEL authors="evgeniigutin"

COPY requirements.txt .
WORKDIR /agent/
COPY tools /agent/tools
COPY utils /agent/utils
COPY runner.py .
COPY runner_tools.py .
COPY prompt_config.py .
COPY requirements.txt .
COPY app.py .
RUN pip3 install -r requirements.txt