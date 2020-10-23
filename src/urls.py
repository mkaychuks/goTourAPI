from src import api

from src.views import (
    Register, Login, Contact, Logout, ForgotPassword, ResetPassword,
    Subscribe, BlogPost, TicketBook
)


api.add_resource(Register, '/register/', endpoint='register')
api.add_resource(Login, '/auth/login/', endpoint='login')
api.add_resource(Logout, '/auth/logout/', endpoint='logout')
api.add_resource(ForgotPassword, '/auth/forgot_password/')
api.add_resource(ResetPassword, '/auth/password_reset/')
api.add_resource(Contact, '/contact/', endpoint='contact')
api.add_resource(Subscribe, '/subscribe/', endpoint='subscribe')
api.add_resource(BlogPost, '/blog/create_new/', endpoint='blog_new')
api.add_resource(TicketBook, '/travel/book/', endpoint='bookings')