#!/usr/bin/env python
import json
import os
import public
import requests

"""
https://developer.github.com/v3/repos/hooks/
"""

@public.add
def request(method, url, data=None, **kwargs):
    """make request and return response"""
    token = os.environ["GITHUB_TOKEN"]
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    kwargs["headers"].update({"Authorization": "Bearer %s" % token})
    if data is not None:
        data = json.dumps(data)
    r = requests.request(method, url, data=data, **kwargs)
    r.raise_for_status()
    return r


@public.add
def get(fullname):
    """return list of repo webhooks data"""
    api_url = "https://api.github.com/repos/%s/hooks" % fullname
    return request("GET", api_url).json()


@public.add
def delete(fullname, hook_id):
    """delete repo webhook"""
    api_url = "https://api.github.com/repos/%s/hooks/%s" % (fullname, hook_id)
    request("DELETE", api_url)