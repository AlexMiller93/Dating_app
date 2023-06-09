from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import MatchAPIView, UserViewSet, UserListViewSet

router = routers.DefaultRouter()
router.register('clients/create', UserViewSet, basename='user_create')
router.register('list', UserListViewSet, basename='users_list')

urlpatterns = [
    path('', include(router.urls)),
    path('clients/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('clients/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('clients/<int:id>/match/', MatchAPIView.as_view()),
]