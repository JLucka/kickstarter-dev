import unittest
import datetime

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from backend.files.File import File
from backend.projects.Project import Project
from backend.users.User import User


class TestFile(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

        User(name="FancyName", google_id="123id", key=ndb.Key(pairs=[(User, 1)])).put()
        Project(name="name123", creator=ndb.Key(pairs=[(User, 1)]), createdOn=datetime.datetime(2016, 4, 25),
                key=ndb.Key(pairs=[(Project, 1)])).put()
        File(project=ndb.Key(pairs=[(Project, 1)]), blobKey=ndb.BlobKey("someGreatKey")).put()
        self.project = Project.query(Project.key == ndb.Key(pairs=[(Project, 1)])).fetch()[0]
        self.file = File.query(File.key == ndb.Key(pairs=[(File, 1)])).fetch()[0]

    def test_create(self):
        self.assertEqual(self.project.key, self.file.project)
        self.assertEqual("someGreatKey", self.file.blobKey)

    def tearDown(self):
        self.testbed.deactivate()
