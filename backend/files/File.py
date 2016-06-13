from google.appengine.ext import ndb


class File(ndb.Model):
    project = ndb.KeyProperty(kind='Project')
    blobKey = ndb.BlobKeyProperty(required=True)
    file_path = ndb.TextProperty(indexed=True)
    content_type = ndb.StringProperty()
    file_name = ndb.StringProperty()

    def to_json(self):
        obj = {
            'url': 'https://kickstarter-dev.appspot.com/api/file_download?blob_key=' + str(self.blobKey),
            'content_type': str(self.content_type),
            'file_name': str(self.file_name)
        }
        return obj


def attach_to_project(files, project):
    for blob_key in files:
        my_file = File.query(File.file_path == str(blob_key)).get()
        my_file.project = project
        my_file.put()


def clear_files(project):
    files = File.query(File.project == project).fetch()
    for my_file in files:
        my_file.project = None
        my_file.put()

