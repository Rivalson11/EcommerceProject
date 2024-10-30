from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.redirect_to_login, name='root_redirect'),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
