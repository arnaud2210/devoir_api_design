FROM python:3.13.0-alpine
WORKDIR /usr/main
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "8000"]