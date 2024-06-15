from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def hello(request):
    name = request.GET.get('name', 'World')
    return HttpResponse(f'Hello, {name}')