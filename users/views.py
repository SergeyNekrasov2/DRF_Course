from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_permissions(self):
        """Позволяет пользователям изменять только свои данные"""
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializers):
        user = serializers.save(is_active=True)
        user.set_password(user.password)
        user.save()
