FROM python:3.14.2
WORKDIR /app
COPY requirements.txt requirements.txt
COPY main.py main.py
RUN pip install -r requirements.txt
ENTRYPOINT ["fastapi", "run", "/app/main.py", "--port", "8080"]
