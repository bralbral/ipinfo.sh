FROM python:3-slim-bullseye

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

VOLUME ["/var/lib/GeoIP"]

COPY . /app

ENV FLASK_APP=geoipweb
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80" ]
