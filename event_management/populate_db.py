"""
Populate database with fake data for Event Management System
Run this script from the project root: python populate_db.py
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

# Import models after Django setup
from events.models import Category, Event, Participant
from faker import Faker

# Initialize Faker
fake = Faker()


def clear_existing_data():
    """Clear existing data to allow multiple runs"""
    print("Clearing existing data...")
    Participant.objects.all().delete()
    Event.objects.all().delete()
    Category.objects.all().delete()
    print("✓ Existing data cleared\n")


def create_categories():
    """Create fake categories"""
    print("Creating categories...")
    
    category_names = [
        "Technology Conference",
        "Music Festival",
        "Sports Event",
        "Educational Workshop",
        "Business Networking"
    ]
    
    categories = []
    for name in category_names:
        category = Category.objects.create(
            name=name,
            description=fake.paragraph(nb_sentences=3)
        )
        categories.append(category)
        print(f"  ✓ Created: {category.name}")
    
    print(f"✓ {len(categories)} categories created\n")
    return categories


def create_events(categories):
    """Create fake events"""
    print("Creating events...")
    
    events = []
    for i in range(20):
        # Generate random date (mix of past, present, and future)
        days_offset = random.randint(-30, 60)  # 30 days ago to 60 days ahead
        event_date = datetime.now().date() + timedelta(days=days_offset)
        
        # Generate random time
        event_time = fake.time_object()
        
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.paragraph(nb_sentences=5),
            date=event_date,
            time=event_time,
            location=fake.city() + ", " + fake.country(),
            category=random.choice(categories)
        )
        events.append(event)
        print(f"  ✓ Created: {event.name} on {event.date}")
    
    print(f"✓ {len(events)} events created\n")
    return events


def create_participants(events):
    """Create fake participants and assign them to random events"""
    print("Creating participants...")
    
    participants = []
    for i in range(50):
        # Generate unique email
        email = fake.unique.email()
        
        participant = Participant.objects.create(
            name=fake.name(),
            email=email
        )
        
        # Assign participant to 1-5 random events
        num_events = random.randint(1, 5)
        selected_events = random.sample(events, num_events)
        participant.events.set(selected_events)
        
        participants.append(participant)
        print(f"  ✓ Created: {participant.name} ({participant.email}) - Registered for {num_events} events")
    
    print(f"✓ {len(participants)} participants created\n")
    return participants


def print_summary(categories, events, participants):
    """Print summary of populated data"""
    print("=" * 60)
    print("DATABASE POPULATION SUMMARY")
    print("=" * 60)
    print(f"✓ Categories created: {len(categories)}")
    print(f"✓ Events created: {len(events)}")
    print(f"✓ Participants created: {len(participants)}")
    print()
    
    # Calculate some statistics
    total_registrations = sum(participant.events.count() for participant in participants)
    avg_participants_per_event = total_registrations / len(events) if events else 0
    
    print("STATISTICS:")
    print(f"  - Total event registrations: {total_registrations}")
    print(f"  - Average participants per event: {avg_participants_per_event:.2f}")
    print()
    
    # Show date distribution
    today = datetime.now().date()
    past_events = Event.objects.filter(date__lt=today).count()
    today_events = Event.objects.filter(date=today).count()
    future_events = Event.objects.filter(date__gt=today).count()
    
    print("EVENT DATE DISTRIBUTION:")
    print(f"  - Past events: {past_events}")
    print(f"  - Today's events: {today_events}")
    print(f"  - Upcoming events: {future_events}")
    print()
    
    print("=" * 60)
    print("✓ Database populated successfully!")
    print("=" * 60)


def populate_db():
    """Main function to populate the database"""
    print("\n" + "=" * 60)
    print("POPULATING EVENT MANAGEMENT DATABASE")
    print("=" * 60 + "\n")
    
    try:
        # Clear existing data
        clear_existing_data()
        
        # Create data
        categories = create_categories()
        events = create_events(categories)
        participants = create_participants(events)
        
        # Print summary
        print_summary(categories, events, participants)
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    populate_db()
