from django.urls import path
from . import views

# Khai báo view tương ứng với url
urlpatterns = [
    path("", views.index, name="index"),
    path("school/", views.index, name="index"),
]
