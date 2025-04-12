from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional


class AddPetForm(FlaskForm):
    """Form for adding a new pet to the system.

    This form includes fields for the pet's name, species, photo URL, age, and additional notes.
    Validation ensures required fields are filled out and input is within acceptable ranges.
    """

    name = StringField(
        "Pet Name",
        validators=[InputRequired()],
    )  # Name is required for adding a pet.

    species = SelectField(
        "Species",
        choices=[("", "--- Select from list ---"), ("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine")],
        validators=[InputRequired()]
    ) # Dropdown for selecting the species of the pet, required field.

    photo_url = StringField(
        "Photo URL",
        validators=[Optional(), URL()],
    ) # Optional field for providing a photo URL. If provided, must be a valid URL.


    age = IntegerField(
        "Age",
        validators=[Optional(), NumberRange(min=0, max=30)],
    ) # Optional field for the pet's age, restricted to numbers between 0 and 30.

    notes = TextAreaField(
        "Comments",
        validators=[Optional(), Length(min=10)],
    ) # Optional field for notes/comments, minimum length of 10 characters.


class EditPetForm(FlaskForm):
    """Form for editing an existing pet's details.

    This form allows updates to a pet's name, species, age, photo, and availability status.
    It also includes a section for notes and uses validators to ensure proper input.
    """

    name = StringField("Pet Name", validators=[InputRequired()]) # Name is required for editing.

    species = SelectField('Species', choices=[('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')])
    # Dropdown for selecting the species of the pet.
    
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0)])
     # Optional field for the pet's age, minimum value of 0.

    notes = TextAreaField("Notes", validators=[Optional(), Length(min=10)])
    # Optional field for notes/comments, minimum length of 10 characters.

    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    # Optional field for updating the pet's photo URL. Valid URL is required.

    available = BooleanField("Available? Click for YES!")
    # Checkbox for setting pet availability. Checked means available.