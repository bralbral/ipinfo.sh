FROM python:3-slim-bullseye

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

VOLUME ["/var/lib/GeoIP"]

COPY . /app

EXPOSE 8080
ENV FLASK_APP=geoipweb
CMD [ "python", "-m" , "gunicorn", "geoipweb:app", "-w 2", "-b 0.0.0.0:8080" ]
