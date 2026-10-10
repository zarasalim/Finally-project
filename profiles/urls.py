
from django.urls import path

from .views import (
    ProfileListView,
    ProfileDetailView,
    MyProfileView,
    MyPhotoListCreateView,
    MyPhotoDetailView,
    RandomProfileView
)

urlpatterns = [
    path('', ProfileListView.as_view(), name='profile-list'),
    path('me/', MyProfileView.as_view(), name='my-profile'),
    path(
        'me/photos/',
        MyPhotoListCreateView.as_view(),
        name='my-photos',
    ),
    path(
        'me/photos/<int:pk>/',
        MyPhotoDetailView.as_view(),
        name='my-photo-detail',
    ),
    path(
        '<int:pk>/',
        ProfileDetailView.as_view(),
        name='profile-detail',
    ),
    path(
    'random/',
    RandomProfileView.as_view(),
    name='random-profile',
    ),
]
