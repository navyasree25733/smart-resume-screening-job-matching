FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm

EXPOSE 7860

CMD uvicorn app.main:app --host 0.0.0.0 --port 7860