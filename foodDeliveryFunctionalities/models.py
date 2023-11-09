from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    address=models.TextField()
    isRestaurantOwner=models.BooleanField(default=False)
    isDeliveryPatner=models.BooleanField(default=False)


    def __str__(self):
        return self.username