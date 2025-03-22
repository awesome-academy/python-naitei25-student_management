from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .constants import (
    NAME_MAX_LENGTH,
    CHAR_MAX_LENGTH,
    PHONE_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    CLASS_MAX_LENGTH,
    RANK_MAX_LENGTH,
    SUBJECT_MAX_LENGTH,
    TIME_DEFAULT,
    ROLE_MAX_LENGTH,
    Role,
    SCORE_MAX_DIGITS,
    SCORE_DECIMAL_PLACES,
    HOMEROOM_DEFAULT,
    AttendanceStatus,
    STATUS_MAX_LENGTH,
)


# Create your models here.
# Học sinh
class Student(models.Model):
    first_name = models.CharField(max_length=NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=NAME_MAX_LENGTH)
    birth_day = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="images/", null=True, blank=True)
    phone = models.CharField(max_length=PHONE_MAX_LENGTH)
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True)
    address = models.TextField(null=True, blank=True)


# Giáo viên
class Teacher(AbstractUser):
    username = models.EmailField(
        max_length=EMAIL_MAX_LENGTH, unique=True, default="username"
    )
    password = models.CharField(max_length=CHAR_MAX_LENGTH)
    first_name = models.CharField(max_length=NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=NAME_MAX_LENGTH)
    birth_day = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="images/", null=True, blank=True)
    phone = models.CharField(max_length=PHONE_MAX_LENGTH, unique=True)
    address = models.TextField(null=True, blank=True)

    ROLE_CHOICES = [
        (Role.TEACHER.value, "Giáo viên"),
        (Role.ADMIN.value, "Quản trị viên"),
    ]

    role = models.CharField(
        max_length=ROLE_MAX_LENGTH, choices=ROLE_CHOICES, default=Role.TEACHER.value
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "role",
    ]

    def save(self, *args, **kwargs):
        if self.role == Role.ADMIN.value:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)


# Lớp học
class Class(models.Model):
    name = models.CharField(max_length=CLASS_MAX_LENGTH)


