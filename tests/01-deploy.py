#!/usr/bin/python3

import os
import amulet
import requests
#from .lib import helper
d = amulet.Deployment(series='trusty')
d.add('gitlab','cs:~f-tom-n/trusty/saikuanalytics-enterprise')
d.expose('gitlab')
try:
    # Create the deployment described above, give us 900 seconds to do it
    d.setup(timeout=900)
    # Setup will only make sure the services are deployed, related, and in a
    # "started" state. We can employ the sentries to actually make sure there
    # are no more hooks being executed on any of the nodes.
    d.sentry.wait()
except amulet.helpers.TimeoutError:
    amulet.raise_status(amulet.SKIP, msg="Environment wasn't stood up in time")
except:
    # Something else has gone wrong, raise the error so we can see it and this
    # will automatically "FAIL" the test.
    raise
# Shorten the names a little to make working with unit data easier
gitlab_unit = d.sentry['gitlab'][0]

home_page = requests.get('http://%s:80/' % gitlab_unit.info['public-address'])
#home_page = requests.get('http://repo.meteorite.bi:8098/')
home_page.raise_for_status() # Make sure it's not 5XX error

