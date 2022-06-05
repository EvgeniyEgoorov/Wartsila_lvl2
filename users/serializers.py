from rest_framework import serializers

from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = Profile.objects.create_user(
            validated_data.pop('login'),
            validated_data.pop('password'),
            **validated_data
        )
        return user

    class Meta:
        model = Profile
        fields = ['id', 'login', 'password', 'bio', 'created_at']




