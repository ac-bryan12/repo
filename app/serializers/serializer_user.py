from app.models.empresa import Empresa
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import query
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128)
    username = serializers.CharField(max_length=150,required=False)
    firstName = serializers.CharField(max_length=150)
    lastName = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=150)
    direccion = serializers.CharField(max_length=30)
    telefono =  serializers.IntegerField()
    cargo = serializers.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username','firstName','lastName','email', 'password','direccion','telefono', 'cargo']

    # def validate(self, attrs):
    #     print("validate user")
    #     user = User.objects.filter(username=attrs['username'])
    #     if len(user)!=0:
    #         raise serializers.ValidationError("Usuario ya existe en el sistema")
    #     return user

    # def create(self,validated_data):
    #     print("crear usuario")
    #     # userAttrs = validated_data.pop('user')
    #     user = User()
    #     user.username = validated_data['username']
    #     user.email = validated_data['email']
    #     user.set_password(validated_data['password'])
    #     user.first_name = validated_data['first_name']
    #     user.last_name = validated_data['last_name']
    #     user.save()
    #     return user

