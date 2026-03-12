from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    
    Provides a structured representation of user data for API responses.
    """
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'is_active',
            'date_joined',
        )
        read_only_fields = ('id', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """
        Create a new user with the provided validated data.
        Ensures the password is hashed using set_password.
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """
        Update an existing user.
        If password is provided, hash it using set_password.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Authenticates a user with username and password,
    and returns the authentication token.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    
    def validate(self, data):
        """
        Authenticate the user with the provided credentials.
        """
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        
        data['user'] = user
        return data
    
    def create(self, validated_data):
        """
        Get or create the token for the authenticated user.
        """
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return {
            'token': token.key,
            'user': user,
        }


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.
    
    Deletes the user's authentication token.
    """
    pass
