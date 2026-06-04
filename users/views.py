from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import LoginSerializer, LogoutSerializer, SignupSerializer


@extend_schema(
    request=LoginSerializer,
    responses={
        200: LoginSerializer,
        400: {'description': 'Invalid username or password'}
    },
    examples=[
        OpenApiExample(
            'Login Request',
            value={
                'username': 'john_doe',
                'password': 'secure_password123'
            }
        ),
        OpenApiExample(
            'Login Response',
            value={
                'token': 'abc123token456',
                'user': {
                    'id': 1,
                    'username': 'john_doe',
                    'email': 'john@example.com',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'is_active': True,
                    'date_joined': '2024-01-15T10:30:00Z'
                }
            },
            response_only=True
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    User login endpoint.
    
    Authenticates a user with their username and password, and returns
    an authentication token for subsequent API requests.
    
    Accepts:
    - username (str): The user's username
    - password (str): The user's password
    
    Returns:
    - token (str): The authentication token for subsequent requests
    - user (dict): The authenticated user's details
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        result = serializer.save()
        return Response(
            {
                'token': result['token'],
                'user': LoginSerializer(serializer.validated_data).data,
            },
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={200: {'description': 'Successfully logged out'}},
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    User logout endpoint.
    
    Deletes the user's authentication token, effectively logging them out.
    
    Requires:
    - Authentication token in the Authorization header
    """
    try:
        request.user.auth_token.delete()
        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    request=SignupSerializer,
    responses={
        201: SignupSerializer,
        400: {'description': 'Validation error'},
        404: {'description': 'Signup is disabled'},
    },
    examples=[
        OpenApiExample(
            'Signup Request',
            value={
                'username': 'john_doe',
                'email': 'john@example.com',
                'password': 'secure_password123',
            }
        ),
        OpenApiExample(
            'Signup Response',
            value={
                'token': 'abc123token456',
                'user': {
                    'id': 1,
                    'username': 'john_doe',
                    'email': 'john@example.com',
                    'first_name': '',
                    'last_name': '',
                    'is_active': True,
                    'date_joined': '2024-01-15T10:30:00Z',
                }
            },
            response_only=True
        ),
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    User signup endpoint.

    Creates a new user account and returns an authentication token.
    Disabled unless the SIGNUP_ENABLED environment variable is set to true.

    Accepts:
    - username (str): The desired username
    - email (str): The user's email address
    - password (str): The desired password (validated against AUTH_PASSWORD_VALIDATORS)

    Returns:
    - token (str): The authentication token for subsequent requests
    - user (dict): The newly created user's details
    """
    if not settings.SIGNUP_ENABLED:
        return Response(
            {'error': 'Not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        result = serializer.save()
        return Response(
            {
                'token': result['token'],
                'user': SignupSerializer(serializer.validated_data).data,
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
