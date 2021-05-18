FROM python:3.8

WORKDIR /

ADD . /

RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "python", "app.py" ]