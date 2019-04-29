#!/usr/bin/env python
# -*- coding:utf-8 -*-

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

from flask import Flask
from flask import request
from service import tasks
from gevent.pywsgi import WSGIServer
import logging

app = Flask(__name__)


@app.route('/test')
def test():
    return 'hello test'


@app.route('/add')
def a1():
    a = request.args.get("x")
    print("add args: %s" % a)
    ret = tasks.add(a)
    return str(ret)


@app.route('/sh')
def cmd():
    precmdline = request.args.get("precmdline")
    cmdline = request.args.get("cmdline")
    version = request.args.get("version")

    retall = []
    if precmdline:
        msg = tasks.precmdline.apply_async(args=[precmdline], queue='taskpre')
        ret = msg.get()
        retall.append(ret)

    if cmdline and version:
        msg1 = tasks.sync_to_pro.apply_async(args=[cmdline, version], queue='publish')
        ret1 = msg1.get()
        retall.append(ret1)
    app.logger.warning(
        "precmdline: [{0}] cmdline:[{1}] version:[{2}] exec finish.".format(precmdline, cmdline, version))
    return "".join(retall)


if __name__ == '__main__':
    handler = logging.FileHandler('sync.log', encoding='UTF-8')
    handler.setLevel(logging.INFO)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run("0.0.0.0")
    WSGIServer(('0.0.0.0', 5000), app).serve_forever()
