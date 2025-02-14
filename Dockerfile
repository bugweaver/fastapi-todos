FROM python:3-12-slim

COPY .. /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]