"""Seed MongoDB Atlas with the sample data from the project brief."""

from django.core.management.base import BaseCommand
from Backend import db


SAMPLE_CUSTOMERS = [
    {
        "customer_id": 101,
        "full_name": "Rahul Sharma",
        "email": "rahul@gmail.com",
        "phone": "9876543210",
        "city": "Hyderabad",
        "password": "rahul123",
    },
    {
        "customer_id": 102,
        "full_name": "Priya Verma",
        "email": "priya@gmail.com",
        "phone": "9123456780",
        "city": "Mumbai",
        "password": "priya123",
    },
]

SAMPLE_PROPERTIES = [
    {
        "property_id": 201,
        "property_title": "Luxury 3BHK Apartment",
        "property_type": "Apartment",
        "location": "Bangalore",
        "price": 8500000,
        "bedrooms": 3,
        "bathrooms": 2,
        "area_sqft": 1650,
        "status": "Available",
        "image_url": "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",
    },
    {
        "property_id": 202,
        "property_title": "Seaside Villa Retreat",
        "property_type": "Villa",
        "location": "Goa",
        "price": 18500000,
        "bedrooms": 4,
        "bathrooms": 4,
        "area_sqft": 3200,
        "status": "Available",
        "image_url": "https://images.pexels.com/photos/1061391/pexels-photo-1061391.jpeg",
    },
    {
        "property_id": 203,
        "property_title": "Modern Independent House",
        "property_type": "Independent House",
        "location": "Hyderabad",
        "price": 6500000,
        "bedrooms": 3,
        "bathrooms": 2,
        "area_sqft": 1800,
        "status": "Rented",
        "image_url": "https://images.pexels.com/photos/2287310/pexels-photo-2287310.jpeg",
    },
    {
        "property_id": 204,
        "property_title": "Prime Commercial Office Space",
        "property_type": "Commercial",
        "location": "Mumbai",
        "price": 25000000,
        "bedrooms": 0,
        "bathrooms": 2,
        "area_sqft": 2400,
        "status": "Available",
        "image_url": "https://images.pexels.com/photos/380769/pexels-photo-380769.jpeg",
    },
    {
        "property_id": 205,
        "property_title": "Residential Plot in Green County",
        "property_type": "Plot",
        "location": "Pune",
        "price": 4500000,
        "bedrooms": 0,
        "bathrooms": 0,
        "area_sqft": 2400,
        "status": "Sold",
        "image_url": "https://images.pexels.com/photos/210182/pexels-photo-210182.jpeg",
    },
    {
        "property_id": 206,
        "property_title": "Skyline Penthouse 4BHK",
        "property_type": "Apartment",
        "location": "Bangalore",
        "price": 15500000,
        "bedrooms": 4,
        "bathrooms": 3,
        "area_sqft": 2800,
        "status": "Available",
        "image_url": "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg",
    },
]

SAMPLE_AGENTS = [
    {
        "agent_id": 301,
        "agent_name": "Anil Kumar",
        "phone": "9876541230",
        "email": "anil@realestate.com",
        "experience": 8,
        "specialization": "Residential Properties",
    },
    {
        "agent_id": 302,
        "agent_name": "Sneha Reddy",
        "phone": "9876501234",
        "email": "sneha@realestate.com",
        "experience": 6,
        "specialization": "Commercial Properties",
    },
    {
        "agent_id": 303,
        "agent_name": "Vikram Singh",
        "phone": "9876512345",
        "email": "vikram@realestate.com",
        "experience": 11,
        "specialization": "Luxury Villas",
    },
]

SAMPLE_BOOKINGS = [
    {
        "booking_id": 401,
        "customer_name": "Rahul Sharma",
        "property_title": "Luxury 3BHK Apartment",
        "visit_date": "2026-08-20",
        "visit_time": "11:00",
        "agent_name": "Anil Kumar",
        "booking_status": "Scheduled",
    },
    {
        "booking_id": 402,
        "customer_name": "Priya Verma",
        "property_title": "Seaside Villa Retreat",
        "visit_date": "2026-09-05",
        "visit_time": "16:30",
        "agent_name": "Vikram Singh",
        "booking_status": "Completed",
    },
]

SAMPLE_INQUIRIES = [
    {
        "inquiry_id": 501,
        "customer_name": "Rahul Sharma",
        "property_title": "Luxury 3BHK Apartment",
        "message": "Is home loan assistance available?",
        "inquiry_date": "2026-08-10",
        "response_status": "Pending",
    },
    {
        "inquiry_id": 502,
        "customer_name": "Priya Verma",
        "property_title": "Seaside Villa Retreat",
        "message": "What are the maintenance charges per month?",
        "inquiry_date": "2026-08-12",
        "response_status": "Responded",
    },
]


class Command(BaseCommand):
    help = "Seed MongoDB Atlas with sample data for the Real Estate Portal."

    def handle(self, *args, **options):
        db.init_counters()
        collections = {
            "customers": (SAMPLE_CUSTOMERS, "customer_id"),
            "properties": (SAMPLE_PROPERTIES, "property_id"),
            "agents": (SAMPLE_AGENTS, "agent_id"),
            "bookings": (SAMPLE_BOOKINGS, "booking_id"),
            "inquiries": (SAMPLE_INQUIRIES, "inquiry_id"),
        }
        for name, (docs, id_field) in collections.items():
            col = db.get_collection(name)
            inserted = 0
            for doc in docs:
                if col.find_one({id_field: doc[id_field]}) is None:
                    col.insert_one(doc.copy())
                    inserted += 1
            self.stdout.write(
                self.style.SUCCESS(f"{name}: {inserted} inserted, {len(docs)} total")
            )
        # Bump counters past the sample ids so new records don't collide.
        db.get_collection("counters").update_one(
            {"_id": "customers"}, {"$set": {"seq": 102}}, upsert=True
        )
        db.get_collection("counters").update_one(
            {"_id": "properties"}, {"$set": {"seq": 206}}, upsert=True
        )
        db.get_collection("counters").update_one(
            {"_id": "agents"}, {"$set": {"seq": 303}}, upsert=True
        )
        db.get_collection("counters").update_one(
            {"_id": "bookings"}, {"$set": {"seq": 402}}, upsert=True
        )
        db.get_collection("counters").update_one(
            {"_id": "inquiries"}, {"$set": {"seq": 502}}, upsert=True
        )
        self.stdout.write(self.style.SUCCESS("Seed complete."))
