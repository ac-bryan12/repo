from correo.views import RegisterView
from django.urls.conf import path


urlpatterns = [
    path('registro/',RegisterView.as_view())
]