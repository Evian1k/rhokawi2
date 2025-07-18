#!/usr/bin/env python3
"""
Add sample verified properties for immediate website demonstration.
"""

from app import create_app, db
from app.models import Property, User
import json

def add_sample_properties():
    """Add sample properties for immediate sale demonstration."""
    app = create_app()
    
    with app.app_context():
        # Get admin user
        admin = User.query.filter_by(username='evian12k').first()
        if not admin:
            print("❌ Admin user not found")
            return
        
        # Sample properties data
        properties = [
            {
                'title': 'Luxury 4-Bedroom Villa in Karen',
                'description': 'Stunning modern villa with panoramic views, spacious living areas, and premium finishes. Features include a swimming pool, landscaped gardens, and 24/7 security. Perfect for executives and families seeking luxury living in one of Nairobi\'s most prestigious neighborhoods.',
                'property_type': 'Villa',
                'location': 'Karen, Nairobi',
                'address': 'Karen Ridge, Karen Road',
                'price': 28500000,  # 28.5M KES
                'bedrooms': 4,
                'bathrooms': 4,
                'square_feet': 3500,
                'lot_size': '0.5 acres',
                'year_built': 2021,
                'status': 'available',
                'features': json.dumps([
                    'Swimming Pool',
                    'Landscaped Gardens',
                    '24/7 Security',
                    'Modern Kitchen',
                    'Master En-suite',
                    'Parking for 3 cars',
                    'Backup Generator',
                    'Fiber Internet Ready'
                ]),
                'is_verified': True,
                'admin_id': admin.id
            },
            {
                'title': 'Modern 3-Bedroom Apartment in Westlands',
                'description': 'Contemporary apartment in the heart of Westlands business district. Features an open-plan living design, modern kitchen, and spectacular city views. Close to shopping malls, restaurants, and major business centers.',
                'property_type': 'Apartment',
                'location': 'Westlands, Nairobi',
                'address': 'Westlands Square, Parklands Road',
                'price': 15200000,  # 15.2M KES
                'bedrooms': 3,
                'bathrooms': 2,
                'square_feet': 1800,
                'year_built': 2020,
                'status': 'available',
                'features': json.dumps([
                    'City Views',
                    'Modern Kitchen',
                    'Open Plan Living',
                    'Balcony',
                    'Covered Parking',
                    'Elevator Access',
                    'Gym Facility',
                    'Rooftop Garden'
                ]),
                'is_verified': True,
                'admin_id': admin.id
            },
            {
                'title': 'Executive Townhouse in Kilimani',
                'description': 'Elegant 3-bedroom townhouse in a gated community. Features include a private garden, modern amenities, and excellent security. Ideal for young professionals and small families seeking convenience and style.',
                'property_type': 'Townhouse',
                'location': 'Kilimani, Nairobi',
                'address': 'Kilimani Estate, Argwings Kodhek Road',
                'price': 18900000,  # 18.9M KES
                'bedrooms': 3,
                'bathrooms': 3,
                'square_feet': 2200,
                'lot_size': '0.1 acres',
                'year_built': 2019,
                'status': 'available',
                'features': json.dumps([
                    'Gated Community',
                    'Private Garden',
                    'Modern Finishes',
                    'DSQ',
                    'Covered Parking',
                    'Children\'s Play Area',
                    'Clubhouse',
                    'Borehole Water'
                ]),
                'is_verified': True,
                'admin_id': admin.id
            },
            {
                'title': 'Prime Commercial Building in Upper Hill',
                'description': 'Strategic commercial property in Nairobi\'s business hub. Multi-story building with modern office spaces, retail units, and ample parking. Excellent investment opportunity with high rental yields.',
                'property_type': 'Commercial',
                'location': 'Upper Hill, Nairobi',
                'address': 'Upper Hill Business District',
                'price': 85000000,  # 85M KES
                'bedrooms': 0,
                'bathrooms': 12,
                'square_feet': 8500,
                'year_built': 2018,
                'status': 'available',
                'features': json.dumps([
                    'Prime Location',
                    'Multiple Office Units',
                    'Retail Spaces',
                    'Elevator',
                    'Backup Power',
                    'Parking for 50 cars',
                    'High Speed Internet',
                    'Modern HVAC System'
                ]),
                'is_verified': True,
                'admin_id': admin.id
            },
            {
                'title': 'Luxury Penthouse in Lavington',
                'description': 'Exclusive penthouse with breathtaking views and premium amenities. Features include a private terrace, jacuzzi, and state-of-the-art smart home technology. The epitome of luxury living in Nairobi.',
                'property_type': 'Penthouse',
                'location': 'Lavington, Nairobi',
                'address': 'Lavington Green, James Gichuru Road',
                'price': 45000000,  # 45M KES
                'bedrooms': 4,
                'bathrooms': 5,
                'square_feet': 4200,
                'year_built': 2022,
                'status': 'available',
                'features': json.dumps([
                    'Private Terrace',
                    'Jacuzzi',
                    'Smart Home Technology',
                    'Panoramic Views',
                    'Wine Cellar',
                    'Private Elevator',
                    'Concierge Service',
                    'Premium Finishes'
                ]),
                'is_verified': True,
                'admin_id': admin.id
            },
            {
                'title': 'Family Home in Runda',
                'description': 'Spacious family home in the prestigious Runda estate. Features mature gardens, swimming pool, and multiple entertainment areas. Perfect for families seeking tranquility and luxury.',
                'property_type': 'House',
                'location': 'Runda, Nairobi',
                'address': 'Runda Estate, Runda Drive',
                'price': 32000000,  # 32M KES
                'bedrooms': 5,
                'bathrooms': 4,
                'square_feet': 4000,
                'lot_size': '0.75 acres',
                'year_built': 2017,
                'status': 'available',
                'features': json.dumps([
                    'Swimming Pool',
                    'Mature Gardens',
                    'Guest Wing',
                    'Staff Quarters',
                    'Double Garage',
                    'Security System',
                    'Backup Generator',
                    'Borehole'
                ]),
                'is_verified': True,
                'admin_id': admin.id
            }
        ]
        
        # Add properties to database
        added_count = 0
        for prop_data in properties:
            # Check if property already exists
            existing = Property.query.filter_by(title=prop_data['title']).first()
            if not existing:
                property = Property(**prop_data)
                db.session.add(property)
                added_count += 1
                print(f"✅ Added: {prop_data['title']}")
            else:
                print(f"⚠️  Already exists: {prop_data['title']}")
        
        db.session.commit()
        
        # Summary
        total_properties = Property.query.count()
        verified_properties = Property.query.filter_by(is_verified=True).count()
        
        print(f"\n🎯 PROPERTIES READY FOR SALE:")
        print(f"✅ Total properties: {total_properties}")
        print(f"✅ Verified (public can see): {verified_properties}")
        print(f"✅ New properties added: {added_count}")
        print(f"\n🚀 Website ready for immediate demonstration and sale!")

if __name__ == '__main__':
    add_sample_properties()