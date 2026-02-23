
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):
	username = None  # Remove the username field
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	address = models.TextField(blank=True, null=True)
	phone_number = models.CharField(max_length=20, blank=True, null=True)
	password = models.CharField(max_length=128)  # Store hashed password
	USERNAME_FIELD = 'email'  # Use email as the unique identifier
	REQUIRED_FIELDS = []  # No additional required fields
	objects = CustomUserManager()  # Use the custom user manager

	def __str__(self):
		return f"{self.first_name} {self.last_name}"
