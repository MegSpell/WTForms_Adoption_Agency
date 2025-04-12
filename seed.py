from app import db
from models import Pet

def seed_pets():
    """Seed some initial pet data into the database."""

    # List of pets to seed
    pets = [
        Pet(
            name="Woofly", 
            species="dog", 
            photo_url="https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHB1cHB5fGVufDB8fDB8fHww", 
            age=5, 
            notes="House trained. Crate trained. Loves dogs. Not a fan of cats!", 
            available=True
        ),
        Pet(
            name="Porchetta", 
            species="porcupine", 
            photo_url="https://plus.unsplash.com/premium_photo-1664302959064-6c3e5fb92fc6?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8cG9yY3VwaW5lfGVufDB8fDB8fHww", 
            age=2, 
            notes="Prickly as they come!", 
            available=True
        ),
        Pet(
            name="Snargle", 
            species="cat", 
            photo_url="https://images.unsplash.com/photo-1543852786-1cf6624b9987?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjZ8fGNhdHxlbnwwfHwwfHx8MA%3D%3D", 
            age=7, 
            notes="Snagglest snaggle tooth you've ever seen!", 
            available=True
        ),
        Pet(
            name="Barkly", 
            species="dog", 
            photo_url="https://mylostpetalert.com/wp-content/themes/mlpa-child/images/nophoto.gif",  # generic photo
            age=9, 
            notes="Don't worry he's not a barker! Just a Barkly!", 
            available=False
        ),
    ]

    # Add each pet to the session
    for pet in pets:
    #    db.session.add(pet)
        existing_pet = Pet.query.filter_by(name=pet.name).first()
        if not existing_pet:
            db.session.add(pet)
            print(f"Added {pet.name}")
        else:
            print(f"{pet.name} already exists, skipping.")


    # Commit to save the changes
    db.session.commit()
    print("Pets have been seeded!")

if __name__ == "__main__":
    # Run the seed function
    seed_pets()