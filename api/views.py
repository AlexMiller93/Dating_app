import geocoder

from django.db.models import FloatField
from django.db.models.functions import Cos, Sin, Radians
from math import radians

from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from django.contrib.auth.hashers import make_password
from django.db.models import FloatField
from django.db.models.functions import Cos, Radians, Sin
from django.db.models.functions.math import ACos

from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from api.filters import GeolocationFilter

from match.models import Match
from .services import check_matching
from authentication.models import Geolocation

from .serializers import (
    MatchSerializer, 
    UserSerializer, 
    UserListSerializer, 
    GeolocationSerializer
)

from .services import check_matching, get_client_ip

# Create your views here.
User = get_user_model()


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

class UserListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    search_fields = ('^first_name', '^last_name',)
    filterset_fields = ('gender', 'first_name', 'last_name',)
    ordering_fields = ('id', 'first_name', 'last_name',)
    ordering = ('-id',)
    filterset_class = GeolocationFilter
    
    def get_queryset(self):
        request_user = self.request.user.geolocation
        self_latitude = radians(request_user.latitude)
        self_longitude = radians(request_user.longitude)
        latitude = Radians('geolocation__latitude', output_field=FloatField())
        longitude = Radians('geolocation__longitude', output_field=FloatField())
        return User.objects.annotate(distance=
            6371 * ACos(Sin(self_latitude) * Sin(latitude) + Cos(self_latitude
            ) * Cos(longitude) * Cos(self_longitude - longitude))
        ).exclude(id=self.request.user.id)

class MatchAPIView(APIView):

    def get(self, request, id):
        matching = get_object_or_404(User, id=id)
        context = {
            "request": self.request,
            "matching": matching
        }
        serializer = UserListSerializer(matching, context=context, many=False)
        return Response(serializer.data)

    def post(self, request, id):
        matching = get_object_or_404(User, id=id)
        context = {
            "request": self.request,
            "matching": matching
        }
        serializer = MatchSerializer(data=request.data, context=context)
        if serializer.is_valid():
            match = serializer.save(user=request.user, matching=matching)
            if match.mark:
                check_matching(match)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        matching = get_object_or_404(
            Match, user=request.user, matching_id=id
        )
        context = {
            "request": self.request
        }
        serializer = MatchSerializer(matching, data=request.data, context=context, partial=True)
        if serializer.is_valid():
            match = serializer.save()
            if match.mark:
                check_matching(match)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def get_geolocation(request):
    """
    Определяет геолокацию соглассно данным об IP
    """
    ip = get_client_ip(request)
    g = geocoder.ip(ip)
    geolocation = g.latlng
    if not geolocation:
        return Response(
            {'results': 'Невозможно определить местоположение'}, status=status.HTTP_400_BAD_REQUEST
        )
    latitude, longitude = geolocation
    context = {
        "request": request
        }
    data = {
        "latitude": latitude,
        "longitude": longitude
    }
    serializer = GeolocationSerializer(
        data=data, context=context
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def set_geolocation(request):
    """
    Устанавливает заданные значения геолокация,
    если нужно поиск в другой локации
    """
    context = {
        "request": request
        }
    serializer = GeolocationSerializer(
        data=request.data, context=context
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)