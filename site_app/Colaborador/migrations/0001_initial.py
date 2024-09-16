# Generated by Django 5.1.1 on 2024-09-13 20:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Usuario", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Colaborador",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=255)),
                ("servicio", models.CharField(max_length=255)),
                ("monto", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "usuario_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Usuario.usuario",
                    ),
                ),
            ],
        ),
    ]
