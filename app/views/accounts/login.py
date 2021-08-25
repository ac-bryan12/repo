from django.urls import path, include,re_path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from app.serializers.serializer_login import LoginSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from django.http import QueryDict
from django.utils.http import urlencode
import json,io
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = LoginSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

# loginView
class LoginView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class= LoginSerializer

    def post(self, request):
        serializer:serializers.Serializer
        if 'application/json' in request.META['CONTENT_TYPE']:
            j_data = request.body
            stream = io.BytesIO(j_data)
            q_data = JSONParser().parse(stream)
            serializer = LoginSerializer(data=q_data)
        else:
            serializer = LoginSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['email']
        if user is not None :
            update_last_login(None, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else: 
            return Response({'token':'0'})
        



# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/', LoginView.as_view()),
    # re_path(r'^',include(router.urls),name="usuarios"),
    # path('auth/', ObtainAuthToken.as_view()),
]