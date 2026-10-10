
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Profile, ProfilePhoto
from .serializers import ProfileSerializer, ProfilePhotoSerializer



import random
from datetime import date

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, ProfilePhoto
from .serializers import ProfileSerializer, ProfilePhotoSerializer
from interactions.models import ProfileViewHistory
from rest_framework.response import Response

class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Profile.objects.filter(
            is_profile_public=True
        ).exclude(
            user=self.request.user
            if self.request.user.is_authenticated
            else None
        ).select_related(
            'user'
        ).prefetch_related('photos')

        city = self.request.query_params.get('city')
        gender = self.request.query_params.get('gender')
        status = self.request.query_params.get('relationship_status')
        min_age = self.request.query_params.get('min_age')
        max_age = self.request.query_params.get('max_age')

        if city:
            queryset = queryset.filter(city__icontains=city)

        if gender:
            queryset = queryset.filter(gender=gender)

        if status:
            queryset = queryset.filter(relationship_status=status)

        today = date.today()

        if min_age:
            try:
                min_age = int(min_age)
                latest_birth_date = date(
                    today.year - min_age,
                    today.month,
                    min(today.day, 28) if today.month == 2 else today.day,
                )
                queryset = queryset.filter(
                    birth_date__lte=latest_birth_date
                )
            except ValueError:
                pass

        if max_age:
            try:
                max_age = int(max_age)
                earliest_birth_date = date(
                    today.year - max_age - 1,
                    today.month,
                    min(today.day, 28) if today.month == 2 else today.day,
                )
                queryset = queryset.filter(
                    birth_date__gt=earliest_birth_date
                )
            except ValueError:
                pass

        return queryset


class RandomProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.filter(
            is_profile_public=True
        ).exclude(
            user=request.user
        ).exclude(
            birth_date__isnull=True
        ).select_related(
            'user'
        ).prefetch_related('photos')

        profiles = list(profiles)

        if not profiles:
            return Response(
                {'detail': 'Пока нет доступных анкет.'},
                status=200,
            )

        profile = random.choice(profiles)

        serializer = ProfileSerializer(
            profile,
            context={'request': request},
        )

        return Response(serializer.data)




class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Profile.objects.filter(
            is_profile_public=True
        ).select_related(
            'user'
        ).prefetch_related('photos')

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()

        if (
            request.user.is_authenticated
            and request.user != profile.user
        ):
            ProfileViewHistory.objects.create(
                viewer=request.user,
                viewed_profile=profile,
            )

        serializer = self.get_serializer(profile)
        return Response(serializer.data)



class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        return profile


class MyPhotoListCreateView(generics.ListCreateAPIView):
    serializer_class = ProfilePhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        return ProfilePhoto.objects.filter(
            profile=profile
        )

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        serializer.save(profile=profile)


class MyPhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfilePhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        return ProfilePhoto.objects.filter(
            profile=profile
        )
