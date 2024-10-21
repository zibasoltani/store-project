import os
import django

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_project.settings')

# Setup Django
django.setup()

from accounts.models import User

# Get user information from input
username = input("Please enter the username: ")
password = input("Please enter the password: ")
email = input("Please enter the email: ")
first_name = input("Please enter the first name: ")
last_name = input("Please enter the last name: ")
phone_number = input("Please enter the phone number: ")

# Create a new user and define it as a superuser
user = User.objects.create_superuser(username=username, password=password, email=email, user_type=1)
user.first_name = first_name
user.last_name = last_name
user.phone_number = phone_number
user.save()

print("New user created successfully.")
