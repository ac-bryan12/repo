from app.models.empresa import Empresa
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import query
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8)
    username = serializers.CharField(max_length=150,required=False)
    firstName = serializers.CharField(min_length=3,max_length=50)
    lastName = serializers.CharField(min_length=3,max_length=50)
    email = serializers.EmailField(min_length=7)
    direccion = serializers.CharField(max_length=255)
    telefono =  serializers.CharField(min_length=10,max_length=10)
    cargo = serializers.CharField(min_length=4,max_length=50)

    class Meta:
        model = User
        fields = ['username','firstName','lastName','email', 'password','direccion','telefono', 'cargo']

    def validate(self, attrs):
        msg:any
        if len(attrs['email']) < 7 :
            msg = _("Email inválido")
        elif User.objects.filter(email=attrs['email']).exists() :
            msg = _("El email ingresado ya existe en el sitema")
        elif len(attrs['password']) < 8 :
            msg = _("Contraseña inválida")
        elif len(attrs['firstName']) < 3 or len(attrs['firstName']) > 50:
            msg = _("Nombre inválido")
        elif len(attrs['lastName']) < 3 or len(attrs['lastName']) > 50 :
            msg = _("Apellido inválido")
        elif len(attrs['cargo']) < 4 or len(attrs['cargo']) > 50 :
            msg = _("Cargo inválido")
        elif len(attrs['telefono']) != 10 :
            msg = _("Teléfono inválido")
        else :
            return attrs
        raise serializers.ValidationError(msg)

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

