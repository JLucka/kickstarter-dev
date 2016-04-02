import logging
import os
import cloudstorage as gcs
import webapp2

from google.appengine.api import app_identity

my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)
BUCKET_NAME = app_identity.get_default_gcs_bucket_name()


class FilesHandler(webapp2.RequestHandler):
    def get(self):
            bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())

            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Demo GCS Application running from Version: '
                        + os.environ['CURRENT_VERSION_ID'] + '\n')
            self.response.write('Using bucket name: ' + bucket_name + '\n\n')
            bucket = '/' + bucket_name
            filename = bucket + '/demo-testfile'
            self.tmp_filenames_to_clean_up = []


app = webapp2.WSGIApplication([('/files', FilesHandler)], debug=True)