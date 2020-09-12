from flask_restx import reqparse, Resource, marshal_with

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