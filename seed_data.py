
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from faker import Faker
from home.models import Student

fake = Faker()

courses = ["Python", "Django", "Java", "Android", "Data Science"]

for _ in range(20):
    Student.objects.create(
        name=fake.name(),
        roll_number=fake.unique.random_int(min=10000, max=99999),
        course=fake.random_element(elements=courses)
    )

print("20 fake students created successfully!")
