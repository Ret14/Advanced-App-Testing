FROM python:3.8
COPY . /src

RUN pip3.8 install -r /src/requirements.txt && rm -f /src/requirements.txt

WORKDIR /src
CMD ["./start_tests.sh"]