from math import radians, sin, cos, acos

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from rest_framework import serializers

from authentication.models import Geolocation
from match.models import Match

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'avatar', 'gender', 
            'first_name', 'last_name', 
            'password', 'email')
        
    def validate_avatar(self, avatar):
        if not avatar:
            return avatar
        
        MAX_FILE_SIZE = 8388608
        MIN_FILE_SIZE = 102400
        if avatar.size > MAX_FILE_SIZE:
            raise serializers.ValidationError(
                'Загружаемое фото больше 8 МБ'
            )
        if avatar.size < MIN_FILE_SIZE:
            raise serializers.ValidationError(
                'Загружаемое фото меньше 100 кБ'
            )
        return avatar

class UserListSerializer(serializers.ModelSerializer):
    distance = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id', 'avatar', 'gender', 'first_name', 'last_name', 'email', 'distance',)

    def get_distance(self, obj):
        return obj.distance

class MatchSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    matching = serializers.SlugRelatedField(
        slug_field='email', required=False,
        queryset=User.objects.all()
    )
    mark = serializers.BooleanField()

    class Meta:
        model = Match
        fields = ('user', 'matching', 'mark')

    def create(self, validated_data):
        return Match.objects.create(**validated_data)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        user = self.context['request'].user
        matching = self.context['matching']

        if Match.objects.filter(user=user, matching=matching).exists():
            raise serializers.ValidationError(
                'Запись с таким совпадинем есть в БД, можно ее обновить'
            )

        if user == matching:
            raise serializers.ValidationError(
                'Нельзя давать оценку на самого себя'
            )

        return data


class GeolocationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Geolocation
        fields = ('user', 'latitude', 'longitude',)

    def create(self, validated_data):
        geolocation, created = Geolocation.objects.get_or_create(
            user=validated_data['user']
        )
        geolocation.latitude = validated_data['latitude']
        geolocation.longitude = validated_data['longitude']
        geolocation.save()
        return geolocation