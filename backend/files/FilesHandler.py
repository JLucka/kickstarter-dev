import webapp2

from backend.files.File import File
from backend.projects.Project import Project


class FilesHandler(webapp2.RequestHandler):
    def get(self):
        my_file = File.get_by_id(int(self.request.get('fileId')))
        if my_file.full_size_image:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(my_file.full_size_image)
        else:
            self.response.out.write('No image')

    def post(self):
        my_file = File()
        my_file.project = Project.get_by_id(int(str(self.request.get("projectId")))).key
        my_file.full_size_image = self.request.get('img')
        my_file.put()
        self.response.write(my_file.key.id())


app = webapp2.WSGIApplication([('/files', FilesHandler)], debug=True)
