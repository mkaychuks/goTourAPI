from flask_restx import fields


# register user resource
register_resource = {
    'username': fields.String(default='JohnDoe'),
    'email': fields.String(default='admin@admin.com'),
    'password': fields.String
}

blog_post = {
    'id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
    'date_created': fields.String
}

bookings = {
    'id' : fields.Integer,
    "type_of_travel" : fields.String,
    "time_of_year" : fields.String,
    "ticket" : fields.String,
    "location_of_choice": fields.String,
    "booked_by" : fields.String
}