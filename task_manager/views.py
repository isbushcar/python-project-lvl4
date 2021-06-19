from django.shortcuts import render
from django.template import loader
from django.views import View

from django.http import HttpResponse

# Create your views here.
class IndexView(View):

    def get(self, request):
        template = loader.get_template('task_manager/index.html')
        context = {
            'page_title': 'Hello, world!',
        }
        return HttpResponse(template.render(context, request))
