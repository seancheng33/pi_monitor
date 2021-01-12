import json

from django.shortcuts import render
from api.models import *


# Create your views here.
def index(request):
    # 因为这里我是要做单机的，所以这个我只取最后的数据
    result = MechineInfo.objects.last()

    context = {"result":result}
    return render(request, "index.html", context)