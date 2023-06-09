from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from PIL import Image as Im
from PIL import ImageDraw, ImageFont

from .manager import UserCustomManager

# Create your models here.
class User(AbstractUser):
    
    class Gender(models.TextChoices):
        MEN = 'M', _('Мужчина')
        WOMEN = 'W', _('Женчина')
        
    username = None
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
            
        if not self.avatar:
            return
        width, height = img.size
        
        # водяной знак
        watermark = Im.open(settings.WATERMARK_PATH)
        if watermark.height > 300 or watermark.width > 300:
            output_size = (300,300)
            watermark.thumbnail(output_size)
        mark_width, mark_height = watermark.size
        x = width - mark_width - settings.MARGIN
        y = height - mark_height - settings.MARGIN
        img.paste(watermark, (x, y))
        img.show()
        img.save(self.avatar.path)
        
        '''
        width, height = img.size
        
        if watermark.height > 300 or watermark.width > 300:
            output_size = (300,300)
            watermark.thumbnail(output_size)
            
        watermark.thumbnail(settings.WATERMARK_SIZE)
        mark_width, mark_height = watermark.size
        paste_mask = watermark.split()[3].point(
            lambda i: i * settings.TRANSPARENCY / 100
        )
        x = width - mark_width - settings.MARGIN
        y = height - mark_height - settings.MARGIN
        img.paste(watermark, (x, y), mask=paste_mask)
        img.save(self.avatar.path)
        '''
        
        
class Geolocation(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='geolocation',
        verbose_name='пользователь'
    )
    latitude = models.DecimalField(
        max_digits=11, decimal_places=8,
        verbose_name='Широта'
    )
    longitude = models.DecimalField(
        max_digits=11, decimal_places=8,
        verbose_name='Долгота'
    )

    class Meta:
        verbose_name = 'Геолокация'
        verbose_name_plural = 'Геолокации'

    def __str__(self) -> str:
        return f'{self.latitude}, {self.longitude}'