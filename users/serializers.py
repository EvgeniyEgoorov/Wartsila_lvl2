from rest_framework import serializers

from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'age', 'city', 'created_at']
        read_only_fields = ['user']
