from google.appengine.ext import ndb


class File(ndb.Model):
    project = ndb.KeyProperty(kind='Project')
    blobKey = ndb.BlobKeyProperty(required=True)
    file_path = ndb.TextProperty(indexed=True)