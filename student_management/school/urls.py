from django.urls import path, include

# from . import views
from school.views import auth_views, teacher_view, action_views

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
    path(
        "student/<int:pk>",
        teacher_view.StudentDetailView.as_view(),
        name="student-detail",
    ),
    path(
        "class/<int:class_id>/semester/<int:semester_id>/attendances",
        teacher_view.AttendancesView.as_view(),
        name="attendance-tracking",
    ),
    path(
        "attendance/tracking/",
        action_views.post_attendance,
        name="tracking",
    ),
    path(
        "class/<int:class_id>/semester/<int:semester_id>/subject/<int:subject_id>",
        teacher_view.GradeView.as_view(),
        name="grade",
    ),
    path(
        "grade/update/",
        action_views.post_grade,
        name="grade-update",
    ),
]
