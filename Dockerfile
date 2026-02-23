FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]

FROM base AS test

RUN pip install --no-cache-dir -r requirements-test.txt

CMD ["pytest", "--cov=app", "tests/", "-v"]
