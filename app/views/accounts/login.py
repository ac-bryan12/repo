from app.serializers.serializer_permission import GroupSerializer, PermissionSerializer
from typing import cast
from django.urls import path, include,re_path,reverse
from django.contrib.auth.models import Group, User
from django.contrib.sessions.models import Session
from rest_framework import routers, serializers, viewsets
from app.serializers.serializer_login import LoginSerializer
from app.serializers.serializer_user import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from datetime import datetime
from django.utils.http import urlencode
import json,io
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.contrib.auth import login,logout
from rest_framework import status, permissions
from rest_framework.renderers import JSONRenderer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = LoginSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

# loginView
class LoginView(APIView):
    # throttle_classes = ()
    # permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = [permissions.AllowAny]
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
        user:User = serializer.validated_data['email']
        if user is not None :
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                if created :
                    # login(request, user)
                    user_S = UserSerializer(user)
                    return Response({"token":token.key})
                else:
                    all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.pk == int(session_data.get('_auth_user_id')):
                                print('borrado')
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user=user)
                    # login(request, user)
                    
                    user_S = UserSerializer(user)
                    return Response({"token":token.key})
                    
        else: 
            return Response({'error':'El usuario no existe en el sistema'},status=status.HTTP_400_BAD_REQUEST)
      

class LogoutView(APIView):

    def post(self, request):
        request.user.auth_token.delete()
        data = {"estado": "SESION_TERMINADA"}
        return Response(data, status=status.HTTP_200_OK)





class UserPermissionView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class= GroupSerializer

    def get(self,request):
        serializer_group = self.serializer_class(request.user.groups.all(),many=True)
        serializer_permission = PermissionSerializer(request.user.user_permissions.all(),many=True)
        response = Response()
        group = JSONRenderer().render(serializer_group.data)
        permissions = JSONRenderer().render(serializer_permission.data)
        response.set_cookie('group',group)
        response.set_cookie('permissions',permissions)
        return response



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    re_path(r'^',include(router.urls),name="usuarios"),
    path('permission/',UserPermissionView.as_view())
]