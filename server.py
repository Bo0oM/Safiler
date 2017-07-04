#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ds_store import DSStore
import cgi, json, os, sys, posixpath
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

reload(sys)
sys.setdefaultencoding("utf8")

DIR_NAME = os.path.dirname(os.path.realpath(__file__)) + '/userdata'


def parse(file):
    filelist = []
    for i in file:
        if i.filename != '.':
            filelist.append(i.filename)
    return list(set(filelist))


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("get")

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        for field in form.keys():
            field_item = form[field]

            if field_item.filename:
                filename = os.path.join(DIR_NAME + posixpath.abspath('/' + field_item.filename))

                if not os.path.exists(os.path.dirname(filename)):
                    try:
                        os.makedirs(os.path.dirname(filename))
                    except:
                        pass
                try:

                    with open(filename, "wb") as f:
                        file_data = field_item.file.read()
                        f.write(file_data)
                        print('Uploaded:' + field_item.filename)

                except: pass

                try:
                    with DSStore.open(filename) as d:
                        fileresult = parse(d)
                        self.wfile.write(json.dumps(fileresult, ensure_ascii=False, encoding="utf-8"))
                        print(filename+': '+ json.dumps(fileresult, ensure_ascii=False, encoding="utf-8"))
                except:
                    pass


def run(server_class=HTTPServer, handler_class=S, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Server listening on', port
    httpd.serve_forever()


try:
    if __name__ == "__main__":
        from sys import argv

        if len(argv) == 2:
            run(port=int(argv[1]))
        else:
            run()
except KeyboardInterrupt:
    print '^C received, shutting down the web server'
# httpd.socket.close()

