from django.shortcuts import render
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import auth
import krmappbackend.firebase  # this initializes Firebase

# Create your views here.
def home(req):
    return JsonResponse({"status": "working"})



def api_response(success, data=None, message=""):
    return Response({
        "success": success,
        "data": data if data is not None else [],
        "message": message
    })

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return api_response(True, serializer.data, "User created successfully")
    return api_response(False, [], serializer.errors)

# API to get all users
@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return api_response(True, serializer.data, "Users fetched successfully")

@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = User.objects.filter(email=email).first()

    if not user:
        return api_response(False, message= "User Not Found") 
    
    if not user.password == password:
        return api_response(False, message="Invalid Password")

    refresh = RefreshToken.for_user(user)
    serializer = UserSerializer(user)
    
    return api_response(
        True, 
        {
            "access_token": str(refresh.access_token), 
            "refresh_token": str(refresh),
            "user": serializer.data, 
        }, 
        "Login Successful"
    )


@api_view(["POST"])
def google_login(request):
    id_token = request.data.get("id_token")

    if not id_token:
        return api_response(False, message="ID token missing")

    try:
        decoded_token = auth.verify_id_token(id_token)
    except Exception as e:
        return api_response(False, message="Invalid or expired token")

    google_id = decoded_token.get("uid")
    email = decoded_token.get("email")
    name = decoded_token.get("name")
    picture = decoded_token.get("picture")
    password = decoded_token.get("password")

    # Check if user exists
    user = User.objects.filter(google_id=google_id).first()

    if not user:
        user = User.objects.create(
            google_id=google_id,
            email=email,
            name=name,
            profile_picture=picture,
            password=password  # since you're ignoring password for now
        )

    # Generate JWT
    refresh = RefreshToken.for_user(user)

    serializer = UserSerializer(user)

    return api_response(
        True,
        {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": serializer.data
        },
        "Google login successful"
    )