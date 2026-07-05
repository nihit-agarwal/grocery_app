from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class CsrfCookieView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({"detail": "CSRF cookie set"}, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name="dispatch")
class SessionLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"detail": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        auth_login(request, user)
        return Response(
            {"detail": "Login successful", "user": {"id": user.id, "username": user.username}},
            status=status.HTTP_200_OK,
        )


@method_decorator(csrf_protect, name="dispatch")
class SessionLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth_logout(request)
        return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)


class SessionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"authenticated": True, "user": {"id": request.user.id, "username": request.user.username}},
            status=status.HTTP_200_OK,
        )