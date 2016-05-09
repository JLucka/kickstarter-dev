import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from backend.users.User import User
from test.textures import TEXT_JSON_OF_USER


class TestUser(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

        User(name="FancyName", google_id="123id").put()
        self.user = User.query(User.name == u'FancyName').fetch()[0]

    def test_create(self):
        self.assertEqual("FancyName", self.user.name)
        self.assertEqual(15, self.user.money)
        self.assertEqual("123id", self.user.google_id)
        self.assertEqual(False, self.user.admin)

    def test_toJsonObject(self):
        self.assertEqual(TEXT_JSON_OF_USER, self.user.to_json_obj())

    def test_subtractMoney(self):
        self.user.substract_money(5)
        self.assertEqual(10, self.user.money)

    def test_addMoney(self):
        self.user.add_money(5)
        self.assertEqual(20, self.user.money)

    def test_setMoney(self):
        self.user.set_money(5)
        self.assertEqual(5, self.user.money)

    def test_makeAdmin(self):
        self.user.make_admin()
        self.assertEqual(True, self.user.admin)

    def tearDown(self):
        self.testbed.deactivate()
