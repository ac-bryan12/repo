from django.db.models.signals import post_save
from empresa.models import Empresa
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

RUC = "RUC"
CEDULA = "CEDULA"

class Profile(models.Model):
    n_identificacion = models.CharField(primary_key=True, max_length=13)
    tipo_identificacion = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    direccion = models.CharField(max_length=150,null=True)
    telefono =  models.CharField(max_length=13,null=True)
    cargoEmpres = models.CharField(max_length=150,null= True)
    empresa = models.ForeignKey(Empresa,on_delete=models.SET_NULL,null=True)
    # firmaElectronica = models.TextField(max_length=100,null=True) # Ni idea de que va aca

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
