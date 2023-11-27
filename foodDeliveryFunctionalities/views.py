from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken




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
                "Congratulations",
                "Welcome aboard! We're thrilled to have you join the [Your Food Delivery App] family. Get ready for a delightful journey filled with delicious meals delivered right to your doorstep.",
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
    
@csrf_exempt
def login(request):
    try:
        if request.method != "POST":
            raise Exception("method not allowed", status.HTTP_405_METHOD_NOT_ALLOWED)
        
        else:
            data = json.loads(request.body)
            usalname = data["username"]
            passworddddd = data["password"]

            if not usalname or not passworddddd:
                raise Exception("Data not passed or incorrect data passed", status.HTTP_400_BAD_REQUEST)
            
            else:
                user = authenticate(request, username= usalname, password = passworddddd)

                if user is not None:
                    refrest = RefreshToken.for_user(user)

                    return JsonResponse({
                        "refreshToken":str(refrest),
                        "accesstoken":str(refrest.access_token)
                    })


            
    except Exception as ex:
        return JsonResponse({
            "status":"failed",
            "message":str(ex)
        })

def addRestuarent(request):
    if request.user.username!="" and request.user.isRestaurantOwner==True:
        data=json.loads(request.body)
        restuarentName=data["restuarentName"]
        restuarentOwner=data["restuarentOwner"]
        address=data["address"]
        phoneNumber=data["phoneNumber"]
        openingTime=data["openingTime"]
        closingTime=data["closingTime"]


        addRestuarentobj=Restuarent.objects.create(restuarentName=restuarentName,restuarentOwner=restuarentOwner,address=address,phoneNumber=phoneNumber,openingTime=openingTime,closingTime=closingTime,isOpen=False)

        return JsonResponse({
            "status":"success",
            "message":"Restuarant added succesfully"
        })
    else:
        return JsonResponse({
            "status":"success",
            "message":"some error occured"
        })