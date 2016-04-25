import webapp2
from google.appengine.api import urlfetch

from google.appengine.api.datastore_types import BlobKey
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from backend.files.File import File
from backend.projects.Project import Project


class UploadLinkHandler(webapp2.RequestHandler):
    def post(self):
        upload_url = blobstore.create_upload_url('/files_upload') + '?projectId=' + str(self.request.get('projectId'))
        self.response.write(urlfetch.fetch(url=upload_url, payload=self.request.body, method=urlfetch.POST))


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        my_file = File()
        my_file.project = Project.get_by_id(int(str(self.request.get("projectId")))).key
        my_file.blobKey = upload.key()
        my_file.put()
        self.response.write(my_file.blobKey)


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        if not blobstore.get(self.request.get('blob_key')):
            self.error(404)
        else:
            self.send_blob(self.request.get('blob_key'))


app = webapp2.WSGIApplication([('/api/files', UploadLinkHandler),
                               ('/api/files_upload', UploadHandler),
                               ('/api/file_download', DownloadHandler)],
                              debug=True)
