from app import create_app, db
from app.models import User, Pet, PetService

def seed_data():
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to preserve data)
        # Pet.query.delete()
        # PetService.query.delete()
        # User.query.filter_by(role='admin').delete()
        
        # Create admin user
        admin_user = User.query.filter_by(email='admin@petplatform.com').first()
        if not admin_user:
            admin_user = User(
                name='Admin',
                email='admin@petplatform.com',
                role='admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("Created admin user")
        else:
            print("Admin user already exists")
        
        # Create sample pets
        pets_data = [
            {
                'name': 'Max',
                'species': 'dog',
                'breed': 'Golden Retriever',
                'age': 3,
                'health_status': 'Healthy, vaccinated',
                'description': 'Max is a friendly and energetic Golden Retriever who loves to play fetch and go for long walks. He gets along well with children and other pets.',
                'image_url': 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=400'
            },
            {
                'name': 'Bella',
                'species': 'dog',
                'breed': 'Labrador',
                'age': 2,
                'health_status': 'Healthy, spayed',
                'description': 'Bella is a sweet and gentle Labrador who enjoys cuddling and playing in the yard. She is house-trained and knows basic commands.',
                'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400'
            },
            {
                'name': 'Luna',
                'species': 'cat',
                'breed': 'Persian',
                'age': 4,
                'health_status': 'Healthy, vaccinated',
                'description': 'Luna is a beautiful Persian cat with a calm and affectionate personality. She enjoys quiet environments and loves being brushed.',
                'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400'
            },
            {
                'name': 'Oliver',
                'species': 'cat',
                'breed': 'Siamese',
                'age': 1,
                'health_status': 'Healthy, neutered',
                'description': 'Oliver is a playful and curious Siamese kitten who loves to explore and play with toys. He is very social and enjoys human company.',
                'image_url': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400'
            },
            {
                'name': 'Charlie',
                'species': 'bird',
                'breed': 'Cockatiel',
                'age': 2,
                'health_status': 'Healthy',
                'description': 'Charlie is a cheerful Cockatiel who loves to whistle and interact with people. He enjoys flying around the room and eating seeds.',
                'image_url': 'https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=400'
            },
            {
                'name': 'Snowball',
                'species': 'other',
                'breed': 'Rabbit',
                'age': 1,
                'health_status': 'Healthy',
                'description': 'Snowball is a adorable white rabbit who loves eating fresh vegetables and hopping around. She is gentle and enjoys being petted.',
                'image_url': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400'
            }
        ]
        
        for pet_data in pets_data:
            existing_pet = Pet.query.filter_by(name=pet_data['name']).first()
            if not existing_pet:
                pet = Pet(**pet_data)
                db.session.add(pet)
                print(f"Created pet: {pet_data['name']}")
            else:
                print(f"Pet {pet_data['name']} already exists")
        
        # Create sample services
        services_data = [
            {
                'name': 'Happy Paws Veterinary Clinic',
                'service_type': 'vet',
                'description': 'Full-service veterinary clinic offering routine check-ups, vaccinations, surgeries, and emergency care. Experienced veterinarians with love for animals.',
                'contact': '+1 (555) 123-4567',
                'location': '123 Main St, Cityville, ST 12345'
            },
            {
                'name': 'Pampered Pets Grooming Salon',
                'service_type': 'grooming',
                'description': 'Professional pet grooming services including bathing, haircuts, nail trimming, and teeth cleaning. We use only pet-safe products and provide a stress-free environment.',
                'contact': '+1 (555) 987-6543',
                'location': '456 Oak Ave, Townsville, ST 67890'
            },
            {
                'name': 'Top Dog Training Academy',
                'service_type': 'training',
                'description': 'Specialized dog training programs including basic obedience, advanced commands, agility training, and behavioral modification. Certified trainers with positive reinforcement methods.',
                'contact': '+1 (555) 246-8135',
                'location': '789 Pine Rd, Villagetown, ST 13579'
            }
        ]
        
        for service_data in services_data:
            existing_service = PetService.query.filter_by(name=service_data['name']).first()
            if not existing_service:
                service = PetService(**service_data)
                db.session.add(service)
                print(f"Created service: {service_data['name']}")
            else:
                print(f"Service {service_data['name']} already exists")
        
        # Commit all changes
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
