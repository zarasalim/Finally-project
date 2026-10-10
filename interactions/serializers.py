
from rest_framework import serializers

from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    from_user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Like
        fields = [
            'id',
            'from_user',
            'to_user',
            'action',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'from_user',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        to_user = attrs.get('to_user')

        if request and to_user == request.user:
            raise serializers.ValidationError(
                'Нельзя оценивать собственную анкету.'
            )

        return attrs



from .models import DateInvitation


class DateInvitationSerializer(serializers.ModelSerializer):
    from_user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    status = serializers.ChoiceField(
        choices=DateInvitation.Status.choices,
        read_only=True,
    )

    class Meta:
        model = DateInvitation
        fields = [
            'id',
            'from_user',
            'to_user',
            'message',
            'proposed_at',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'from_user',
            'status',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        to_user = attrs.get('to_user')

        if request and to_user == request.user:
            raise serializers.ValidationError(
                'Нельзя отправить приглашение самому себе.'
            )

        if request and to_user:
            from .models import Like

            mutual_like = (
                Like.objects.filter(
                    from_user=request.user,
                    to_user=to_user,
                    action=Like.Action.LIKE,
                ).exists()
                and Like.objects.filter(
                    from_user=to_user,
                    to_user=request.user,
                    action=Like.Action.LIKE,
                ).exists()
            )

            if not mutual_like:
                raise serializers.ValidationError(
                    'Приглашение можно отправить только при взаимном лайке.'
                )

        return attrs
