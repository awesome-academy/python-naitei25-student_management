from django.urls import path, include
from . import views

# from . import views
from school.views import auth_views

# Khai báo view tương ứng với url
urlpatterns = [
    path("", auth_views.index, name="class-list"),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    # Students
    path('students/', views.manage_students, name='manage_students'),
    path('students/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),

    # Teachers
    path('teachers/', views.manage_teachers, name='manage_teachers'),
    path('teachers/edit/<int:pk>/', views.edit_teacher, name='edit_teacher'),
    path('teachers/delete/<int:pk>/', views.delete_teacher, name='delete_teacher'),

    # Classes
    path('classes/', views.manage_classes, name='manage_classes'),
    path('classes/edit/<int:pk>/', views.edit_class, name='edit_class'),
    path('classes/delete/<int:pk>/', views.delete_class, name='delete_class'),

    # Class Students
    path('classes/students/', views.manage_class_students, name='manage_class_students'),
    path('classes/students/edit/<int:pk>/', views.edit_class_student, name='edit_class_student'),
    path('classes/students/delete/<int:pk>/', views.delete_class_student, name='delete_class_student'),

    # Class Teachers
    path('classes/teachers/', views.manage_class_teachers, name='manage_class_teachers'),
    path('classes/teachers/edit/<int:pk>/', views.edit_class_teacher, name='edit_class_teacher'),
    path('classes/teachers/delete/<int:pk>/', views.delete_class_teacher, name='delete_class_teacher'),
]
