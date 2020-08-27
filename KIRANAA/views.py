from math import ceil

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

#from .models import Merchentdb, Product


def index(request):
    return render(request,'kirana/home.html')
