FROM python:3.9-slim-bullseye

WORKDIR /opt/app
COPY requirements.txt ./requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    && pip install --upgrade pip \
    && pip install --no-cache-dir --prefer-binary -r requirements.txt \
    && apt-get purge -y --auto-remove

COPY database ./database
COPY resources ./resources
COPY static ./static
COPY routes ./routes
#COPY models ./models
COPY app.py ./
#COPY .env ./

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]