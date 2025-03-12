from django.urls import path, include

# from . import views
from school.views import auth_views

# Khai báo view tương ứng với url
urlpatterns = [
    path("", auth_views.index, name="class-list"),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
]
