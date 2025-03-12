from django.shortcuts import render


# Create your views here.
def index(request):

    context = {
        "teacher_name": "Việt Hoàn",
        "teacher_email": "viethoan557723@gmail.comoan557723@gmail",
        "is_homeroom_teacher": True,
        "is_subject_teacher": True,
        "language": "Tiếng Việt",
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)
