import yaml
import json
import socket
import argparse

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


try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(10)

    print(f'Server started on {host}:{port}')

    while True:
        client, address = sock.accept()
        print(f'Client with address {address} was detected')

        b_data = client.recv(buffersize)
        request = json.loads(b_data.decode(encoding))
        response = json.dumps(request)

        client.send(response.encode(encoding))
        client.close()

except KeyboardInterrupt:
    print('Server closed')