FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV DATABASE_URL=sqlite:///data/seguros.db
VOLUME ["/app/data","/app/logs","/app/exports"]
CMD ["python", "-m", "neoroute.cli", "run"]
