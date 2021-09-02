from django.contrib.auth.models import Group, User
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from rest_framework.authtoken.models import Token


@csrf_exempt
def perfil(request):
    if request.method == 'GET':
        # if 'Authorization' in request.headers.keys():
            # token_key:str = request.headers.get('Authorization')
            # token_key = token_key.removeprefix('Token ')
            # token:Token = Token.objects.filter(key=token_key)
            # if token.exists():
            #     user:User = token.last().user
            #     print(user.groups.all())
        return render(request,'dashboard.html',)
        # else:
        #     return HttpResponse("Sin token")
    
    return HttpResponse("No es petición GET")

urlpatterns = [
    path('perfil/',perfil,name='perfil')
]