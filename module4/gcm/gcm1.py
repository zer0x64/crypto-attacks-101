#!/usr/bin/env python3

import random
import base64
from argparse import ArgumentParser
from os import urandom
from flask import Flask, request, send_from_directory

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

app = Flask(__name__)

secret = ""
encrypted_secret = b""
key = b""
nonce = b""
tag = b"THIS IS A TAG"


def main():
    global secret, encrypted_secret, key, nonce
    secret = gen_flag()

    key = urandom(32)
    nonce = urandom(8)

    encrypted_secret = encrypt(secret.encode('utf-8'), tag)


def encrypt(data, tag):
    cipher = AESGCM(key)
    return tag + cipher.encrypt(nonce, data, tag)


def gen_flag():
    a = "0123456789abcdef"
    b = "FLAG-{"
    for _ in range(0, 32):
            b = b + random.choice(a)
    b = b + "}"
    return b


@app.route('/')
def get_index():
    return send_from_directory('website', 'index.html')


@app.route('/api/encrypt', methods=["POST"])
def post_encrypt():
    return base64.b64encode(encrypt(request.get_json().get('data').encode('utf-8'), request.get_json().get('tag').encode('utf-8')))


@app.route('/api/verify', methods=["POST"])
def verify_secret():
    if request.get_json().get('data') == secret:
        return "You won!"
    else:
        return "Invalid!"


@app.route('/api/leak')
def api_get_leak():
    return base64.b64encode(encrypted_secret)


@app.route('/<path:path>')
def get_website(path):
    return send_from_directory('website', path)


main()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-H',
                        '--host',
                        action='store',
                        dest='host',
                        default='127.0.0.1',
                        help='Host address')
    parser.add_argument('-p',
                        '--port',
                        action='store',
                        dest='port',
                        default=5000,
                        help='Host port')

    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
