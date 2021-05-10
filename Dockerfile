FROM python:3.8.5

WORKDIR /app 

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "python", "app.py" ]