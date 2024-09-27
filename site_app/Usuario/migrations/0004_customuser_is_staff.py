# Generated by Django 5.1.1 on 2024-09-21 03:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "Usuario",
            "0003_remove_customuser_email_remove_customuser_first_name_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_staff",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether the user can log into this admin site.",
                verbose_name="staff status",
            ),
        ),
    ]
