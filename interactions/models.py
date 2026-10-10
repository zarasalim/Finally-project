
from django.conf import settings
from django.db import models


class Like(models.Model):
    class Action(models.TextChoices):
        LIKE = 'like', 'Лайк'
        DISLIKE = 'dislike', 'Дизлайк'

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_likes',
    )

    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_likes',
    )

    action = models.CharField(
        max_length=10,
        choices=Action.choices,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['from_user', 'to_user'],
                name='unique_user_like',
            ),
            models.CheckConstraint(
                condition=~models.Q(from_user=models.F('to_user')),
                name='no_self_like',
            ),
        ]

    def __str__(self):
        return (
            f'{self.from_user} -> {self.to_user}: '
            f'{self.action}'
        )

class ProfileViewHistory(models.Model):
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile_views',
    )

    viewed_profile = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='view_history',
    )

    viewed_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return (
            f'{self.viewer} посмотрел анкету '
            f'{self.viewed_profile.user}'
        )

class DateInvitation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает ответа'
        ACCEPTED = 'accepted', 'Принято'
        DECLINED = 'declined', 'Отклонено'

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_invitations',
    )

    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_invitations',
    )

    message = models.TextField(
        blank=True,
        max_length=1000,
    )

    proposed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(from_user=models.F('to_user')),
                name='no_self_invitation',
            ),
        ]

    def __str__(self):
        return (
            f'Приглашение от {self.from_user} '
            f'для {self.to_user}'
        )
