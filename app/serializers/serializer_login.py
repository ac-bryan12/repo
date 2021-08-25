from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import query
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

# Serializers define the API representation.
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30,write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self,attrs):
        user:User;
        try:
            userAcount:User = User.objects.get(email=attrs['email'])
            user = authenticate(username=userAcount.username,password=attrs['password'])

            if user is not None :
                attrs['email'] = user
            else:
                # msg = _('User invalid')
                # raise serializers.ValidationError(msg,code='authorization')
                attrs['email'] = None
        except User.DoesNotExist:
            attrs['email'] = None
        return attrs


    # def create(self,validated_data):
    #      user = User.objects.create(**validated_data)
    #      return user 
