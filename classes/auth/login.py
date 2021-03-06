# This file will authenticate the user upon login.
import re
import os
from flask import request, jsonify, make_response
from app.models import Users
from flask.views import MethodView
import jwt
import datetime
from app.models import BlacklistToken
from classes.auth.auth import token_required
from passlib.apps import custom_app_context as password_context

class UserLoginAuthentication(MethodView):
    """This class will handle the access of resources by user through login.
    """
    @classmethod
    def post(self):
        # User login using post method
        """
        User login
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: user details
            description: User's email and password
            type: string
            required: true
            schema:
              id: login
              properties:
                email:
                  default: jimmy@gmail.com
                password:
                  default: pass1234
        responses:
          200:
            description: Login Successful
          400:
            description: Invalid email, token
          404:
            description: User not registered!
          412:
            description: The password is too short
          422:
            description: Please fill all the fields
        """
        email_pattern = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        user_email = str(request.data.get('email', '')).strip().lower()
        user_password = str(request.data.get('password', ''))
        user_details = Users.query.filter_by(email=user_email).first()

        if not user_email and not user_password:
            return make_response(jsonify({'message': 'Please fill all the fields'})), 400

        if not re.search(email_pattern, user_email):
            return make_response(jsonify({'message': 'Invalid email given'})), 400

        if len(user_password) < 7:
            return make_response(jsonify({'message': 'The password is too short'})), 412

        if not user_details:
            return make_response(jsonify({'message': 'User not registered!'})), 404

        if not password_context.verify(user_password, user_details.password):
            return make_response(jsonify({'message': 'Wrong email or password.'})), 400

        access_token = jwt.encode({'id': user_details.id, 'expiry_time': str(datetime.datetime.utcnow() +
                                                                     datetime.timedelta(minutes=30))},
                                  os.getenv('SECRET', '$#%^%$^%@@@@@56634@@@'))

        if access_token:
            return make_response(jsonify({'access_token': access_token.decode(),
                                          'message': 'Successful login',
                                          'username': user_details.username,
                                          'email': user_details.email})), 200
        else:

            return make_response(jsonify({'message': 'Invalid access token'})), 400


class UserLogoutAuthentication(MethodView):
    """This will enable user to destroy the session of the current user.
    """
    decorators = [token_required]

    @classmethod
    def post(self, user_in_session):
        """Method to logout the user

         User logout
        ---
        tags:
          - Authentication
        responses:
          200:
            description: User logged out successfully
          400:
            description: Invalid access token
          409:
            description: The user is already logged out!
        """
        access_token = request.headers.get('x-access-token')
        if access_token:
            user_details = Users.query.filter_by(id=user_in_session).first()
            save_tokens = BlacklistToken(token=access_token)
            save_tokens.save()

            return make_response(jsonify({'message': 'User '+str(user_details.username) +
                                                     ' logged out successfully'})), 200
        return make_response(jsonify({'message': 'Invalid access token'})), 400


# Link the class and operation to a variable.
user_login = UserLoginAuthentication.as_view('user_login')
user_logout = UserLogoutAuthentication.as_view('user_logout')
