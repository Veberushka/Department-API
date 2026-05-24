FROM python:3.12-slim
WORKDIR /app
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt
COPY . .
ENV ENV_FILE=.env.container
CMD sh -c "sleep 5 &&(alembic revision --autogenerate -m 'initial' 2>/dev/null || true) && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"
