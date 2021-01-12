import json

from django.shortcuts import render
from api.models import *


# Create your views here.
def index(request):
    result = MechineInfo.objects.last()
    print(result)
    context = {"result":result}
    return render(request, "index.html", context)