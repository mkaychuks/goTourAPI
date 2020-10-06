from datetime import timedelta
from flask.templating import render_template

from sqlalchemy.exc import IntegrityError

from flask import session, abort, request
from flask_restx import reqparse, Resource, marshal_with
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token
from flask_mail import Message
from werkzeug.exceptions import InternalServerError

from src import db, bcrypt, mail

from src.models import Users, Newsletter
from src.schema import (
    register_resource
)
from src.mail_service import send_mail


register_args = reqparse.RequestParser()
register_args.add_argument('username', type=str, required=True, help='Username here')
register_args.add_argument('email', type=str, required=True, help='Email here')
register_args.add_argument('password', type=str, required=True, help='Password here')

# init a registration route
class Register(Resource):

    @marshal_with(register_resource)
    def post(self):

        try:
            args = register_args.parse_args()
            
            # init a password hashing
            hashed_password = bcrypt.generate_password_hash(args['password']).decode('utf-8')

            new_user = Users(
                username = args['username'],
                email = args['email'],
                password = hashed_password
            )

            db.session.add(new_user)
            db.session.commit()

            return new_user
        except IntegrityError:
            abort(400, 'User already exists')



login_args = reqparse.RequestParser()
login_args.add_argument('email', type=str, required=True, help='Email here')
login_args.add_argument('password', type=str, required=True, help='Password here')


# init login view
class Login(Resource):

    def post(self):
        
        args = login_args.parse_args()
        existing_user = Users.query.filter_by(email=args['email']).first()

        if existing_user and bcrypt.check_password_hash(existing_user.password, args['password']):
            expiry = timedelta(days=5)
            access_token = create_access_token(
                identity=str(existing_user.username), expires_delta=expiry, fresh=True
            )

            return {
                'message': f'Logged in as {existing_user.username}',
                'jwt_credentials':[
                    {
                        'access_token': access_token,
                    }
                ]
            }, 200
        
        abort(401, 'Invalid credentials, check username or password')


# init logout route
class Logout(Resource):

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()

        if current_user in session:
            session.pop(current_user, None)
        return {'status':200,
                'message':
                    'Successfully Logged out'
            }



# init the ContactForm
contact_args = reqparse.RequestParser()
contact_args.add_argument('subject', type=str, required=True, help='Your name here')
contact_args.add_argument('email', type=str, required=True, help='Your mail address')
contact_args.add_argument('message', type=str, required=True, help='Your message here')

class Contact(Resource):

    def post(self):
        args = contact_args.parse_args()

        msg = Message(subject=args['subject'], sender=args['email'], recipients=[])
        msg.body = args['message']

        mail.send(msg)

        return {'message': 'Success'}


# forgot password
forgot_password = reqparse.RequestParser()
forgot_password.add_argument('email', type=str, required=True, help='email required')

class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'

        try:
            args = forgot_password.parse_args()
            user = Users.query.filter_by(email=args['email']).first()
            if not user:
                abort(401, 'Email doesn\'t exists')
            expires = timedelta(hours=24)
            reset_token = create_access_token(str(user.username), expires_delta=expires)

            send_mail(
                'Reset Your Password', sender='support@reply.com',
                recipients=[user.email],
                text_body=render_template('reset_password.txt', url=url + reset_token),
                html_body=render_template('reset_password.html', url=url + reset_token)
            )

            return {'message': 'Check your email for suggestions'}
        
        except InternalServerError:
            abort(500, 'Internal Server Error')


# reset password
reset_password = reqparse.RequestParser()
reset_password.add_argument('reset_token', type=str, required=True, help='{reset token required}')
reset_password.add_argument('password', type=str, required=True, help='{new password required}')

class ResetPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        try:
            args = reset_password.parse_args()
            user_username = decode_token(args['reset_token'])['identity']

            user = Users.query.filter_by(username=user_username).first()
            hash_password = bcrypt.generate_password_hash(args['password']).decode('utf-8')

            user.password = hash_password
            db.session.commit()

            send_mail(
                'Password Successful',
                sender='support@mail.com',
                recipients=[user.email],
                text_body='Password reset was successful',
                html_body='<p>Password reset was successful </p>'
            )
            return {'message': "You can now log in with your new password"}, 200

        except InternalServerError:
            abort(500, 'Internal Server Error')


# creating the subscribing to the newsletter args
newsletter_args = reqparse.RequestParser()
newsletter_args.add_argument('name', type=str, help='{Your name}', required=True)
newsletter_args.add_argument('email', type=str, help='{Your email address}', required=True)


class Subscribe(Resource):
    
    def post(self):
        args = newsletter_args.parse_args()
        email = Newsletter.query.filter_by(email=args['email']).first()

        try:

            if email:
                abort(401, "This email is not available")

            subscriber = Newsletter(
                name=args['name'],
                email=args['email']
            )

            db.session.add(subscriber)
            db.session.commit()

            return {'message': 'You have successfully subscribed to our newsletter'}
        except InternalServerError:
            abort(500, 'Something went wrong internally')
