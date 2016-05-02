import webapp2

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from backend.files.File import File
from backend.projects.Project import Project


class UploadLinkHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/api/files_upload')
        self.response.out.write(upload_url)


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        project_id = Project.get_by_id(int(str(self.request.get("projectId")))).key
        answer = []
        # for i in range(0, len(self.get_uploads())):
        #     upload = self.get_uploads()[i]
        #     my_file = File()
        #     my_file.project = project_id
        #     my_file.blobKey = upload.key()
        #     my_file.put()
        #     answer.append(str(my_file.blobKey))
        self.response.write(answer)


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