from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *


# Create your views here.
class MemInfoView(viewsets.ModelViewSet):
    queryset = MemInfo.objects.all().order_by('-pk')

    serializer_class = MemInfoSerrializers


class LoginFailedView(viewsets.ModelViewSet):
    queryset = LoginFailed.objects.all().order_by('-pk')

    serializer_class = LoginFailedSerrializers


class DiskInfoView(viewsets.ModelViewSet):
    queryset = DiskInfo.objects.all().order_by('-pk')

    serializer_class = DiskInfoSerrializers

class MechineInfoView(viewsets.ModelViewSet):
    queryset = MechineInfo.objects.all().order_by('-pk')

    serializer_class = MechineInfoSerrializers