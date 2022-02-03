FROM python:3.8

ADD requirements.txt /requirements.txt

RUN pip3.8 install -r /requirements.txt && rm -f /requirements.txt

WORKDIR /src
CMD ["./start_tests.sh"]