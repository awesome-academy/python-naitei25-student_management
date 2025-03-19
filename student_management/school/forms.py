from django import forms
from .models import Student, Teacher, Class, ClassStudent, ClassTeacher


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'birth_day', 'avatar', 'phone', 'email', 'address']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'birth_day', 'avatar', 'phone', 'email', 'address', 'role']


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']


class ClassStudentForm(forms.ModelForm):
    class Meta:
        model = ClassStudent
        fields = ['classroom', 'semester', 'student', 'late_time', 'absent_time', 'excused_time']


class ClassTeacherForm(forms.ModelForm):
    class Meta:
        model = ClassTeacher
        fields = ['classroom', 'semester', 'teacher', 'is_homeroom', 'can_manage']
