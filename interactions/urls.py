
from django.urls import path

from .views import (
    LikeListCreateView,
    LikeDetailView,
    MutualLikesView,
    ProfileViewHistoryListView,
    DateInvitationListCreateView,
    DateInvitationDetailView,
)

urlpatterns = [
    path('likes/', LikeListCreateView.as_view(), name='like-list'),
    path(
        'likes/<int:pk>/',
        LikeDetailView.as_view(),
        name='like-detail',
    ),
    path(
    'view-history/',
    ProfileViewHistoryListView.as_view(),
    name='profile-view-history',
    ),
    path(
        'mutual-likes/',
        MutualLikesView.as_view(),
        name='mutual-likes',
    ),
    path(
    'invitations/',
    DateInvitationListCreateView.as_view(),
    name='invitation-list',
    ),
    path(
    'invitations/<int:pk>/',
    DateInvitationDetailView.as_view(),
    name='invitation-detail',
    ),
]
