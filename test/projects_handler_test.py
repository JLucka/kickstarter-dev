import unittest

import webapp2
import webtest

import backend.projects.ProjectsHandler


class TestHandlers(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication([('/projects', backend.projects.ProjectsHandler.ProjectsHandler)])
        self.testapp = webtest.TestApp(app)

    def test_get_all_projects(self):
        response = self.testapp.get('/projects')
        self.assertEquals(response.status_int, 200)
        self.assertTrue("testName" in response.body)

    def test_get_project(self):
        response = self.testapp.get('/projects?name=testName')
        self.assertEquals(response.status_int, 200)
        self.assertTrue('"money": 0' in response.body)
        self.assertTrue('"creatorid": 1' in response.body)
        self.assertTrue('creatorname": "tomek"' in response.body)
        self.assertTrue('"description": "testDesc"' in response.body)

        self.assertFalse('"creatorid": 2' in response.body)
        self.assertFalse('creatorname": "magda"' in response.body)
        self.assertFalse('"description": "testDesc2"' in response.body)

    # def test_post_project(self):
    #     response = self.testapp.post('/projects?name=testName&desc=description&creatorId=1')
    #     self.assertEquals(response.status_int, 400)
