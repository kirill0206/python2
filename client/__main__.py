import yaml
import socket
import json
import argparse
import logging
import logging.handlers

from settings import (HOST, PORT, BUFFERSIZE, ENCODING)


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
    help='Set server IP ADDRESS for connection'
)
parser.add_argument(
    '-p', '--port', type=int, default=port,
    help='Set server PORT number for connection'
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

LOG_FILENAME = 'log/client.log'

logger = logging.getLogger('client')
logging.basicConfig(
    filename=LOG_FILENAME,
    filemode='w+',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

formatter = logging.Formatter(
    '%(asctime)-10s - %(levelname)-8s - %(name)-6s - %(message)s'
)

handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=1024,
    backupCount=7,
    encoding=ENCODING,
)

handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)


try:
    sock = socket.socket()
    sock.connect((host, port))

    logging.info(f'Client started.\nConnecting to {host}:{port}')

    data = input('Input data to send')
    request = json.dumps(
        {'data': data}
    )

    sock.send(request.encode(encoding))

    b_data = sock.recv(buffersize)
    response = json.loads(b_data.decode(encoding))

    logging.info('Get response: ', response)
    sock.close()

except KeyboardInterrupt:
    logging.info('Client closed')
