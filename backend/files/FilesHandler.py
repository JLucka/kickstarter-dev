import webapp2
from google.appengine.api import urlfetch

from google.appengine.api.datastore_types import BlobKey
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from backend.files.File import File
from backend.projects.Project import Project


class UploadLinkHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/api/files_upload', gs_bucket_name='kickstarter-dev.appspot.com')
        self.response.write(upload_url)


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        print 'wchodze do upload handler'
        project_id = Project.get_by_id(int(str(self.request.get("projectId")))).key
        answer = []
        for i in range(0, len(self.get_uploads())):
            print 'wchodze do petli'
            upload = self.get_uploads()[i]
            my_file = File()
            my_file.project = project_id
            my_file.blobKey = upload.key()
            my_file.put()
            answer.append(str(my_file.blobKey))
        print 'wychodze z petli'
        self.response.write(answer)


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        if not blobstore.get(self.request.get('blob_key')):
            self.error(404)
        else:
            self.send_blob(self.request.get('blob_key'))


app = webapp2.WSGIApplication([
    webapp2.Route('/api/files', handler=UploadLinkHandler),
    webapp2.Route('/api/files_upload', handler=UploadHandler, name='upload'),
    webapp2.Route('/api/file_download', handler=DownloadHandler),
    ], debug=True)