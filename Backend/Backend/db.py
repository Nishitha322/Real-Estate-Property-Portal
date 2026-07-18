"""
MongoDB Atlas data layer for the Real Estate Property Portal.

A single PyMongo client is created at import time and reused for the life
of the process. Each collection auto-increments its numeric id via the
`counters` collection so documents keep the stable ids expected by the
REST API (customer_id, property_id, agent_id, booking_id, inquiry_id).
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from django.conf import settings

_client = None
_db = None


def get_db():
    """Return the shared MongoDB database handle (lazy singleton)."""
    global _client, _db
    if _db is None:
        _client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=15000)
        _db = _client[settings.MONGO_DB_NAME]
    return _db


def get_collection(name):
    """Return a collection handle from the default database."""
    return get_db()[name]


def next_id(name):
    """
    Atomically increment and return the next id for a collection.

    The `counters` collection stores one document per entity type with the
    shape { _id: <name>, seq: <int> }. Initial seed values start at 100 so
    generated ids line up with the sample data (101, 201, 301, 401, 501).
    """
    counters = get_db()["counters"]
    doc = counters.find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True,
    )
    return doc["seq"]


def init_counters():
    """Seed counter documents so the first id matches the sample data."""
    seeds = {
        "customers": 100,
        "properties": 200,
        "agents": 300,
        "bookings": 400,
        "inquiries": 500,
    }
    counters = get_db()["counters"]
    for name, start in seeds.items():
        existing = counters.find_one({"_id": name})
        if existing is None:
            counters.insert_one({"_id": name, "seq": start})
        elif existing.get("seq", 0) < start:
            counters.update_one({"_id": name}, {"$set": {"seq": start}})


def ping():
    """Sanity check the connection. Returns True if reachable."""
    try:
        get_db().command("ping")
        return True
    except PyMongoError:
        return False
