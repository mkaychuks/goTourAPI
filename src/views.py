from datetime import timedelta

from flask_restx import reqparse, Resource, marshal_with
from flask_jwt_extended import create_access_token, create_refresh_token

from src import db, bcrypt

from src.models import Users
from src.schema import (
    register_resource
)


register_args = reqparse.RequestParser()
register_args.add_argument('username', type=str, required=True, help='Username here')
register_args.add_argument('email', type=str, required=True, help='Email here')
register_args.add_argument('password', type=str, required=True, help='Password here')

# init a registration route
class Register(Resource):

    @marshal_with(register_resource)
    def post(self):
        args = register_args.parse_args()\
        
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
            refresh_token = create_refresh_token(
                identity=str(existing_user.username)
            )

            return {
                'message': f'Logged in as {existing_user.username}',
                'jwt_credentials':[
                    {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                    }
                ]
            }, 200
        
        return {'message': 'Invalid credentials, check username or password'}
