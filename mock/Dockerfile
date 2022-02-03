FROM python:3.8

ADD requirements.txt /requirements.txt

RUN pip3.8 install -r /requirements.txt && rm -f /requirements.txt

ADD code /code
WORKDIR /code

CMD ["python3.8", "flask_mock.py"]