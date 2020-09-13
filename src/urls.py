from src import api

from src.views import (
    Register, Login
)


api.add_resource(Register, '/register/', endpoint='register')
api.add_resource(Login, '/auth/login/', endpoint='login')