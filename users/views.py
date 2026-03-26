from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def home(req):
    return JsonResponse({"status": "working"})