""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, String
import base64

''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''


class Images(db.Model):
    __tablename__ = 'images'  # table name is plural, class name is singular

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _likes = db.Column(db.Integer, unique=False, nullable=True)
    _dob = db.Column(db.Date)
    _image = db.Column(db.String(255), unique=False, nullable=True)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, likes, dob=date.today(), image=None):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self.likes = likes
        self._dob = dob
        self._image = image

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image_data):
        self._image = image_data
    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def likes(self):
        return self._likes
    
    # a setter function, allows name to be updated after initial object creation
    @likes.setter
    def likes(self, likes):
        self._likes = likes
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            if self.image is not None:
                self._image = base64.b64encode(self.image.encode()).decode()  # Encode the image data as base64 string
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None


    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "dob": self.dob,
            "likes": self.likes,
            "image": self.image
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", likes=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if likes > 0:
            self.likes = likes
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initImages():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = Images(name='Thomas Edison', uid='toby', likes=1, dob=date(1847, 2, 11), image=None)
        u2 = Images(name='Nicholas Tesla', uid='niko', likes=2, dob=date(1856, 7, 10), image=None)
        u3 = Images(name='Alexander Graham Bell', likes=4, uid='lex', image=None)
        u4 = Images(name='Grace Hopper', uid='hop', likes=3, dob=date(1906, 12, 9), image=None)

        images = [u1, u2, u3, u4]

        """Builds sample user/note(s) data"""
        for image in images:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    image.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {image.uid}")
            