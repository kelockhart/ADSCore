import sys
import os
from flask_testing import TestCase
from flask import request
from flask import url_for, Flask
import unittest
import requests
import time
import urllib.parse
import json
import httpretty

from adscore import app, api
from adscore.constants import SEARCH_SERVICE


class TestApi(TestCase):
    def create_app(self):
        '''Create the wsgi application'''
        app_ = app.__init__('app_')
        return app_

    @httpretty.activate
    def test_abstract(self):
        identifier = '2019Test..........A'
        headers = {"Authorization": "Bearer:{}".format('secrets'), }
        params = urllib.parse.urlencode({
            'fl': 'title,bibcode,author,pub,pubdate,abstract,citation_count,[citations],read_count,esources,property',
            'q': 'identifier:{0}'.format(identifier),
            'rows': '25',
            'sort': 'date desc, bibcode desc',
            'start': '0'
        })
        url = SEARCH_SERVICE + "?" + params
        body = {u'responseHeader': {u'status': 0,
                                    u'QTime': 1015,
                                    u'params': {u'x-amzn-trace-id': u'trace',
                                                u'rows': u'1',
                                                u'q': u'identifier:{0}'.format(identifier),
                                                u'start': u'0',
                                                u'wt': u'json',
                                                u'fl': u'title,bibcode,author,pub,pubdate,abstract,citation_count,[citations],read_count,esources,property'}},
                u'response': {u'start': 0,
                              u'numFound': 1,
                              u'docs': [{u'title': [u"title"],
                                         u'bibcode': '{0}'.format(identifier),
                                         u'author': [u'Lname, F'],
                                         u'pub': u'Publication',
                                         u'pubdate': u'2019-08-01',
                                         u'abstract': u'This is an abstract',
                                         u'citation_count': 5,
                                         u'[citations]': {u'num_references': 15, u'num_citations': 5},
                                         u'read_count': 10,
                                         u'esources': [u'EPRINT_HTML'],
                                         u'property': [u'ARTICLE']}]}}

        httpretty.register_uri(
            httpretty.GET, url,
            status=200,
            content_type='application/json',
            body=body
        )

        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['cookies'] = 'cookies'
                sess['auth']['access_token'] = 'secrets'

            results = api.abstract(identifier)
            import pdb
            pdb.set_trace()