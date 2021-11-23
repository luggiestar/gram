from django.shortcuts import render, redirect, get_object_or_404

# from ..model_test import Plan
from ..models import *


def home(request):
    get_plan = Plan.objects.all()
    return render(request, 'GRAMONEY/index.html',{'plan':get_plan} )
