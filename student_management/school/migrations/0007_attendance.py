# Generated by Django 5.1.7 on 2025-03-21 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school", "0006_alter_teacher_is_staff_alter_teacher_is_superuser"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("present", "Có mặt"),
                            ("late", "Đi muộn"),
                            ("excused", "Nghỉ có phép"),
                            ("absent", "Nghỉ không phép"),
                        ],
                        default="present",
                        max_length=10,
                    ),
                ),
                (
                    "classstudent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="school.classstudent",
                    ),
                ),
            ],
            options={
                "unique_together": {("classstudent", "date")},
            },
        ),
    ]
