# Generated by Django 5.1.1 on 2024-10-11 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='otp_secret',
            field=models.CharField(blank=True, default=None, max_length=16, null=True),
        ),
    ]
