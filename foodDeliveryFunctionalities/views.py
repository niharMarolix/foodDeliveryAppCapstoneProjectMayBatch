from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
import random
from django.core.cache import cache
from django.core.mail import send_mail
from .models import *


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
    
@csrf_exempt
def send_otp(request):
    email = (json.loads(request.body))['email']

    userObjExist = User.objects.filter(email=email).exists()

    if userObjExist == False:
        return JsonResponse({
            "status":"failed",
            "message":"User not registered"
        }, status = status.HTTP_404_NOT_FOUND)
    
    else:
        userObj = User.objects.get(email=email)

        otp = random.randint(1000,9999)

        cache.set(email, otp, timeout=50)

        subject = "OTP for reset password"
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        

        html_message = render_to_string("send_otp.html", {"otp":otp})

        email = EmailMultiAlternatives(subject,'', from_email, to_email)
        email.attach_alternative(html_message, "text/html")
        email.send()
        return JsonResponse({
            "status":"success",
            "message":"OTP sent successfully"
        }, status = status.HTTP_200_OK)









        


        
