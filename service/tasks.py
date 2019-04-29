#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import celeryconfig

from celery import Celery
from celery import shared_task
import os
import tempfile
import subprocess
import os.path
import logging
import time
import signal

celery = Celery("tasks", broker='amqp://rabbitmq:rabbitmq@10.10.61.55:5672/')
celery.config_from_object(celeryconfig)


@celery.task
def add(x, y=1):
    return int(x) + int(y)


@shared_task
def mul(x, y):
    return x * y


@celery.task
def precmdline(precmdline):
    timeout = 60
    cmdpath = os.path.join("/usr/local/bin", "{0}.sh".format(precmdline))
    if not os.path.exists(cmdpath):
        msg = "命令错误：[{0}] 请检查重试...".format(precmdline)
        logging.error("cmdline:[{0}] error".format(precmdline))
        return msg
    try:
        ftemp = tempfile.TemporaryFile('w+')
        fileno = ftemp.fileno()
        t_beginning = time.time()
        p = subprocess.Popen(cmdpath, stderr=fileno, stdout=fileno, close_fds=True, preexec_fn=os.setsid, shell=True)
        seconds_passed = 0

        # flag来表示命令是正常退出还是超时
        flag = True
        while flag:
            if p.poll() is not None:
                break
            seconds_passed = time.time() - t_beginning
            if timeout and seconds_passed > timeout:
                logging.error("precmdline exec [{0}]s > [{1}]s, 请检查网络重试...".format(precmdline, timeout))
                os.killpg(p.pid, signal.SIGUSR1)
                flag = False
                break
        if not flag:
            msg = "命令超时： [{0}] exec [{1}]s > [{2}]s,请检查网络重试...".format(precmdline, seconds_passed, timeout)
        else:
            ftemp.seek(0)
            msg = ftemp.read()
        logging.warning("precmdline:[{0}] exec finish in total [{1}]s".format(precmdline, seconds_passed))
    finally:
        if ftemp:
            ftemp.close()

    return msg


@celery.task
def sync_to_pro(cmdline, version):
    cmdpath = os.path.join("/usr/local/bin", "{0}.sh".format(cmdline))
    if not os.path.exists(cmdpath):
        msg = "命令错误：[{0}] 请检查重试...".format(cmdline)
        logging.error("cmdline:[{0}] error".format(cmdline))
        return msg

    try:
        ftemp = tempfile.TemporaryFile('w+')
        fileno = ftemp.fileno()
        t_beginning = time.time()
        commond = "%s %s" % (cmdpath, version)
        p = subprocess.Popen(commond, stderr=fileno, stdout=fileno, close_fds=True,
                             preexec_fn=os.setsid, shell=True)

        seconds_passed = 0
        timeout = 60

        # flag来表示命令是正常退出还是超时
        flag = True
        while flag:
            if p.poll() is not None:
                break
            seconds_passed = time.time() - t_beginning
            if timeout and seconds_passed > timeout:
                logging.error("命令超时： shell [{0}] exec timeout:[{1}]s > [{2}]s".format(cmdline, seconds_passed, timeout))
                os.killpg(p.pid, signal.SIGUSR1)
                flag = False
                break
            time.sleep(0.1)
        if not flag:
            msg = "命令超时: [{0}] exec timeout: [{1}]s > [{2}]s".format(cmdline, seconds_passed, timeout)
        else:
            ftemp.seek(0)
            msg = ftemp.read()
        logging.warning(
            " 命令执行cmdline:[{0}] version:[{1}] exec finish in total [{2}]s ".format(cmdline, version, seconds_passed))
    finally:
        if ftemp:
            ftemp.close()

    return msg
