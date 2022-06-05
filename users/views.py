from rest_framework.viewsets import ModelViewSet

from users.models import Profile
from users.permissions import IsOwnerOrReadOnly
from users.serializers import ProfileSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]




