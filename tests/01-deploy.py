#!/usr/bin/python3

# import os
import amulet
import requests

d = amulet.Deployment(series='xenial')
d.add('gitlab', 'cs:~spiculecharms/gitlab-server')
d.expose('gitlab')

d.add('haproxy', 'cs:haproxy')
d.expose('haproxy')

try:
    d.setup(timeout=1200)
    d.sentry.wait()
except amulet.helpers.TimeoutError:
    amulet.raise_status(amulet.SKIP, msg="Environment wasn't stood up in time")
except:
    raise

gitlab_unit = d.sentry['gitlab'][0]
haproxy_unit = d.sentry['haproxy'][0]

home_page = requests.get('http://%s:80/' % gitlab_unit.info['public-address'])
home_page.raise_for_status()  # Make sure it's not 5XX error
assert "GitLab Community Edition" in home_page.text

d.relate('haproxy:reverseproxy', 'gitlab:website')

home_page = requests.get('http://%s:80/' % haproxy_unit.info['public-address'])
home_page.raise_for_status()

assert "GitLab Community Edition" in home_page.text


d.configure('gitlab', {
    'external_url': 'http://test.spiculecharms.com',
})

contents = d.sentry['gitlab/0'].file_contents('/etc/gitlab/gitlab.rb')

assert "test.spiculecharms.com" in contents
