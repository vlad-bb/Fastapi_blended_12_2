from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from threading import Thread
from pathlib import Path
import urllib.parse
import mimetypes
import json
import logging
import socket
import os

jinja = Environment(loader=FileSystemLoader('templates'))
BUFFER_SIZE = 1024
HTTP_PORT = 3000
HTTP_HOST = '0.0.0.0'
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 5000
BASE_DIR = Path()


class OurHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case '/':
                self.send_html('index.html')
            case '/contact':
                self.send_html('message.html')
            case '/blog':
                self.render_template('blog.jinja')
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html('error.html', 404)

    def do_POST(self):
        size = self.headers.get('Content-Length')
        data = self.rfile.read(int(size))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(data, (SOCKET_HOST, SOCKET_PORT))

        self.send_response(302)
        self.send_header('Location', '/contact')
        self.end_headers()

    def render_template(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Context-Type', 'text/html')
        self.end_headers()
        with open('storage/db.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        template = jinja.get_template(filename)
        msg = 'Hello world!'
        html = template.render(blogs=data, msg=msg)
        self.wfile.write(html.encode('utf-8'))

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Context-Type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Context-Type', mime_type)
        else:
            self.send_header('Context-Type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())


def load_data_from_form():
    if os.path.exists('data/data.json'):
        with open('data/data.json', 'r', encoding='utf-8') as file:
            if os.path.getsize('data/data.json') != 0:
                dict_from_file = json.load(file)
                return dict_from_file


def save_data_from_form(data):
    parse_data = urllib.parse.unquote_plus(data.decode())
    try:
        parse_dict = {key: value for key, value in [el.split('=') for el in parse_data.split('&')]}
        parse_with_date = {f'{datetime.now()}': parse_dict}
        dict_from_file = load_data_from_form()
        if dict_from_file:
            parse_with_date.update(dict_from_file)
        with open('data/data.json', 'w', encoding='utf-8') as file:
            json.dump(parse_with_date, file, ensure_ascii=False, indent=4)
    except ValueError as err:
        logging.error(err)
    except OSError as err:
        logging.error(err)


def run_socket_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    logging.info('Starting socket server')
    try:
        while True:
            msg, addr = server_socket.recvfrom(BUFFER_SIZE)
            logging.info(f'Socket received {addr}: {msg}')
            save_data_from_form(msg)
    except KeyboardInterrupt:
        pass
    finally:
        server_socket.close()


def run_http_server(host, port):
    server_address = (host, port)
    http = HTTPServer(server_address, OurHttpServer)
    logging.info('Starting http server')
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        http.server_close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(threadName)s] - %(message)s')

    http_server = Thread(target=run_http_server, args=(HTTP_HOST, HTTP_PORT))
    http_server.start()

    sock_server = Thread(target=run_socket_server, args=(SOCKET_HOST, SOCKET_PORT))
    sock_server.start()
