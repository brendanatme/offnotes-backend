from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    
    Provides CRUD operations for users:
    - list: Get all users
    - create: Create a new user
    - retrieve: Get a specific user with their details
    - update: Update a user
    - partial_update: Partially update a user
    - destroy: Delete a user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
