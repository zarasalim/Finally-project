
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'male', 'Мужской'
        FEMALE = 'female', 'Женский'
        OTHER = 'other', 'Другой'

    class RelationshipStatus(models.TextChoices):
        SINGLE = 'single', 'Свободен'
        DATING = 'dating', 'Встречается'
        COMPLICATED = 'complicated', 'Всё сложно'
        PRIVATE = 'private', 'Не указано'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        blank=True,
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    bio = models.TextField(
        blank=True,
    )

    interests = models.JSONField(
        default=list,
        blank=True,
    )

    relationship_status = models.CharField(
        max_length=20,
        choices=RelationshipStatus.choices,
        default=RelationshipStatus.SINGLE,
    )

    is_profile_public = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'Профиль: {self.user.email}'




class ProfilePhoto(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='photos',
    )

    image = models.ImageField(
        upload_to='profile_photos/',
    )

    is_main = models.BooleanField(
        default=False,
    )

    position = models.PositiveIntegerField(
        default=0,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['position', 'id']

    def save(self, *args, **kwargs):
        if self.is_main:
            ProfilePhoto.objects.filter(
                profile=self.profile,
                is_main=True,
            ).exclude(pk=self.pk).update(is_main=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Фото профиля {self.profile.user.email}'


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)



@receiver(post_delete, sender=ProfilePhoto)
def delete_profile_photo_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)