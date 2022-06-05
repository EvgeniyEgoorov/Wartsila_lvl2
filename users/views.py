from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Profile
from users.permissions import IsOwnerOrReadOnly
from users.serializers import ProfileSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
