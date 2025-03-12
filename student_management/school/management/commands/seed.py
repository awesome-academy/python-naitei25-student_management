import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from school.models import (
    Student,
    Teacher,
    Subject,
    Class,
    Semester,
    Classification,
    Grade,
    ClassStudent,
    ClassTeacher,
)


class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding data..."))

        # Tạo 2 admin
        admin1 = Teacher.objects.create(
            username=f"viethoan@gmail.com",
            first_name=f"Việt",
            last_name=f"Hoàn",
            phone=f"0111222333",
            role="admin",
        )
        admin1.set_password("matkhau")
        admin1.save()

        admin2 = Teacher.objects.create(
            username=f"minhquan@gmail.com",
            password="matkhau",
            first_name=f"Minh",
            last_name=f"Quân",
            phone=f"0444555666",
            role="admin",
        )
        admin2.set_password("matkhau")
        admin2.save()

        # Tạo 10 giáo viên
        teachers = []
        for i in range(10):
            teacher = Teacher.objects.create(
                username=f"giaovien{i}@gmail.com",
                first_name=f"Giáo{i}",
                last_name=f"Viên{i}",
                phone=f"012345678{i}",
                role="teacher",
            )
            teacher.set_password("matkhau")
            teacher.save()
            teachers.append(teacher)

        # Tạo 15 học sinh
        students = []
        for i in range(15):
            student = Student.objects.create(
                first_name=f"Học{i}",
                last_name=f"Sinh{i}",
                birth_day=f"2005-07-{i+1}",
                phone=f"09876543{i}",
                email=f"hocsinh{i}@school.com",
                address="Hanoi",
            )
            students.append(student)

        # Tạo 6 môn học
        subjects = []
        for name in ["Toán", "Ngữ Văn", "Tiếng Anh", "Vật Lý", "Hóa Học", "Sinh Học"]:
            subject = Subject.objects.create(name=name)
            subjects.append(subject)

        # Tạo 3 lớp học
        classes = []
        for i in range(3):
            class_obj = Class.objects.create(name=f"Lớp A{i+1}(23-26)")
            classes.append(class_obj)

        # Tạo 4 học kỳ
        semesters = []
        semester1 = Semester.objects.create(
            name=f"Kỳ 1 năm 2023", start_date="2023-09-05", end_date="2024-01-15"
        )
        semester2 = Semester.objects.create(
            name=f"Kỳ 2 năm 2023", start_date="2024-01-16", end_date="2024-05-01"
        )
        semester3 = Semester.objects.create(
            name=f"Kỳ 1 năm 2024", start_date="2024-09-05", end_date="2025-01-15"
        )
        semester4 = Semester.objects.create(
            name=f"Kỳ 2 năm 2024", start_date="2025-01-16", end_date="2025-05-01"
        )

        semesters.extend([semester1, semester2, semester3])

        # Gán giáo viên vào lớp
        for cls in classes:
            for semester in semesters:
                teacher_indexs = list(range(10))
                random_number = random.randint(0, len(teacher_indexs) - 1)
                teacher_index = teacher_indexs.pop(random_number)
                teacher = teachers[teacher_index]
                is_homeroom = False
                if len(teacher_indexs) == 10:
                    is_homeroom = True

                for subject in subjects:
                    ClassTeacher.objects.create(
                        classroom=cls,
                        semester=semester,
                        subject=subject,
                        teacher=teacher,
                        is_homeroom=is_homeroom,
                    )

        # Gán học sinh vào lớp
        for student in students:
            class_student = random.choice(classes)
            # Các kỳ trước
            for semester in semesters:
                ClassStudent.objects.create(
                    classroom=class_student,
                    student=student,
                    semester=semester,
                    late_time=random.randint(0, 3),
                    absent_time=random.randint(0, 3),
                    excused_time=random.randint(0, 3),
                )

            # Kỳ hiện tại
            ClassStudent.objects.create(
                classroom=class_student,
                student=student,
                semester=semester4,
            )

        # Thêm điểm cho mỗi học sinh
        for student in students:
            for semester in semesters:
                for subject in subjects:
                    Grade.objects.update_or_create(
                        student=student,
                        semester=semester,
                        subject=subject,
                        defaults={
                            "oral_score": Decimal(str(round(random.uniform(5, 10), 2))),
                            "fifteen_min_score": Decimal(
                                str(round(random.uniform(5, 10), 2))
                            ),
                            "one_period_score": Decimal(
                                str(round(random.uniform(5, 10), 2))
                            ),
                            "midterm_score": Decimal(
                                str(round(random.uniform(5, 10), 2))
                            ),
                            "final_score": Decimal(
                                str(round(random.uniform(5, 10), 2))
                            ),
                        },
                    )

        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
