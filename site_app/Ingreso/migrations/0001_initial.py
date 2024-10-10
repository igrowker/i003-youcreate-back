# Generated by Django 5.1.1 on 2024-10-10 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingreso',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('origen', models.CharField(max_length=255)),
                ('fecha', models.DateField()),
            ],
        ),
    ]