# Kỳ học
class Semester(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


# Môn học
class Subject(models.Model):
    name = models.CharField(max_length=SUBJECT_MAX_LENGTH)


# Lớp - Học sinh
class ClassStudent(models.Model):
    classroom = models.ForeignKey(Class, on_delete=models.PROTECT)
    semester = models.ForeignKey(
        Semester,
        on_delete=models.SET_NULL,
        null=True,
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    late_time = models.IntegerField(default=TIME_DEFAULT)  # Số lần đi muộn
    absent_time = models.IntegerField(
        default=TIME_DEFAULT
    )  # Số lần vắng mặt không phép
    excused_time = models.IntegerField(default=TIME_DEFAULT)  # Số lần vắng mặt có phép

    class Meta:
        unique_together = ("classroom", "student", "semester")


# Lớp - Giáo viên
class ClassTeacher(models.Model):
    classroom = models.ForeignKey(Class, on_delete=models.PROTECT)
    semester = models.ForeignKey(
        Semester,
        on_delete=models.SET_NULL,
        null=True,
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    is_homeroom = models.BooleanField(
        default=HOMEROOM_DEFAULT
    )  # Là giáo viên chủ nhiệm ?

    class Meta:
        unique_together = ("classroom", "semester", "subject")
        constraints = [
            models.UniqueConstraint(
                fields=["classroom", "semester"],
                condition=models.Q(is_homeroom=True),
                name="unique_homeroom_per_class_per_semester",
            )
        ]

    def clean(self):
        """Đảm bảo mỗi lớp chỉ có một giáo viên chủ nhiệm."""
        if self.is_homeroom:
            existing_homeroom = ClassTeacher.objects.filter(
                classroom=self.classroom, semester=self.semester, is_homeroom=True
            ).exclude(pk=self.pk)

            if existing_homeroom.exists():
                raise ValidationError(_("Mỗi lớp chỉ được có một giáo viên chủ nhiệm."))

        # Kiểm tra giáo viên phải có role là "teacher"
        if self.teacher.role != "teacher":
            raise ValidationError(
                _("Chỉ có giáo viên mới có thể được chỉ định vào lớp học.")
            )

    def save(self, *args, **kwargs):
        """Kiểm tra ràng buộc trước khi lưu."""
        self.clean()
        super().save(*args, **kwargs)


# Điểm danh
class Attendance(models.Model):
    classstudent = models.ForeignKey(ClassStudent, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = [
        (AttendanceStatus.PRESENT.value, "Có mặt"),
        (AttendanceStatus.LATE.value, "Đi muộn"),
        (AttendanceStatus.EXCUSED.value, "Nghỉ có phép"),
        (AttendanceStatus.ABSENT.value, "Nghỉ không phép"),
    ]
    status = models.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=AttendanceStatus.PRESENT.value,
    )

    class Meta:
        unique_together = ("classstudent", "date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_classstudent_attendance()

    def update_classstudent_attendance(self):
        classstudent = self.classstudent

        classstudent.late_time = Attendance.objects.filter(
            classstudent=classstudent, status="late"
        ).count()

        classstudent.absent_time = Attendance.objects.filter(
            classstudent=classstudent, status="absent"
        ).count()

        classstudent.excused_time = Attendance.objects.filter(
            classstudent=classstudent, status="excused"
        ).count()

        classstudent.save()


# Điểm số môn học
class Grade(models.Model):
    classstudent = models.ForeignKey(ClassStudent, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    oral_score = models.DecimalField(
        max_digits=SCORE_MAX_DIGITS,
        decimal_places=SCORE_DECIMAL_PLACES,
        null=True,
        blank=True,
    )  # Điểm miệng
    fifteen_min_score = models.DecimalField(
        max_digits=SCORE_MAX_DIGITS,
        decimal_places=SCORE_DECIMAL_PLACES,
        null=True,
        blank=True,
    )  # Điểm 15p
    one_period_score = models.DecimalField(
        max_digits=SCORE_MAX_DIGITS,
        decimal_places=SCORE_DECIMAL_PLACES,
        null=True,
        blank=True,
    )  # Điểm 1 tiết
    midterm_score = models.DecimalField(
        max_digits=SCORE_MAX_DIGITS,
        decimal_places=SCORE_DECIMAL_PLACES,
        null=True,
        blank=True,
    )  # Điểm giữa kỳ
    final_score = models.DecimalField(
        max_digits=SCORE_MAX_DIGITS,
        decimal_places=SCORE_DECIMAL_PLACES,
        null=True,
        blank=True,
    )  # Điểm cuối kỳ
    final_grade = models.DecimalField(
        max_digits=SCORE_MAX_DIGITS,
        decimal_places=SCORE_DECIMAL_PLACES,
        null=True,
        blank=True,
    )  # Điểm tổng kết môn học

    class Meta:
        unique_together = ("classstudent", "subject")


# Xếp loại
class Classification(models.Model):
    classstudent = models.ForeignKey(ClassStudent, on_delete=models.CASCADE, null=True)
    gpa = models.DecimalField(
        max_digits=SCORE_MAX_DIGITS,
        decimal_places=SCORE_DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    rank = models.CharField(max_length=RANK_MAX_LENGTH, null=True, blank=True)


# Tạo bảng điểm cho học sinh khi được thêm vào lớp
@receiver(post_save, sender=ClassStudent)
def create_student_grades(sender, instance, created, **kwargs):
    if created:
        subjects = Subject.objects.all()
        for subject in subjects:
            Grade.objects.create(
                classstudent=instance,
                subject=subject,
            )


# Cập nhật điểm tb môn
@receiver(post_save, sender=Grade)
def update_final_grade(sender, instance, **kwargs):
    if all(
        [
            instance.oral_score is not None,
            instance.fifteen_min_score is not None,
            instance.one_period_score is not None,
            instance.midterm_score is not None,
            instance.final_score is not None,
        ]
    ):
        new_final_grade = (
            instance.oral_score * Decimal("0.1")
            + instance.fifteen_min_score * Decimal("0.1")
            + instance.one_period_score * Decimal("0.2")
            + instance.midterm_score * Decimal("0.3")
            + instance.final_score * Decimal("0.3")
        )

        if instance.final_grade != new_final_grade:
            instance.final_grade = new_final_grade
            instance.save(update_fields=["final_grade"])


# Cập nhật gpa và xếp loại
@receiver([post_save, post_delete], sender=Grade)
def update_gpa(sender, instance, **kwargs):
    # Tổng số môn học trong học kỳ này
    total_subjects = Grade.objects.filter(classstudent=instance.classstudent).count()

    # Số môn học đã có final_score
    subjects_with_score = (
        Grade.objects.filter(classstudent=instance.classstudent)
        .exclude(final_score=None)
        .count()
    )

    # Cập nhật khi đã có hết điểm
    if total_subjects == subjects_with_score and total_subjects > 0:
        avg_gpa = (
            Grade.objects.filter(classstudent=instance.classstudent).aggregate(
                avg_gpa=models.Avg("final_grade")
            )["avg_gpa"]
            or 0
        )

        rank = ""
        if avg_gpa >= 8.5:
            rank = "Giỏi"
        elif avg_gpa >= 7:
            rank = "Khá"
        elif avg_gpa >= 5:
            rank = "Trung bình"
        elif avg_gpa > 0:
            rank = "Yếu"

        classification, created = Classification.objects.update_or_create(
            classstudent=instance.classstudent,
            defaults={"gpa": avg_gpa, "rank": rank},
        )

        if not created:
            classification.save()
