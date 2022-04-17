#!/usr/bin/env python3.8
import random
import threading
import logging
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
VK_IDS = dict()
mysql_client = MysqlORMClient()
logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('test.log')
logger.addHandler(handler)


@app.route('/vk_id/<username>', methods=['GET'])
def get_vk_id(username):
    if check_active(username):
        if username not in VK_IDS:
            VK_IDS[username] = random_ascii(15)

        return jsonify({'vk_id': f'{VK_IDS[username]}'}), 200
    return jsonify({}), 404


def read_file(filename):
    file_lines = []
    with open(filename, 'r') as f:
        for line in f:
            file_lines.append(line.strip())

    return file_lines


def random_ascii(min_len=None, max_len=None):
    if max_len is None:
        max_len = min_len

    letters_set = read_file('./printable.txt')[0]

    return ''.join(random.choice(letters_set) for _ in range(random.randint(min_len, max_len)))


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')

    if terminate_func:
        terminate_func()


def check_active(username):
    mysql_client.session.commit()  # need to expire current models and get updated data from MySQL
    return bool(mysql_client.session.query(AppUsers).filter(
            AppUsers.username == username, AppUsers.active == 1).all())


@app.route('/shutdown')
def shutdown():
    mysql_client.connection.close()
    shutdown_mock()
    return jsonify(f'Ok, exiting'), 200


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': '0.0.0.0',
        'port': 4001
    })
    server.start()
    mysql_client.connect(db_created=True)
    return server


if __name__ == '__main__':
    # run_mock()
    try:
        run_mock()
    except ServerTerminationError:
        pass
    finally:
        mysql_client.connection.close()
