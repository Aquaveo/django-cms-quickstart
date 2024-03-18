from django.shortcuts import render
import os


def home(request):
    home_path = os.environ.get("PREFIX_TO_PATH")
    return render(request, "base.html", {"home_path": home_path})
