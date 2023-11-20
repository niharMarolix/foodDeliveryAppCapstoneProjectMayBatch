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

class Restuarent(models.Model):
    restuarentName=models.CharField(max_length=200)
    restuarentOwner=models.CharField(max_length=100)
    address=models.TextField(max_length=500)
    phoneNumber=models.CharField(max_length=20)
    openingTime=models.TimeField()
    closingTime=models.TimeField()
    isOpen=models.BooleanField(default=False)
    
    def __str__(self):
        self.restuarentName

class Menuitem(models.Model):
    dishName=models.CharField(max_length=200)
    dishDescription=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    restuarent=models.ForeignKey(Restuarent,on_delete=models.CASCADE,related_name="menuItem")

    def __str__(self):
        self.dishName

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="order")
    item=models.ManyToManyField(Menuitem,through="Orderitem")
    totalPrice=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"order {self.id} by {self.user.username}"

class Orderitem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    menuItem=models.ForeignKey(Menuitem,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} X {self.menuItem.dishName} in order {self.order.id}"

        



