from src import api

from src.views import (
    Register, Login, Contact, Logout
)


api.add_resource(Register, '/register/', endpoint='register')
api.add_resource(Login, '/auth/login/', endpoint='login')
api.add_resource(Logout, '/auth/logout/', endpoint='logout')
api.add_resource(Contact, '/contact/', endpoint='contact')