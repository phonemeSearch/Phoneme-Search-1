FROM python:3.9

WORKDIR /opt/app

COPY . .

RUN pip install flask

RUN apt-get -y update && apt-get -y upgrade

RUN pip install pyicu

RUN apt-get -y install libicu-dev

RUN apt-get -y install pkg-config

RUN pip install indic_transliteration

RUN useradd py

USER py

CMD HOST=0.0.0.0 python3 backend.py
