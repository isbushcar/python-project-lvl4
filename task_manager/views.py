from django.http import HttpResponse
from django.template import loader
from django.views import View


class IndexView(View):  # TODO: rework

    def get(self, request):
        template = loader.get_template('task_manager/index.html')
        context = {
            'page_title': 'Hello, world!',
        }
        return HttpResponse(template.render(context, request))


