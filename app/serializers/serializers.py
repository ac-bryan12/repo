from rest_framework import serializers
from rest_framework import generics
from app.models.plan import Plan
from django.urls import path


class planSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['nombre','precio','description','documentos','reportes','soporte','firma','usuarios','clientes']

class planViewSet(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = planSerializer


    
urlpatterns = [
    path('planes.format.json/',planViewSet.as_view()),
]
