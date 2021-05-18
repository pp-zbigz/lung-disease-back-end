FROM python:3.7.3

WORKDIR /

ADD . /

RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "python", "app.py" ]