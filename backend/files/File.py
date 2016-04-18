from google.appengine.ext import ndb


class File(ndb.Model):
    project = ndb.KeyProperty(kind='Project')
    full_size_image = ndb.BlobProperty()
