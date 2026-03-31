from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model


User = get_user_model()


class CreateUserView(View):
    def get(self, request):
        token = request.GET.get("token")
        if token != f"create-user-{settings.CU_SECRET}":
            return JsonResponse({"error": "Invalid token"}, status=403)

        email = request.GET.get("email")
        password = request.GET.get("password")

        if not email or not password:
            return JsonResponse({"error": "email and password required"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"error": "User with this email already exists"}, status=400
            )

        user = User.objects.create_user(email, email=email, password=password)
        return JsonResponse({"message": f"User created: {user.email}"}, status=201)
