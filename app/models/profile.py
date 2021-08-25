from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver
from .empresa import Empresa

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=30,null=True)
    telefono =  models.PositiveBigIntegerField(null=True)
    cargoEmpres = models.CharField(max_length=30,null= True)
    firmaElectronica = models.TextField(max_length=100,null=True) # Ni idea de que va aca
    empresa = models.ForeignKey(Empresa,on_delete=models.SET_NULL,null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()