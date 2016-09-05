# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment( loader = jinja2.FileSystemLoader(template_dir))



class Success(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('success.html')
        self.response.write(template.render())

class MainPage(webapp2.RequestHandler):


    def validateUsername(self,username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    def validatePasswords(self,password,verify):

        USER_RE = re.compile(r"^.{3,20}$")
        if USER_RE.match(password):
            if password == verify:
                return True
        return False

    def validateEmail(self,email):

        USER_RE = re.compile(r"[\S]+@[\S]+.[\S]+$")
        return USER_RE.match(email)

    def get(self):
        template = jinja_env.get_template('frontend.html')
        self.response.write(template.render())
    def post(self):

        username =  self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        errorMessages = {}

        errorFound = False

        if not self.validateUsername(username):
            errorMessages['usernameerror'] = "Invalid Username"
            errorFound = True
        if not self.validatePasswords(password,verify):
            errorMessages['passworderror'] = "Invalid Passwords"
            errorFound = True
        if email and not self.validateEmail(email):
            errorMessages['emailerror'] = "Invalid email"
            errorFound = True

        if errorFound:
            template = jinja_env.get_template('frontend.html')
            self.response.write(template.render(**errorMessages))
        else:
            self.redirect('/success')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/success',Success)
], debug=True)
