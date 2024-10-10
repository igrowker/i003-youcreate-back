# Generated by Django 5.1.1 on 2024-10-10 14:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Colaborador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagoColaborador',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_pago', models.DateField()),
                ('descripcion', models.TextField(null=True)),
                ('metodo_pago', models.CharField(max_length=50)),
                ('colaborador_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Colaborador.colaborador')),
            ],
        ),
    ]
