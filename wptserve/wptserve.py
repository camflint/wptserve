#!/usr/bin/env python
import argparse
import os
import logging

import server
import openssl
from logger import logger


def abs_path(path):
    return os.path.abspath(path)


def parse_args():
    parser = argparse.ArgumentParser(description="HTTP server designed for extreme flexibility "
                                     "required in testing situations.")
    parser.add_argument("document_root", action="store", type=abs_path,
                        help="Root directory to serve files from")
    parser.add_argument("--port", "-p", dest="port", action="store",
                        type=int, default=8000,
                        help="Port number to run server on")
    parser.add_argument("--host", "-H", dest="host", action="store",
                        type=str, default="127.0.0.1",
                        help="Host to run server on")
    parser.add_argument("--use-ssl", dest="use_ssl", action="store_true")
    parser.add_argument("--install-certs", dest="install_certs", action="store_true")
    parser.add_argument("--cert-root", dest="cert_root", action="store",
                        type=str, default=os.path.join(os.getcwd(), ".certs"))
    parser.add_argument("--log-file", dest="log_file", action="store",
                        type=str, default=None)
    return parser.parse_args()


def main():
    args = parse_args()

    cert_path = None
    key_path = None
    if args.use_ssl:
        cert_root = args.cert_root
        if not os.path.exists(cert_root):
            os.mkdir(cert_root)

        with openssl.OpenSSLEnvironment(logger, base_path=cert_root, install_certs=args.install_certs) as ssl_env:
            key_path, cert_path = ssl_env.host_cert_path([args.host])
            logger.info("Using host cert: %s" % cert_path)

    httpd = server.WebTestHttpd(host=args.host, port=args.port,
                                use_ssl=args.use_ssl, certificate=cert_path, key_file=key_path,
                     doc_root=args.document_root)
    httpd.start(block=True)


if __name__ == "__main__":
    main()
