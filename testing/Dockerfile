FROM python:3.8
ADD requirements.txt /src/requirements.txt

RUN pip3.8 install -r /src/requirements.txt && rm -f /src/requirements.txt

ADD start_tests.sh /src/start_tests.sh
RUN chmod +x /src/start_tests.sh
ADD code /src/code

WORKDIR /src
CMD ["./start_tests.sh"]