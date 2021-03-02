FROM python:3.7

COPY ./backend /app

RUN pip install -r /app/requirements.txt

EXPOSE 80

WORKDIR "/app/app"
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]