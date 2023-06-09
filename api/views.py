from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from match.models import Match
from .serializers import MatchSerializer, UserSerializer, UserListSerializer
from .services import check_matching

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
    ordering_fields = ('id', 'first_name', 'last_name')
    ordering = ('-id',)

class MatchAPIView(APIView):

    def get(self, request, id):
        matching = get_object_or_404(User, id=id)
        serializer = UserListSerializer(matching, many=False)
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