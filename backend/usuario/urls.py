
from usuario.views import GroupsList, GroupsListPagination, UserViewSet, listProfileViewSet, profileViewSet
from usuario.views import PermisosViewSet,PermisosGruposViewSet,ProfileUserViewSet
from django.urls.conf import path


urlpatterns = [
    path('buscar-profiles/<int:pk>/',profileViewSet.as_view(), name = "Profile"),
    path('buscar-user/<int:pk>/',UserViewSet.as_view(), name = "User"),
    # path('lista-de-users/', listUserViewSet.as_view(), name = "Users"),
    path('lista-de-profiles/', listProfileViewSet.as_view(), name = "Profiles"),
    path('PerfilInfo/',ProfileUserViewSet.as_view()),
    path('grupos/',GroupsListPagination.as_view(), name = "Grupos"),
    path('all_groups/',GroupsList.as_view(), name = "Grupos"),
    path('permisos/<int:pk>/',PermisosViewSet.as_view(), name ="Permisos"),
    path('asignarPermisosRoles/',PermisosGruposViewSet.as_view()),
    path('asignarPermisosRoles/<int:pk>/',PermisosGruposViewSet.as_view()),
    path('getPermisosRoles/<int:pk>/',PermisosGruposViewSet.as_view())
]