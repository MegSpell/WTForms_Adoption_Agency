from flask_sqlalchemy import SQLAlchemy

# Fallback image used when no pet photo is provided
GENERIC_IMAGE = "https://mylostpetalert.com/wp-content/themes/mlpa-child/images/nophoto.gif"

# Initialize SQLAlchemy instance
db = SQLAlchemy()


class Pet(db.Model):
    """
    Model for an adoptable pet.

    Represents a pet in the adoption database, with fields for
    name, species, age, notes, photo, and availability status.
    """

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True) # Unique ID for each pet
    name = db.Column(db.Text, nullable=False) # Pet's name
    species = db.Column(db.Text, nullable=False) # Species (dog, cat, etc.)
    photo_url = db.Column(db.Text) # Optional photo URL
    age = db.Column(db.Integer) # Optional age
    notes = db.Column(db.Text) # Optional notes about the pet
    available = db.Column(db.Boolean, nullable=False, default=True) # Whether the pet is available for adoption (defaults to True)


    def image_url(self):
        """Return the pet's photo URL, or a generic image if none provided."""

        return self.photo_url or GENERIC_IMAGE


def connect_db(app):
    """Connect the SQLAlchemy database to a Flask app instance.

    Should be called in the main application file after app is configured.
    """

    db.app = app
    db.init_app(app)