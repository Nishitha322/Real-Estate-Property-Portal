#!/usr/bin/env python
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings")
django.setup()

from Backend.db import get_collection

get_collection('properties').delete_many({})
get_collection('customers').delete_many({})
get_collection('agents').delete_many({})
get_collection('bookings').delete_many({})
get_collection('inquiries').delete_many({})
get_collection('counters').delete_many({})
print('✓ All collections cleared')
