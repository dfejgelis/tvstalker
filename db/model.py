# -*- coding: utf-8 -*-
from __future__ import with_statement

from google.appengine.ext import db
from google.appengine.api import files
from google.appengine.api import urlfetch


class InvalidUserException(Exception):
    """The user session wasn't able to be created."""


class StalkerLogin(db.Model):
    access_token_key = db.StringProperty()
    access_token_secret = db.StringProperty()
    username = db.StringProperty()
    login_type = db.StringProperty()

    def __init__(self, *args, **kw):
        super(StalkerLogin, self).__init__(*args, **kw)
        self.login_type = kw.get('login_type', None)
        if self.login_type is None:
            raise InvalidUserException(InvalidUserException.__doc__)

    def nickname(self):
        return self.username


class Serie(db.Model):
    name = db.StringProperty()
    title = db.StringProperty()
    description = db.StringProperty(multiline=True)
    image_name = db.StringProperty(default='')
    last_season = db.IntegerProperty()
    source_url = db.StringProperty()

    def store_image(self, link):
        file_name = files.blobstore.create(
            mime_type='application/octet-stream')
        with files.open(file_name, 'a') as f:
            f.write(urlfetch.Fetch(link, deadline=60).content)
        files.finalize(file_name)
        self.image_name = file_name


class Season(db.Model):
    nro = db.IntegerProperty()
    serie = db.ReferenceProperty(Serie)


class Episode(db.Model):
    title = db.StringProperty()
    description = db.TextProperty()
    airdate = db.DateProperty()
    season = db.ReferenceProperty(Season)
    nro = db.IntegerProperty()


class ValidateUser(db.Model):
    username = db.StringProperty()
    email = db.EmailProperty()
    password = db.StringProperty()
    validate_code = db.StringProperty()


class User(db.Model):
    name = db.StringProperty()
    lastname = db.StringProperty()
    email = db.EmailProperty()
    avatar = db.StringProperty()
    login = db.ReferenceProperty(StalkerLogin)


class FollowingShows(db.Model):
    login = db.ReferenceProperty(StalkerLogin)
    serie = db.ReferenceProperty(Serie)


class PublishedImages(db.Model):
    image_name = db.StringProperty()
    url = db.StringProperty()