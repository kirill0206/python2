import yaml
import socket
import json
import argparse
import logging
import logging.handlers
import hashlib
import zlib
from datetime import datetime

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
parser.add_argument(
    '-m', '--mode', type=str, default='w',
    help='Set client working mode: w - writing, or l - listening'
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

#add logging
LOG_FILENAME = 'log/client.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILENAME, encoding=ENCODING),
        logging.StreamHandler(),
        ]
    )


try:
    sock = socket.socket()
    sock.connect((host, port))

    logging.info(f'Client started.\nConnecting to {host}:{port}')

    if args.mode == 'w':
        while True:
            hash_obj = hashlib.sha256()
            hash_obj.update(
                str(datetime.now().timestamp()).encode(ENCODING)
            )

            action = input('Enter action name: ')
            data = input('Enter data to send: ')

            request = json.dumps(
                {
                    'action': action,
                    'data': data,
                    'time': datetime.now().timestamp(),
                    'user': hash_obj.hexdigest()
                }
            )

            sock.send(
                zlib.compress(
                    request.encode(encoding)
                )
            )
    elif args.mode == 'l':
        while True:
            b_data = sock.recv(buffersize)

            b_response = zlib.decompress(b_data)

            response = json.loads(
                b_response.decode(encoding)
            )

            print(response)
    else:
        logging.info(f'Wrong mode argument {args.mode}')

except KeyboardInterrupt:
    logging.info('Client closed')
    sock.close()
