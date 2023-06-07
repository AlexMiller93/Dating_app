from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from PIL import Image as Im

# Create your models here.
class Participant(models.Model):
    
    class Gender(models.TextChoices):
        MEN = 'M', _('Men')
        WOMEN = 'W', _('Women')
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    first_name = models.CharField(
        max_length=100, 
        null=False,
        blank=False,
        help_text="Введите ваше имя")
    
    last_name = models.CharField(
        max_length=100, 
        null=False,
        blank=False,
        help_text="Введите вашу фамилию")
    
    avatar = models.ImageField(
        upload_to='avatars', 
        default='avatars/default.jpg',
        null=False,
        blank=False,
        help_text="Загрузите фотографию с вами")
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        help_text="Введите вашу почту")
    
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.MEN,
        null=False,
        blank=False,
        help_text="Выберите ваш пол")
    
    date_of_birth = models.DateField(
        null=True,
        blank=True,)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    def save(self): 
        super().save()
        img = Im.open(self.avatar.path)
        # уменьшить фотографию
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)