"""URL routing for the Real Estate Property Portal REST API."""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("seed/", views.seed_data, name="seed-data"),
    # Customer Management
    path("customers/add/", views.add_customer, name="add-customer"),
    path("customers/", views.list_customers, name="list-customers"),
    path("customers/<int:cid>/", views.customer_detail, name="customer-detail"),
    path("customers/update/<int:cid>/", views.update_customer, name="update-customer"),
    path("customers/delete/<int:cid>/", views.delete_customer, name="delete-customer"),
    # Property Management
    path("properties/add/", views.add_property, name="add-property"),
    path("properties/", views.list_properties, name="list-properties"),
    path("properties/<int:pid>/", views.property_detail, name="property-detail"),
    path("properties/update/<int:pid>/", views.update_property, name="update-property"),
    path("properties/delete/<int:pid>/", views.delete_property, name="delete-property"),
    # Property Agent Management
    path("agents/add/", views.add_agent, name="add-agent"),
    path("agents/", views.list_agents, name="list-agents"),
    path("agents/<int:aid>/", views.agent_detail, name="agent-detail"),
    path("agents/update/<int:aid>/", views.update_agent, name="update-agent"),
    path("agents/delete/<int:aid>/", views.delete_agent, name="delete-agent"),
    # Property Visit Booking
    path("bookings/add/", views.add_booking, name="add-booking"),
    path("bookings/", views.list_bookings, name="list-bookings"),
    path("bookings/<int:bid>/", views.booking_detail, name="booking-detail"),
    path("bookings/update/<int:bid>/", views.update_booking, name="update-booking"),
    path("bookings/delete/<int:bid>/", views.delete_booking, name="delete-booking"),
    # Inquiry Management
    path("inquiries/add/", views.add_inquiry, name="add-inquiry"),
    path("inquiries/", views.list_inquiries, name="list-inquiries"),
    path("inquiries/<int:iid>/", views.inquiry_detail, name="inquiry-detail"),
    path("inquiries/update/<int:iid>/", views.update_inquiry, name="update-inquiry"),
    path("inquiries/delete/<int:iid>/", views.delete_inquiry, name="delete-inquiry"),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATICFILES_DIRS[0]
    )