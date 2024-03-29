# Generated by Django 3.2.19 on 2023-06-09 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geolocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Широта')),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Долгота')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='geolocation', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Геолокация',
                'verbose_name_plural': 'Геолокации',
            },
        ),
    ]
