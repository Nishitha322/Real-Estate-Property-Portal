"""
Function-based REST views for the Real Estate Property Portal.

All endpoints accept and return JSON. Numeric ids are stored as ints in
MongoDB and surfaced as ints in the API. Each CRUD module follows the same
shape: add (POST), list (GET), update (PUT), delete (DELETE), plus a
detail endpoint that resolves a single document by id.
"""
from django.shortcuts import render
import json
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from . import db


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_json(request):
    """Parse a JSON body, returning {} on empty/invalid input."""
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None


def json_response(data, status=200):
    return JsonResponse(data, status=status, safe=False)


def error(message, status=400):
    return JsonResponse({"error": message}, status=status)


def require_json(request):
    body = parse_json(request)
    if body is None:
        return None, error("Invalid JSON body")
    return body, None


def serialize(doc):
    """Convert a Mongo document into a JSON-friendly dict with a clean id."""
    if doc is None:
        return None
    doc.pop("_id", None)
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.date().isoformat()
    return doc


def find_by_id(collection_name, entity_id, id_field):
    return db.get_collection(collection_name).find_one({id_field: int(entity_id)})


# ---------------------------------------------------------------------------
# API root + seed
# ---------------------------------------------------------------------------

def api_root(request):
    if request.method == "POST" and request.path == "/seed/":
        return seed_data(request)
    return JsonResponse({
        "name": "Real Estate Property Portal API",
        "version": "1.0",
        "endpoints": [
            "/customers/", "/properties/", "/agents/",
            "/bookings/", "/inquiries/",
        ],
    })


def seed_data(request):
    """Insert the sample data from the project brief if collections empty."""
    db.init_counters()
    customers = db.get_collection("customers")
    properties = db.get_collection("properties")
    agents = db.get_collection("agents")
    bookings = db.get_collection("bookings")
    inquiries = db.get_collection("inquiries")

    if customers.count_documents({}) == 0:
        customers.insert_many([
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
        ])
    if properties.count_documents({}) == 0:
        properties.insert_many([
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
                "image_url": "https://picsum.photos/500/400?random=1",
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
                "image_url": "https://picsum.photos/500/400?random=2",
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
                "image_url": "https://picsum.photos/500/400?random=3",
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
                "image_url": "https://picsum.photos/500/400?random=4",
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
                "image_url": "https://picsum.photos/500/400?random=5",
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
                "image_url": "https://picsum.photos/500/400?random=6",
            },
        ])
    if agents.count_documents({}) == 0:
        agents.insert_many([
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
        ])
    if bookings.count_documents({}) == 0:
        bookings.insert_many([
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
        ])
    if inquiries.count_documents({}) == 0:
        inquiries.insert_many([
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
        ])
    return JsonResponse({"message": "Sample data seeded"})


# ---------------------------------------------------------------------------
# Module 1 — Customer Management
# ---------------------------------------------------------------------------

def add_customer(request):
    if request.method != "POST":
        return error("POST required", 405)
    body, err = require_json(request)
    if err:
        return err
    for field in ("full_name", "email", "phone", "city", "password"):
        if not body.get(field):
            return error(f"Missing field: {field}")
    doc = {
        "customer_id": db.next_id("customers"),
        "full_name": body["full_name"],
        "email": body["email"],
        "phone": body["phone"],
        "city": body.get("city", ""),
        "password": body["password"],
    }
    db.get_collection("customers").insert_one(doc)
    return json_response(serialize(doc), 201)


def list_customers(request):
    if request.method != "GET":
        return error("GET required", 405)
    docs = list(db.get_collection("customers").find().sort("customer_id", 1))
    return json_response([serialize(d) for d in docs])
def home(request):
    return render(request, "index.html")

def customer_detail(request, cid):
    if request.method != "GET":
        return error("GET required", 405)
    doc = find_by_id("customers", cid, "customer_id")
    if not doc:
        return error("Customer not found", 404)
    return json_response(serialize(doc))


def update_customer(request, cid):
    if request.method != "PUT":
        return error("PUT required", 405)
    body, err = require_json(request)
    if err:
        return err
    update = {k: v for k, v in body.items() if k != "customer_id"}
    res = db.get_collection("customers").update_one(
        {"customer_id": int(cid)}, {"$set": update}
    )
    if res.matched_count == 0:
        return error("Customer not found", 404)
    doc = find_by_id("customers", cid, "customer_id")
    return json_response(serialize(doc))


def delete_customer(request, cid):
    if request.method != "DELETE":
        return error("DELETE required", 405)
    res = db.get_collection("customers").delete_one({"customer_id": int(cid)})
    if res.deleted_count == 0:
        return error("Customer not found", 404)
    return JsonResponse({"message": "Customer deleted"})


