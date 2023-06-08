from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from PIL import Image as Im

from .manager import UserCustomManager

# Create your models here.
class User(AbstractUser):
    
    class Gender(models.TextChoices):
        MEN = 'M', _('Мужчина')
        WOMEN = 'W', _('Женчина')
        
    first_name = models.CharField(
        max_length=100, 
        null=False,
        blank=False,
        verbose_name='Имя',
        help_text="Введите ваше имя")
    
    last_name = models.CharField(
        max_length=100, 
        null=False,
        blank=False,
        verbose_name='Фамилия',
        help_text="Введите вашу фамилию")
    
    avatar = models.ImageField(
        upload_to='images/users/avatars', 
        default='images/users/avatars/default.jpg',
        null=False,
        blank=False,
        verbose_name='Аватар',
        help_text="Загрузите фотографию с вами")
    
    email = models.EmailField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name='Адрес электронной почты',
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
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserCustomManager()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        
        
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