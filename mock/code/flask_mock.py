#!/usr/bin/env python3.8
import random
import string
import threading
import logging
import time
import signal
from flask import Flask, jsonify, request
from SQL.models.model import *
from SQL.mysql_orm.client import MysqlORMClient


class ServerTerminationError(Exception):
    pass


def exit_gracefully(signum, frame):
    raise ServerTerminationError()

# gracefully exit on -2
signal.signal(signal.SIGINT, exit_gracefully)
# gracefully exit on -15
signal.signal(signal.SIGTERM, exit_gracefully)

app = Flask(__name__)
VK_IDS = {}
mysql_client = MysqlORMClient()
logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('test.log')
logger.addHandler(handler)


@app.route('/vk_id/<username>', methods=['GET'])
def get_vk_id(username):
    if check_active(username):
        if username not in VK_IDS:
            VK_IDS[username] = generate_string()

        return jsonify({'vk_id': f'{VK_IDS[username]}'}), 200
    return jsonify({}), 404


def generate_string(length=6):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    random_string = random_string + str(int(time.time()) % 10000)
    return random_string


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')

    if terminate_func:
        terminate_func()


def check_active(username):
    mysql_client.session.commit()  # need to expire current models and get updated data from MySQL
    return mysql_client.session.query(AppUsers).filter(AppUsers.username==username,
                                                       AppUsers.access==1).all()


@app.route('/shutdown')
def shutdown():
    mysql_client.connection.close()
    shutdown_mock()
    return jsonify(f'Ok, exiting'), 200


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': '0.0.0.0',
        'port': 8081
    })
    server.start()
    mysql_client.connect(db_created=True)
    return server


if __name__ == '__main__':
    run_mock()
    try:
        run_mock()
    except ServerTerminationError:
        pass
    finally:
        mysql_client.connection.close()
