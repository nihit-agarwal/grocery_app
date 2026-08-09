from django.urls import path
from .views import CsrfCookieView, SessionLoginView, SessionLogoutView, SessionSignupView, SessionStatusView

urlpatterns = [
    path("csrf", CsrfCookieView.as_view(), name="auth-csrf"),
    path("login", SessionLoginView.as_view(), name="auth-login"),
    path("logout", SessionLogoutView.as_view(), name="auth-logout"),
    path("signup", SessionSignupView.as_view(), name="auth-signup"),
    path("session", SessionStatusView.as_view(), name="auth-session"),
]