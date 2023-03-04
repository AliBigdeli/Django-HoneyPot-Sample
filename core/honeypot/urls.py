from django.urls import path, include,re_path
from . import views

app_name = "honeypot"

urlpatterns = [
    path("login/",views.LoginView.as_view(),name="login" ),
    re_path("^",views.RedirectToLogin.as_view()),
]
