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

from google.appengine.ext import db

from django.utils.html import strip_tags

from framework import content
from framework.subsystems import template
from framework.subsystems.forms import form, control, textareacontrol

class Text(content.Content):

    titles = db.StringListProperty()
    bodies = db.StringListProperty()

    name = 'Text'
    author = 'Imran Somji'

    actions = [
        ['edit', 'Edit', True],
    ]
    views = [
        ['default', 'Default - multiple items are tabbed', True],
    ]

    def action_edit(self, item):
        if self.section.handler.request.get('submit'):
            i = 0
            item.titles = []
            item.bodies = []
            while self.section.handler.request.get('title' + unicode(i)) or self.section.handler.request.get('body' + unicode(i)):
                title = strip_tags(self.section.handler.request.get('title' + unicode(i))).strip()
                body = self.section.handler.request.get('body' + unicode(i)).strip()
                if title or body:
                    item.titles.append(title)
                    item.bodies.append(body)
                i += 1
            item.update()
            raise Exception('Redirect', '/' + (self.section.path if not self.section.is_default else ''))
        ret = '<h2>Edit text</h2>'
        f = form(self.section.full_path)
        for i in range(len(item.titles)):
            f.add_control(control('text', 'title' + unicode(i), item.titles[i], 'Title', 60))
            f.add_control(textareacontrol('body' + unicode(i), item.bodies[i], 'Body', 100, 10))
        f.add_control(control('text', 'title' + unicode(len(item.titles)), '', 'Title', 60))
        f.add_control(textareacontrol('body' + unicode(len(item.bodies)), '', 'Body', 100, 10))
        f.add_control(control('submit', 'submit'))
        ret += unicode(f)
        return ret

    def view_default(self, item, params):
        items = []
        for i in range(len(item.titles)):
            items.append([item.titles[i], item.bodies[i]])
        params = {
                  'section': self.section,
                  'content_type': self.name,
                  'namespace': self.namespace,
                  'items': items,
                  }
        return template.snippet('text-tabs', params)