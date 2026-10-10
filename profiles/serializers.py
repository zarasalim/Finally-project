
from datetime import date

from rest_framework import serializers

from .models import Profile, ProfilePhoto


class ProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhoto
        fields = [
            'id',
            'image',
            'is_main',
            'position',
            'uploaded_at',
        ]
        read_only_fields = ['id', 'uploaded_at']


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name',
        read_only=True,
    )
    last_name = serializers.CharField(
        source='user.last_name',
        read_only=True,
    )
    age = serializers.SerializerMethodField()
    photos = ProfilePhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'first_name',
            'last_name',
            'gender',
            'birth_date',
            'age',
            'city',
            'bio',
            'interests',
            'relationship_status',
            'is_profile_public',
            'photos',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'age',
            'created_at',
            'updated_at',
        ]

    def get_age(self, obj):
        if not obj.birth_date:
            return None

        today = date.today()
        age = today.year - obj.birth_date.year

        if (today.month, today.day) < (
            obj.birth_date.month,
            obj.birth_date.day,
        ):
            age -= 1

        return age