# ---------------------------------------------------------------------------
# Module 2 — Property Management
# ---------------------------------------------------------------------------

def add_property(request):
    if request.method != "POST":
        return error("POST required", 405)
    body, err = require_json(request)
    if err:
        return err
    for field in ("property_title", "property_type", "location", "price"):
        if body.get(field) in (None, ""):
            return error(f"Missing field: {field}")
    doc = {
        "property_id": db.next_id("properties"),
        "property_title": body["property_title"],
        "property_type": body["property_type"],
        "location": body["location"],
        "price": int(body["price"]),
        "bedrooms": int(body.get("bedrooms", 0)),
        "bathrooms": int(body.get("bathrooms", 0)),
        "area_sqft": int(body.get("area_sqft", 0)),
        "status": body.get("status", "Available"),
        "image_url": body.get("image_url", ""),
    }
    db.get_collection("properties").insert_one(doc)
    return json_response(serialize(doc), 201)


def list_properties(request):
    if request.method != "GET":
        return error("GET required", 405)
    query = {}
    property_type = request.GET.get("type")
    location = request.GET.get("location")
    status = request.GET.get("status")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    bedrooms = request.GET.get("bedrooms")
    q = request.GET.get("q")
    if property_type:
        query["property_type"] = property_type
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    if status:
        query["status"] = status
    if min_price or max_price:
        query["price"] = {}
        if min_price:
            query["price"]["$gte"] = int(min_price)
        if max_price:
            query["price"]["$lte"] = int(max_price)
    if bedrooms:
        query["bedrooms"] = {"$gte": int(bedrooms)}
    if q:
        query["$or"] = [
            {"property_title": {"$regex": q, "$options": "i"}},
            {"location": {"$regex": q, "$options": "i"}},
        ]
    docs = list(db.get_collection("properties").find(query).sort("property_id", 1))
    return json_response([serialize(d) for d in docs])


def property_detail(request, pid):
    if request.method != "GET":
        return error("GET required", 405)
    doc = find_by_id("properties", pid, "property_id")
    if not doc:
        return error("Property not found", 404)
    return json_response(serialize(doc))


def update_property(request, pid):
    if request.method != "PUT":
        return error("PUT required", 405)
    body, err = require_json(request)
    if err:
        return err
    update = {}
    for k, v in body.items():
        if k == "property_id":
            continue
        if k in ("price", "bedrooms", "bathrooms", "area_sqft"):
            update[k] = int(v)
        else:
            update[k] = v
    res = db.get_collection("properties").update_one(
        {"property_id": int(pid)}, {"$set": update}
    )
    if res.matched_count == 0:
        return error("Property not found", 404)
    doc = find_by_id("properties", pid, "property_id")
    return json_response(serialize(doc))


def delete_property(request, pid):
    if request.method != "DELETE":
        return error("DELETE required", 405)
    res = db.get_collection("properties").delete_one({"property_id": int(pid)})
    if res.deleted_count == 0:
        return error("Property not found", 404)
    return JsonResponse({"message": "Property deleted"})


# ---------------------------------------------------------------------------
# Module 3 — Property Agent Management
# ---------------------------------------------------------------------------

def add_agent(request):
    if request.method != "POST":
        return error("POST required", 405)
    body, err = require_json(request)
    if err:
        return err
    for field in ("agent_name", "phone", "email"):
        if not body.get(field):
            return error(f"Missing field: {field}")
    doc = {
        "agent_id": db.next_id("agents"),
        "agent_name": body["agent_name"],
        "phone": body["phone"],
        "email": body["email"],
        "experience": int(body.get("experience", 0)),
        "specialization": body.get("specialization", ""),
    }
    db.get_collection("agents").insert_one(doc)
    return json_response(serialize(doc), 201)


def list_agents(request):
    if request.method != "GET":
        return error("GET required", 405)
    docs = list(db.get_collection("agents").find().sort("agent_id", 1))
    return json_response([serialize(d) for d in docs])


def agent_detail(request, aid):
    if request.method != "GET":
        return error("GET required", 405)
    doc = find_by_id("agents", aid, "agent_id")
    if not doc:
        return error("Agent not found", 404)
    return json_response(serialize(doc))


def update_agent(request, aid):
    if request.method != "PUT":
        return error("PUT required", 405)
    body, err = require_json(request)
    if err:
        return err
    update = {k: v for k, v in body.items() if k != "agent_id"}
    if "experience" in update:
        update["experience"] = int(update["experience"])
    res = db.get_collection("agents").update_one(
        {"agent_id": int(aid)}, {"$set": update}
    )
    if res.matched_count == 0:
        return error("Agent not found", 404)
    doc = find_by_id("agents", aid, "agent_id")
    return json_response(serialize(doc))


