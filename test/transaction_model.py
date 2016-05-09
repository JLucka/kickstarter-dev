import datetime
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from backend.projects.Project import Project
from backend.transactions.Transaction import Transaction
from backend.users.User import User
from test.textures import TEXT_JSON_OF_TRANSACTION


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

        User(name="FancyName", google_id="123id", key=ndb.Key(pairs=[(User, 1)])).put()
        Project(name="name123", creator=ndb.Key(pairs=[(User, 1)]),
                createdOn=datetime.datetime(2016, 4, 25), key=ndb.Key(pairs=[(Project, 1)])).put()
        Transaction(project=ndb.Key(pairs=[(Project, 1)]), user=ndb.Key(pairs=[(User, 1)]),
                    time_stamp=datetime.datetime(2016, 4, 25),  key=ndb.Key(pairs=[(Transaction, 1)])).put()
        self.transaction = Transaction.query(Transaction.key == ndb.Key(pairs=[(Transaction, 1)])).fetch()[0]

    def test_create(self):
        self.assertEqual(ndb.Key(Project, 1), self.transaction.project)
        self.assertEqual(ndb.Key(User, 1), self.transaction.user)
        self.assertEqual(0, self.transaction.money)
        self.assertEqual(datetime.datetime(2016, 4, 25), self.transaction.time_stamp)

    def test_toJsonObject(self):
        self.assertEqual(TEXT_JSON_OF_TRANSACTION, self.transaction.to_json_obj())

    def tearDown(self):
        self.testbed.deactivate()
