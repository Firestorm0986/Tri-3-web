import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from operator import itemgetter
from model.images import Images

image_api = Blueprint('image_api', __name__,
                   url_prefix='/api/images')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(image_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            likes = body.get('likes')
            dob = body.get('dob')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Images(name=name, 
                      uid=uid, likes = likes)
            
            ''' Additional garbage error checking '''
            # set password if provided
            # convert to date type
            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            image = uo.create()
            # success returns json of user
            if image:
                return jsonify(image.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        def get(self):
            images = Images.query.all()
            json_ready = [image.read() for image in images]

            # Sort the images based on the number of likes using merge sort
            sorted_images = self.merge_sort(json_ready, key=itemgetter('likes'))

            return jsonify(sorted_images)

        def merge_sort(self, arr, key):
            if len(arr) <= 1:
                return arr

            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            left_half = self.merge_sort(left_half, key=key)
            right_half = self.merge_sort(right_half, key=key)

            return self.merge(left_half, right_half, key=key)

        def merge(self, left, right, key):
            merged = []
            left_index = 0
            right_index = 0

            while left_index < len(left) and right_index < len(right):
                if key(left[left_index]) < key(right[right_index]):
                    merged.append(left[left_index])
                    left_index += 1
                else:
                    merged.append(right[right_index])
                    right_index += 1

            merged.extend(left[left_index:])
            merged.extend(right[right_index:])

            return merged

    
 

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')