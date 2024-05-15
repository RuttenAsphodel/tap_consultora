# Generated by Django 5.0 on 2024-05-15 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='area',
            field=models.CharField(choices=[('Ejecutivo Telefonico', 'Ejecutivo Telefonico'), ('Soporte', 'Soporte'), ('Atencion al Cliente', 'Atencion al Cliente'), ('Soporte Nivel 2', 'Soporte Nivel 2')], max_length=255),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Solucionado', 'Solucionado'), ('Validado', 'Validado'), ('Cerrado', 'Cerrado')], default='Pendiente', max_length=255),
        ),
    ]