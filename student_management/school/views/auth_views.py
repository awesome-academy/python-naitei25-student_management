from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _

from ..constants import Role


def index(request):

    context = {
        "language": "Tiếng Việt",
    }

    return render(request, "index.html", context=context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == Role.TEACHER.value:
                return redirect("class-list")
            elif user.role == Role.ADMIN.value:
                return redirect("/admin/")
        else:
            error = _("Email hoặc mật khẩu không đúng!")

    return render(
        request,
        "school/registration/login.html",
        {"error": error if "error" in locals() else None},
    )


def logout_view(request):
    logout(request)
    return redirect("login")
