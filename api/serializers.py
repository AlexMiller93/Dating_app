from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'avatar', 'gender', 'first_name', 'last_name', 'email')
        
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