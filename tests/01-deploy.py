#!/usr/bin/python3


import amulet
import requests
import unittest


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.d = amulet.Deployment(series='xenial')
        self.d.add('gitlab', 'cs:~spiculecharms/gitlab-server')
        self.d.expose('gitlab')

        self.d.add('haproxy', 'cs:haproxy')
        self.d.expose('haproxy')
    

        self.d.setup(timeout=1200)
        self.d.sentry.wait()

        self.gitlab_unit = self.d.sentry['gitlab'][0]

    def test_service(self):

        haproxy_unit = d.sentry['haproxy'][0]

        home_page = requests.get('http://%s:80/' % gitlab_unit.info['public-address'])
        home_page.raise_for_status()  # Make sure it's not 5XX error
        assert "GitLab Community Edition" in home_page.text

        d.relate('haproxy:reverseproxy', 'gitlab:website')

        home_page = requests.get('http://%s:80/' % haproxy_unit.info['public-address'])
        home_page.raise_for_status()

        assert "GitLab Community Edition" in home_page.text

    def test_change_url(self):
        d.configure('gitlab', {
            'external_url': 'http://test.spiculecharms.com',
        })

        contents = d.sentry['gitlab/0'].file_contents('/etc/gitlab/gitlab.rb')

        assert "test.spiculecharms.com" in contents


    def test_set_root_password(self):


    def test_login(self):

    def test_create_repo(self):

    def test_push_to_repo(self):