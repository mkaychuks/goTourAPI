from src import api

from src.views import (
    Register
)


api.add_resource(Register, '/register/', endpoint='register')