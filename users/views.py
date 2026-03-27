from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def home(req):
    return JsonResponse({"status": "working"})



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer


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