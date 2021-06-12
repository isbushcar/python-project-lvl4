from django.shortcuts import render
from django.views import View

from django.http import HttpResponse

# Create your views here.
class IndexView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')