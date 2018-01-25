# This file will create the user and reset the password.
import datetime
import re
from passlib.apps import custom_app_context as password_context

import jwt
import os
from flask import request, jsonify, make_response, Flask
from app.models import Users
from flask.views import MethodView
from classes.auth.auth import token_required
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

recipients = []


class CreateUser(MethodView):
    """This class will handle the creation of new users
    """
    email_pattern = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    regex_username = "^[a-zA-Z0-9-+\s]{4,20}$"

    @classmethod
    def post(self):
        # create user using post method
        """
        Register user
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: user details
            description: User's email, username and password
            type: string
            required: true
            schema:
              id: register
              properties:
                email:
                  default: jimmy@gmail.com
                username:
                  default: kaguna
                password:
                  default: pass1234
        responses:
          201:
            description: User registered successfully
          409:
            description: User exists!
          400:
            description: Invalid email or username given
          412:
            description: The password is too short
          422:
            description: Please fill all the fields
        """
        user_email = str(request.data.get('email', '')).strip().lower()
        user = Users.query.filter_by(email=user_email).first()
        user_name = str(request.data.get('username', '')).strip()
        user_password = str(request.data.get('password', ''))

        if not user_email and not user_name and not user_password:
            return make_response(jsonify({'message': 'Please fill all the fields'})), 400

        if not re.search(self.email_pattern, user_email):
            return make_response(jsonify({'message': 'Invalid email given'})), 400

        if not re.search(self.regex_username, user_name):
            return make_response(jsonify({'message': 'Invalid username given'})), 400

        if len(user_password) < 7:
            return make_response(jsonify({'message': 'The password is too short'})), 412

        if user:
            return make_response(jsonify({'message': 'User exists!'})), 409
        user_hashed_password = password_context.encrypt(user_password)
        user_creation = Users(email=user_email, username=user_name, password=user_hashed_password)
        user_creation.save()
        return make_response(jsonify({'message': 'User registered successfully'})), 201


class SendResetPasswordToken(MethodView):
    """ This will send an email with the token to reset password."""
    @classmethod
    def post(self):
        # This method will edit the already existing password

        """
        Send token to email
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: user_email
            description: User's email
            type: string
            required: true
            schema:
              id: send_email
              properties:
                email:
                  default: karyorkir@gmail.com
        responses:
          200:
            description: Token sent successfully
          400:
            description: Invalid email given
          404:
            description: User does not exist!
        """
        user_email = str(request.data.get('email', '')).strip().lower()

        user = Users.query.filter_by(email=user_email).first()

        if not user_email:
            return make_response(jsonify({'message': 'Please fill all the fields'})), 412

        if not re.search(CreateUser.email_pattern, user_email):
            return make_response(jsonify({'message': 'Invalid email given'})), 400

        if not user:
            return make_response(jsonify({'message': 'User does not exist!'})), 404

        try:
            access_token = jwt.encode({'id': user.id, 'expiry_time': str(datetime.datetime.utcnow() +
                                                                         datetime.timedelta(minutes=30))},
                                  os.getenv('SECRET', '$#%^%$^%@@@@@56634@@@'))
            subject = "Yummy Recipe Reset Password"
            recipients.append(user_email)
            msg = Message(subject, sender="Admin", recipients=recipients)
            msg.html = "Copy the token between the single quotes below:\n \n<h3>"+str(access_token)+"</h3>"
            with app.app_context():
                mail.send(msg)
            return make_response(jsonify({'message': 'Token sent successfully to '+user_email+''})), 201
        except Exception:
            return make_response(jsonify({'message': 'Invalid request sent.'})), 400


class ResetPassword(MethodView):
    """This class will handle the resetting of password"""
    decorators = [token_required]

    @classmethod
    def put(self, user_in_session):
        # This method will edit the already existing password

        """
        Reset password
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: user details
            description: User's email, password and re-typed password
            type: string
            required: true
            schema:
              id: send_mail
              properties:
                email:
                  default: jimmy@gmail.com
                retyped_password:
                  default: pass1234
                password:
                  default: pass1234
        responses:
          201:
            description: Password resetting is successful
          409:
            description: User exists!
          400:
            description: Invalid email given
          404:
            description: User does not exist!
          412:
            description: The password is too short
          422:
            description: Please fill all the fields
        """
        user_email = str(request.data.get('email', '')).strip().lower()

        user_password = str(request.data.get('password', ''))
        retyped_password = str(request.data.get('retyped_password', ''))
        user = Users.query.filter_by(email=user_email).first()

        if not user_email and not user_password:
            return make_response(jsonify({'message': 'Please fill all the fields'})), 400

        if not re.search(CreateUser.email_pattern, user_email):
            return make_response(jsonify({'message': 'Invalid email given'})), 400

        if len(user_password) < 7 and len(retyped_password) < 7:
            return make_response(jsonify({'message': 'The password is too short'})), 412

        if user_password != retyped_password:
            return make_response(jsonify({'message': 'Password mismatch'})), 400

        if not user:
            return make_response(jsonify({'message': 'User does not exist!'})), 404

        if user.id != user_in_session:
            return make_response(jsonify({'message': 'Unauthorized access!'})), 400
        user_hashed_password = bcrypt.generate_password_hash(user_password, 10)
        user.password = user_hashed_password
        user.save()
        return make_response(jsonify({'message': 'Password resetting is successful'})), 201


# Link the class and operation to a variable.
user_creation = CreateUser.as_view('user_creation')
reset_password = ResetPassword.as_view('reset_password')
reset_password_token = SendResetPasswordToken.as_view('reset_password_token')
