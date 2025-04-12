from flask import Flask, url_for, render_template, redirect, flash

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.app_context().push()  # Ensures the app context is available (important outside app factories)

# Configuration settings

app.config['SECRET_KEY'] = "ihaveasecret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Allows flash messages to appear after redirects

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:

# Initialize the debug toolbar
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


##############################################################################
# Route Definitions
##############################################################################


@app.route("/")
def list_pets():
    """Display a list of all pets currently in the adoption system. Divided by availability"""

    # pets = Pet.query.all()
    # return render_template("pet_list.html", pets=pets) ---> UPDATED BELOW to split homepage by available pets vs unavailable pets!

    available_pets = Pet.query.filter_by(available=True).all()
    unavailable_pets = Pet.query.filter_by(available=False).all()
    return render_template("pet_list.html", available_pets=available_pets, unavailable_pets=unavailable_pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """
    Handle displaying and processing the 'Add a Pet' form.

    - On GET: render the form to add a new pet.
    - On POST: validate form, add pet to DB, then redirect with flash message.
    """


    form = AddPetForm()

    if form.validate_on_submit():
        # Refactored code using form.data
        # Use dictionary comprehension to avoid CSRF token
        data = {k: v for k, v in form.data.items() if k != "csrf_token"} # Remove csrf_token from form data

        new_pet = Pet(**data) # Unpack the form data directly into the Pet model
        # new_pet = Pet(name=form.name.data, age=form.age.data, ...)

        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added.")
        return redirect(url_for('list_pets'))

    else:
        # On failed validation or GET request bring user to add pet form
        return render_template("pet_add_form.html", form=form)


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """
    Handle editing an existing pet's information.

    - On GET: pre-populate the form with current pet data.
    - On POST: update pet info if form is valid, flash confirmation.
    """

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        # Update pet attributes from form data

        pet.name = form.name.data
        pet.species = form.species.data
        pet.age = form.age.data
        pet.notes = form.notes.data
        pet.photo_url = form.photo_url.data
        pet.available = form.available.data

        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('list_pets'))

    else:
        # if failed return user to pet edit form page
        return render_template("pet_edit_form.html", form=form, pet=pet)


@app.route("/<int:pet_id>/delete", methods=["POST"])
def delete_pet(pet_id):
    """
    Handle deleting a pet from the database.

    - Only accepts POST requests to prevent accidental deletions.
    - Redirects to home page with flash message.
    """   

    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash(f"{pet.name} has been deleted.")
    return redirect(url_for('list_pets'))

@app.route("/pets/<int:pet_id>")
def show_pet(pet_id):
    """
    Display a full profile page for a single pet.

    Includes photo, species, age, notes, and adoption status.
    """

    pet = Pet.query.get_or_404(pet_id)
    return render_template("pet_profile.html", pet=pet)



# @app.route("/api/pets/<int:pet_id>", methods=['GET'])
# def api_get_pet(pet_id):
   # """
    #API route: Return JSON with basic info about a single pet.

    #This can be used for AJAX requests or external API consumers.
    #"""

   # pet = Pet.query.get_or_404(pet_id)
   # info = {"name": pet.name, "age": pet.age}

   # return jsonify(info)