from django.urls import path, include

# from . import views
from school.views import auth_views, teacher_view

# Khai báo view tương ứng với url
urlpatterns = [
    path("", teacher_view.ClassListView.as_view(), name="class-list"),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    path(
        "class/<int:class_id>/semester/<int:semester_id>/",
        teacher_view.StudentListView.as_view(),
        name="student-list",
    ),
]
