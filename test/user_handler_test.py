import unittest

import google
import mock
import webapp2
import webtest

import backend.users.UserHandler


def get_user():
    return "gargas.magdalena"


class TestHandlers(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication([('/user', backend.users.UserHandler.UserHandler)])
        self.testapp = webtest.TestApp(app)

    @mock.patch.object(google.appengine.api.users, 'get_current_user', get_user)
    def test_get_user(self):
        response = self.testapp.get('/user')
        self.assertEquals(response.status_int, 200)
        self.assertTrue('"name": "gargas.magdalena"' in response.body)
        self.assertTrue('"money"' in response.body)
        self.assertTrue('"id"' in response.body)