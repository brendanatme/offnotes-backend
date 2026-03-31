from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()


class SetupSuperuserView(View):
    def get(self, request):
        token = request.GET.get("token")
        if token != f"create-superuser-{request.get_host().split('.')[0]}":
            return JsonResponse({"error": "Invalid token"}, status=403)

        action = request.GET.get("action")

        if action == "test-db":
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    db_info = connection.settings_dict
                    return JsonResponse({
                        "status": "connected",
                        "engine": db_info["ENGINE"],
                        "name": db_info.get("NAME", "N/A"),
                    })
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=500)

        if User.objects.filter(is_superuser=True).exists():
            return JsonResponse({"message": "Superuser already exists"}, status=200)

        email = request.GET.get("email")
        password = request.GET.get("password")

        if not email or not password:
            return JsonResponse({"error": "email and password required"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "User with this email already exists"}, status=400)

        user = User.objects.create_superuser(email=email, password=password)
        return JsonResponse({"message": f"Superuser created: {user.email}"}, status=201)
