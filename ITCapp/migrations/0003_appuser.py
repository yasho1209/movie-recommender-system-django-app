# Generated by Django 4.2.6 on 2023-11-06 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ITCapp", "0002_rename_student_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="AppUser",
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
                ("username", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=20)),
                ("name", models.CharField(max_length=20)),
                ("email", models.CharField(max_length=20)),
                ("country", models.CharField(max_length=20)),
                ("age", models.CharField(max_length=20)),
            ],
        ),
    ]