def delete_agent(request, aid):
    if request.method != "DELETE":
        return error("DELETE required", 405)
    res = db.get_collection("agents").delete_one({"agent_id": int(aid)})
    if res.deleted_count == 0:
        return error("Agent not found", 404)
    return JsonResponse({"message": "Agent deleted"})


# ---------------------------------------------------------------------------
# Module 4 — Property Visit Booking
# ---------------------------------------------------------------------------

def add_booking(request):
    if request.method != "POST":
        return error("POST required", 405)
    body, err = require_json(request)
    if err:
        return err
    for field in ("customer_name", "property_title", "visit_date", "visit_time"):
        if not body.get(field):
            return error(f"Missing field: {field}")
    doc = {
        "booking_id": db.next_id("bookings"),
        "customer_name": body["customer_name"],
        "property_title": body["property_title"],
        "visit_date": body["visit_date"],
        "visit_time": body["visit_time"],
        "agent_name": body.get("agent_name", ""),
        "booking_status": body.get("booking_status", "Scheduled"),
    }
    db.get_collection("bookings").insert_one(doc)
    return json_response(serialize(doc), 201)


def list_bookings(request):
    if request.method != "GET":
        return error("GET required", 405)
    customer = request.GET.get("customer")
    query = {}
    if customer:
        query["customer_name"] = {"$regex": customer, "$options": "i"}
    docs = list(db.get_collection("bookings").find(query).sort("booking_id", 1))
    return json_response([serialize(d) for d in docs])


def booking_detail(request, bid):
    if request.method != "GET":
        return error("GET required", 405)
    doc = find_by_id("bookings", bid, "booking_id")
    if not doc:
        return error("Booking not found", 404)
    return json_response(serialize(doc))


def update_booking(request, bid):
    if request.method != "PUT":
        return error("PUT required", 405)
    body, err = require_json(request)
    if err:
        return err
    update = {k: v for k, v in body.items() if k != "booking_id"}
    res = db.get_collection("bookings").update_one(
        {"booking_id": int(bid)}, {"$set": update}
    )
    if res.matched_count == 0:
        return error("Booking not found", 404)
    doc = find_by_id("bookings", bid, "booking_id")
    return json_response(serialize(doc))


def delete_booking(request, bid):
    if request.method != "DELETE":
        return error("DELETE required", 405)
    res = db.get_collection("bookings").delete_one({"booking_id": int(bid)})
    if res.deleted_count == 0:
        return error("Booking not found", 404)
    return JsonResponse({"message": "Booking deleted"})


# ---------------------------------------------------------------------------
# Module 5 — Inquiry Management
# ---------------------------------------------------------------------------

def add_inquiry(request):
    if request.method != "POST":
        return error("POST required", 405)
    body, err = require_json(request)
    if err:
        return err
    for field in ("customer_name", "property_title", "message"):
        if not body.get(field):
            return error(f"Missing field: {field}")
    doc = {
        "inquiry_id": db.next_id("inquiries"),
        "customer_name": body["customer_name"],
        "property_title": body["property_title"],
        "message": body["message"],
        "inquiry_date": body.get(
            "inquiry_date", datetime.utcnow().strftime("%Y-%m-%d")
        ),
        "response_status": body.get("response_status", "Pending"),
    }
    db.get_collection("inquiries").insert_one(doc)
    return json_response(serialize(doc), 201)


def list_inquiries(request):
    if request.method != "GET":
        return error("GET required", 405)
    customer = request.GET.get("customer")
    query = {}
    if customer:
        query["customer_name"] = {"$regex": customer, "$options": "i"}
    docs = list(db.get_collection("inquiries").find(query).sort("inquiry_id", 1))
    return json_response([serialize(d) for d in docs])


def inquiry_detail(request, iid):
    if request.method != "GET":
        return error("GET required", 405)
    doc = find_by_id("inquiries", iid, "inquiry_id")
    if not doc:
        return error("Inquiry not found", 404)
    return json_response(serialize(doc))


def update_inquiry(request, iid):
    if request.method != "PUT":
        return error("PUT required", 405)
    body, err = require_json(request)
    if err:
        return err
    update = {k: v for k, v in body.items() if k != "inquiry_id"}
    res = db.get_collection("inquiries").update_one(
        {"inquiry_id": int(iid)}, {"$set": update}
    )
    if res.matched_count == 0:
        return error("Inquiry not found", 404)
    doc = find_by_id("inquiries", iid, "inquiry_id")
    return json_response(serialize(doc))


def delete_inquiry(request, iid):
    if request.method != "DELETE":
        return error("DELETE required", 405)
    res = db.get_collection("inquiries").delete_one({"inquiry_id": int(iid)})
    if res.deleted_count == 0:
        return error("Inquiry not found", 404)
    return JsonResponse({"message": "Inquiry deleted"})
