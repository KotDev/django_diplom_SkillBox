from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError


from accounts.models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = ["src", "alt"]


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)

    def validate(self, attrs):
        cur_password = attrs.get('currentPassword')
        if self.instance.check_password(cur_password):
            return attrs
        else:
            raise ValidationError('Incorrect password')

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('newPassword'))
        instance.save()
        return instance

