from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate


# Create your views here.
# @login_required(login_url="login")
def home(request):
    # if request.user.is_authenticated:
    return render(request, "index.html")

    # return redirect("login")
