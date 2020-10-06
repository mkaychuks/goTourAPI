import enum

from src import db


# User model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    bookings = db.relationship("Booking", backref='booking', lazy=True)

    def __repr__(self):
        return f'{self.username}'



# creating an Enum class function so as to have a strict choice option
# the booking of rooms for learning purposes

class TravelTypeEnum(enum.Enum):
    holidays = 'holidays'
    family_vacation = 'family_vacation'
    adventure = 'adventure'

class SeasonEnum(enum.Enum):
    winter = 'winter'
    summer = 'summer'

class TicketType(enum.Enum):
    economy = 'economy'
    first_class = 'first_class'

class LocationEnum(enum.Enum):
    santorini = 'santorini'
    cape_verde = 'cape_verde'
    seychelles = 'seychelles'
    ghana = 'ghana'
    obudu_cattle_ranch = 'obudu_cattle_ranch'
    mexico = 'mexico'



# Booking model
class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_of_travel = db.Column(db.Enum(TravelTypeEnum), nullable=False)
    time_of_year = db.Column(db.Enum(SeasonEnum), nullable=False)
    ticket = db.Column(db.Enum(TicketType), nullable=False)
    location_of_choice = db.Column(db.Enum(LocationEnum), nullable=False)
    booked_by = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    
    def __repr__(self) -> str:
        return f'{self.booked_by} booked a tour {self.time_of_year} tour'