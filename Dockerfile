FROM python:3.9

WORKDIR /opt/app

COPY . .

RUN pip install flask

RUN useradd py

USER py

CMD HOST=0.0.0.0 python3 backend.py
