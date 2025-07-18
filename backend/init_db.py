#!/usr/bin/env python3
"""
Database initialization script.
Creates tables and adds sample data for testing.
"""

from app import create_app, db
from app.models import User, Property, ContactMessage
import json

def init_database():
    """Initialize database with tables and sample data."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            db.session.add(admin)
        
        # Check if agent user exists
        agent = User.query.filter_by(username='agent1').first()
        if not agent:
            # Create agent user
            agent = User(
                username='agent1',
                email='agent@example.com',
                password='agent123',
                first_name='John',
                last_name='Agent',
                role='agent'
            )
            db.session.add(agent)
        
        # Check if client user exists
        client = User.query.filter_by(username='client1').first()
        if not client:
            # Create client user
            client = User(
                username='client1',
                email='client@example.com',
                password='client123',
                first_name='Jane',
                last_name='Client',
                role='client'
            )
            db.session.add(client)
        
        # Commit users first
        db.session.commit()
        
        # Add sample properties if none exist
        if Property.query.count() == 0:
            properties = [
                Property(
                    title='Beautiful Family Home',
                    description='A spacious 4-bedroom home perfect for families.',
                    property_type='house',
                    location='Los Angeles, CA',
                    address='123 Main Street, Los Angeles, CA 90210',
                    price=750000.00,
                    bedrooms=4,
                    bathrooms=3,
                    square_feet=2500,
                    lot_size='0.25 acres',
                    year_built=2015,
                    features=json.dumps(['Pool', 'Garage', 'Garden', 'Modern Kitchen']),
                    agent_id=agent.id
                ),
                Property(
                    title='Downtown Luxury Apartment',
                    description='Modern apartment in the heart of downtown.',
                    property_type='apartment',
                    location='New York, NY',
                    address='456 Park Avenue, New York, NY 10001',
                    price=1200000.00,
                    bedrooms=2,
                    bathrooms=2,
                    square_feet=1200,
                    year_built=2020,
                    features=json.dumps(['Gym', 'Doorman', 'City View', 'Hardwood Floors']),
                    agent_id=agent.id
                ),
                Property(
                    title='Cozy Townhouse',
                    description='Perfect starter home in a quiet neighborhood.',
                    property_type='townhouse',
                    location='Austin, TX',
                    address='789 Oak Street, Austin, TX 78701',
                    price=450000.00,
                    bedrooms=3,
                    bathrooms=2,
                    square_feet=1800,
                    year_built=2010,
                    features=json.dumps(['Patio', 'Fireplace', 'Walk-in Closet']),
                    agent_id=agent.id
                )
            ]
            
            for property in properties:
                db.session.add(property)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized successfully!")
        print(f"Admin user: admin / admin123")
        print(f"Agent user: agent1 / agent123")
        print(f"Client user: client1 / client123")

if __name__ == '__main__':
    init_database()