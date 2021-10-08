
from usuario.views import UserViewSet, listProfileViewSet, listUserViewSet, profileViewSet
from usuario.views import GroupViewSet,PermisosViewSet,PermisosGruposViewSet
from django.urls.conf import path


urlpatterns = [
    path('buscar-profiles/<int:pk>/',profileViewSet.as_view(), name = "Profile"),
    path('lista-de-profiles/', listProfileViewSet.as_view(), name = "Profiles"),
    path('buscar-users/<int:pk>/',UserViewSet.as_view(), name = "User"),
    path('lista-de-users/', listUserViewSet.as_view(), name = "Users"),
    path('grupos/',GroupViewSet.as_view(), name = "Grupos"),
    path('permisos/',PermisosViewSet.as_view(), name ="Permisos"),
    path('asignarPermisosRoles/',PermisosGruposViewSet.as_view()),
    path('getPermisosRoles/<int:pk>',PermisosGruposViewSet.as_view())
]