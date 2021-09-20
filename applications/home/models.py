# Django
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField('Imagen', upload_to='media/promotions')
    phone_number = models.CharField('Telefono', max_length=100)
    short_description = models.TextField('Direccion')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfil de usuarios"


class AnonymousUser(models.Model):
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name = "Usuario Anonimo"
        verbose_name_plural = "Usuarios Anonimos"


class Room(models.Model):
    anonymousUser = models.ForeignKey(AnonymousUser, on_delete=models.SET_NULL, blank=True, null=True)
    speaker = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return 'a'
    #     return "{} {}".format(self.anonymousUser.ip_address, self.speaker.user.username)

    class Meta:
        verbose_name = "Habitacion"
        verbose_name_plural = "Habitaciones"
