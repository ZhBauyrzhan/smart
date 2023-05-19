FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN python3.10 -m pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN python3.10 -m pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /proj
WORKDIR /proj

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]