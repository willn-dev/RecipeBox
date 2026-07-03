FROM python:3.14-slim
WORKDIR /app
COPY dependencies/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000 
CMD ["gunicorn", "-w", "4", "-k", "gthread", "--threads", "2", "--bind", "0.0.0.0:8000", "app:app"]