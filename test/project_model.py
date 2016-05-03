import datetime
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from backend.projects.Project import Project, Status
from backend.users.User import User
from test.textures import TEXT_JSON_OF_PROJECT


class TestProject(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

        Project(description="desc").put()
        User(key=ndb.Key(pairs=[(User, 1)])).put()
        Project(name="name123", creator=ndb.Key(pairs=[(User, 1)]), createdOn=datetime.datetime(2016, 4, 25)).put()
        self.project = Project.query(Project.name == u'name123').fetch()[0]

    def test_create(self):
        self.assertEqual("name123", self.project.name)
        self.assertEqual(None, self.project.description)
        self.assertEqual(0, self.project.money)
        self.assertEqual(ndb.Key(pairs=[(User, 1)]), self.project.creator)
        self.assertEqual(Status.ACTIVE, self.project.status)

    def test_jsonToObject(self):
        self.assertEqual(TEXT_JSON_OF_PROJECT, self.project.to_json_object())
        self.assertEqual(self.project.check_if_accepted(), None)

    def test_hide(self):
        self.project.hide()
        self.assertEqual(self.project.status,  Status.HIDDEN)

    def test_getUrl(self):
        self.assertEqual(self.project.get_url(), "https://kickstarter-dev.appspot.com/project/name123")

    def tearDown(self):
        self.testbed.deactivate()
