# Real Estate Property Portal

A full-stack Real Estate Property Portal where property owners can list properties, customers can search and view properties, schedule visits, and submit inquiries, and administrators can manage the entire platform.

Built with a **vanilla HTML/CSS/JavaScript** frontend and a **Django REST API** backend backed by **MongoDB Atlas** (PyMongo).

## Features

### Core Modules (20 REST APIs)
- **Customer Management** — register, list, update, delete customers
- **Property Management** — full CRUD for property listings with type/status
- **Property Agent Management** — manage agents and their contact details
- **Property Visit Booking** — schedule and track property visits
- **Inquiry Management** — submit and track customer inquiries

### Frontend Pages
- Home page with hero banner, search, and featured properties
- Customer registration & login
- Property listings with cards, images, price, location
- Property details with gallery, features, agent info, map, and actions
- Booking page with form and booking history
- Inquiry page with form and inquiry history
- Customer dashboard (saved properties, bookings, inquiries, owned/rented)
- Admin dashboard (manage all 5 modules with add/edit/delete)

### Bonus Features
- Advanced search filters (price, location, type, bedrooms)
- Property image gallery on the details page
- Favorite / wishlist properties (saved in localStorage)
- Google Maps location integration on property details
- Property comparison feature (compare up to 3 side by side)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript (ES6), Fetch API |
| Backend | Django (function-based views), REST APIs |
| Database | MongoDB Atlas (PyMongo) |

## Folder Structure

```
RealEstatePropertyPortal/
├── Backend/
│   ├── manage.py
│   ├── .env                  # MongoDB URI + secrets (gitignored)
│   ├── Backend/
│   │   ├── settings.py       # Django config + Mongo connection
│   │   ├── urls.py           # 20 REST endpoints
│   │   ├── views.py          # Function-based CRUD views
│   │   ├── db.py             # MongoDB Atlas data layer
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── portal/
│       └── management/commands/seed_db.py
└── Frontend/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── properties.html
    ├── property_details.html
    ├── bookings.html
    ├── inquiries.html
    ├── customer_dashboard.html
    ├── admin_dashboard.html
    ├── style.css
    └── script.js
```

## Setup & Run

### 1. Backend (Django + MongoDB Atlas)
```bash
cd Backend
pip install django pymongo python-dotenv django-cors-headers
python manage.py migrate          # creates Django internal tables (sqlite, unused for app data)
python manage.py seed_db          # seeds sample data into MongoDB Atlas
python manage.py runserver 0.0.0.0:8000
```
The API will be available at `http://127.0.0.1:8000/`.

### 2. Frontend
Open `Frontend/index.html` in any browser, or serve the folder with any static server:
```bash
cd Frontend
python3 -m http.server 5500
```
Then visit `http://127.0.0.1:5500/`.

The frontend calls the backend via the Fetch API at `http://127.0.0.1:8000` (configurable via `API_BASE` in `script.js`).

## API Reference

| Module | Method | Endpoint |
|--------|--------|----------|
| Customer | POST | `/customers/add/` |
| Customer | GET | `/customers/` |
| Customer | PUT | `/customers/update/<id>/` |
| Customer | DELETE | `/customers/delete/<id>/` |
| Property | POST | `/properties/add/` |
| Property | GET | `/properties/` (supports `?type=&location=&min_price=&max_price=&bedrooms=&q=`) |
| Property | PUT | `/properties/update/<id>/` |
| Property | DELETE | `/properties/delete/<id>/` |
| Agent | POST | `/agents/add/` |
| Agent | GET | `/agents/` |
| Agent | PUT | `/agents/update/<id>/` |
| Agent | DELETE | `/agents/delete/<id>/` |
| Booking | POST | `/bookings/add/` |
| Booking | GET | `/bookings/` (supports `?customer=`) |
| Booking | PUT | `/bookings/update/<id>/` |
| Booking | DELETE | `/bookings/delete/<id>/` |
| Inquiry | POST | `/inquiries/add/` |
| Inquiry | GET | `/inquiries/` (supports `?customer=`) |
| Inquiry | PUT | `/inquiries/update/<id>/` |
| Inquiry | DELETE | `/inquiries/delete/<id>/` |

## Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Customer | rahul@gmail.com | rahul123 |
| Admin | admin@realestate.com | admin123 |

## Environment Variables

Stored in `Backend/.env` (gitignored):
- `MONGO_URI` — MongoDB Atlas connection string
- `MONGO_DB_NAME` — database name (default: `realestate_portal`)
- `DJANGO_SECRET_KEY` — Django secret key

## Sample Data

Run `python manage.py seed_db` to insert the sample customer, property, agent, booking, and inquiry records from the project brief.

## Notes

- The Django ORM is not used for app data — all persistence goes through PyMongo directly.
- CORS is enabled (`django-cors-headers`) so the static frontend can call the API from any origin.
- Customer passwords are stored in plaintext for this educational project; do not use this approach in production.
