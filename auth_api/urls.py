from django.urls import path
from .views import CsrfCookieView, SessionLoginView, SessionLogoutView, SessionStatusView

urlpatterns = [
    path("csrf", CsrfCookieView.as_view(), name="auth-csrf"),
    path("login", SessionLoginView.as_view(), name="auth-login"),
    path("logout", SessionLogoutView.as_view(), name="auth-logout"),
    path("session", SessionStatusView.as_view(), name="auth-session"),
]