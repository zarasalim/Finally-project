
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Like
from .serializers import LikeSerializer
from .models import Like, ProfileViewHistory
from .models import Like, ProfileViewHistory, DateInvitation
from .serializers import LikeSerializer, DateInvitationSerializer

from rest_framework.exceptions import PermissionDenied, ValidationError

User = get_user_model()


class LikeListCreateView(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(
            from_user=self.request.user
        ).select_related('to_user')

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class LikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(
            from_user=self.request.user
        )


class MutualLikesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        liked_user_ids = Like.objects.filter(
            from_user=request.user,
            action=Like.Action.LIKE,
        ).values_list('to_user_id', flat=True)

        mutual_user_ids = Like.objects.filter(
            from_user_id__in=liked_user_ids,
            to_user=request.user,
            action=Like.Action.LIKE,
        ).values_list('from_user_id', flat=True)

        users = User.objects.filter(id__in=mutual_user_ids)

        return Response(
            [
                {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
                for user in users
            ],
            status=status.HTTP_200_OK,
        )


class ProfileViewHistoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProfileViewHistory.objects.filter(
            viewer=self.request.user
        ).select_related(
            'viewed_profile',
            'viewed_profile__user',
        )

    def list(self, request, *args, **kwargs):
        history = self.get_queryset()

        data = [
            {
                'id': item.id,
                'profile_id': item.viewed_profile_id,
                'email': item.viewed_profile.user.email,
                'first_name': item.viewed_profile.user.first_name,
                'last_name': item.viewed_profile.user.last_name,
                'viewed_at': item.viewed_at,
            }
            for item in history
        ]

        return Response(data)




class DateInvitationListCreateView(generics.ListCreateAPIView):
    serializer_class = DateInvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DateInvitation.objects.filter(
            Q(from_user=self.request.user)
            | Q(to_user=self.request.user)
        ).select_related('from_user', 'to_user')

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class DateInvitationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = DateInvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DateInvitation.objects.filter(
            Q(from_user=self.request.user)
            | Q(to_user=self.request.user)
        )

    def update(self, request, *args, **kwargs):
        invitation = self.get_object()

        if invitation.to_user != request.user:
            raise PermissionDenied(
                'Изменять статус приглашения может только получатель.'
            )

        new_status = request.data.get('status')

        if new_status not in [
            DateInvitation.Status.ACCEPTED,
            DateInvitation.Status.DECLINED,
        ]:
            raise ValidationError(
                {'status': 'Укажите accepted или declined.'}
            )

        invitation.status = new_status
        invitation.save(update_fields=['status', 'updated_at'])

        return Response(
            self.get_serializer(invitation).data
        )
