FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

ENV DJANGO_SETTINGS_MODULE=WoutaBack.settings

RUN python manage.py collecstatic --noinput

RUN python manage.py migrate --noinput

EXPOSE 8000

CMD ["gunicorn","--bind","0.0.0.0:8000", "WoutaBack.wsgi:application"]