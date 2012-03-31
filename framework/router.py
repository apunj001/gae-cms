"""
GAE-Python-CMS: Python-based CMS designed for Google AppEngine
Copyright (C) 2012  Imran Somji

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from framework import section
import settings

class Router(webapp.RequestHandler):
    def get(self, path):
        path = path.strip('/').lower()
        if path == section.HOME_SECTION:
            self.error(404) # Only want to access DEFAULT_SECTION through the root
            return False
        elif not path:
            path = section.HOME_SECTION
        try:
            self.response.out.write(section.get_section(self, self.path_parts(path)))
        except IndexError:
            try:
                section.get_section(self, [section.HOME_SECTION])
                self.error(404)
            except IndexError:
                self.response.out.write(section.create_section(path=section.HOME_SECTION, parent_path=None, title='GAE-Python-CMS'))
        except AttributeError:
            self.error(404)
        except:
            self.error(403) # Access Denied
            
    def post(self, path):
        self.get(path)
        
    def path_parts(self, path):
        base_path = path.split('/')[0]
        path = path.lstrip(base_path).strip('/')
        module_path = path.split('/')[0]
        path = path.lstrip(module_path).strip('/')
        action_path = path.split('/')[0]
        path = path.lstrip(action_path).strip('/')
        parameter_path = path.split('/')[0]
        return base_path, module_path, action_path, parameter_path
        

application = webapp.WSGIApplication([('(/.*)', Router)], debug=settings.DEBUG)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()