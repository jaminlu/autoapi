# /usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class TimeoutError(Exception):
    pass


def req(url, timeout=10):
    try:
        r = requests.get(url, timeout=timeout)
    except Exception as err:
        return {"err": err}
    return r.text
