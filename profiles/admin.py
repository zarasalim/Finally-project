from django.contrib import admin

from .models import Profile, ProfilePhoto


class ProfilePhotoInline(admin.TabularInline):
    model = ProfilePhoto
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'gender',
        'birth_date',
        'city',
        'relationship_status',
        'is_profile_public',
    )

    search_fields = (
        'user__email',
        'city',
    )

    list_filter = (
        'gender',
        'relationship_status',
        'is_profile_public',
    )

    inlines = [ProfilePhotoInline]