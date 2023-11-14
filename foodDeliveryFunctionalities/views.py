from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.


@csrf_exempt
def register(request):
    try:
        if request.method != "POST":
            raise Exception("method not allowed")
        
        else:
            data = json.loads(request.body)

            esmail = data["email"]
            usalname = data["username"]
            passworddddd = data["password"]
            address=data["address"]
            isRestaurantOwner=data["isRestaurantOwner"]
            isDeliveryPatner=data["isDeliveryPatner"]



            if not esmail or not usalname or not passworddddd:
                raise Exception("Data not passed or incorrect data passed")
            
            else:
                user = User.objects.create_user(username = usalname, password = passworddddd, email = esmail,address=address,isRestaurantOwner=isRestaurantOwner,isDeliveryPatner=isDeliveryPatner)
                user.save()
                send_mail(
                "congratulations",
                "Greetings and welcome to [Your Food Delivery App Name]! 🌟 We're thrilled to have you join our community of food enthusiasts who share a passion for delicious flavors and convenient dining experiences..",
                settings.DEFAULT_FROM_EMAIL,
                [esmail],
                fail_silently=False,
            )

                return JsonResponse({
                    "status":"Success",
                    "message":f"User {usalname} registered"
                    
                })
    
    except Exception as ex:
        return JsonResponse({
            "status":"failed",
            "message":str(ex)
        })
    