FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flet flet-fastapi uvicorn
EXPOSE 8080
CMD sh -c "python proempreusil.py --port ${PORT:-8080}"