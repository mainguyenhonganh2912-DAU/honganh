FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
RUN python seed_data.py

EXPOSE 8000

CMD ["gunicorn", "du_an.wsgi:application", "--bind", "0.0.0.0:8000"]
