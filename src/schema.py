from flask_restx import fields


# register user resource
register_resource = {
    'username': fields.String(default='JohnDoe'),
    'email': fields.String(default='admin@admin.com'),
    'password': fields.String
}