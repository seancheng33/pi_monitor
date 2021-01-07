from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *


# Create your views here.
class MemInfoView(viewsets.ModelViewSet):
    queryset = MemInfoModel.objects.all().order_by('-pk')

    serializer_class = MemInfoSerrializers


class LoginFailedView(viewsets.ModelViewSet):
    queryset = LoginFailedModel.objects.all().order_by('-pk')

    serializer_class = LoginFailedSerrializers