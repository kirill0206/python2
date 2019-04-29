import yaml
import json
import socket
import argparse
import select
import logging
import threading
import logging.handlers

from handlers import handle_default_request
from actions import (
    resolve, get_server_actions
    )

from protocol import (
    validate_request, make_response, make_400, make_404
    )

from settings import (
    HOST, PORT, BUFFERSIZE, ENCODING
    )


host = HOST
port = PORT
buffersize = BUFFERSIZE
encoding = ENCODING


parser = argparse.ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration'
)
parser.add_argument(
    '-a', '--address', type=str, default=host,
    help='Set server IP ADDRESS for listening'
)
parser.add_argument(
    '-p', '--port', type=int, default=port,
    help='Set server PORT number for listening'
)
args = parser.parse_args()


if args.config:
    with open(args.config) as file:
        conf = yaml.load(file, Loader=yaml.Loader)
        host = conf.get('host', HOST)
        port = conf.get('port', PORT)
        buffersize = conf.get('buffersize', BUFFERSIZE)
        encoding = conf.get('encoding', ENCODING)

if args.address:
    host = args.address

if args.port:
    port = args.port

LOG_FILENAME = 'log/server.log'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILENAME, encoding=ENCODING),
        logging.StreamHandler()
        ]
    )

requests = []
connections = []


def read(client, request, buffersize):
    b_request = client.recv(buffersize)
    request.append(b_request)


def write(client, response):
    client.send(b_response)

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.settimeout(0)
    sock.listen(10)

    logging.info(f'Server started on {host}:{port}')

    while True:
        try:
            client, address = sock.accept()
            logging.info(f'Client with address {address} was detected')
            connections.append(client)
        except:
            pass

        rlist, wlist, xlist = select.select(
            connections, connections, connections, 0
        )

        for r_client in rlist:
            r_thread = threading.Thread(
                target=read,
                args=(r_client, requests, buffersize),
                daemon=True,
            )
            r_thread.start()

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)

            for w_client in wlist:
                w_thread = threading.Thread(
                    target=write,
                    args=(w_client, b_response),
                    daemon=True,
                )
                w_thread.start()

except KeyboardInterrupt:
    logging.info('Server closed')
