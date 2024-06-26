# Generated by Django 5.0.4 on 2024-06-21 15:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_area', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Criticidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_criticidad', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_ticket', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_ticket', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.TextField()),
                ('observaciones', models.TextField(blank=True)),
                ('area', models.ForeignKey(default='Ejecutivo Telefonico', on_delete=django.db.models.deletion.CASCADE, to='core.area', verbose_name='Area')),
                ('criticidad', models.ForeignKey(default='Media', on_delete=django.db.models.deletion.CASCADE, to='core.criticidad', verbose_name='Criticidad')),
                ('estado', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.estado', verbose_name='Estado')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('tipo', models.ForeignKey(default='Solicitud', on_delete=django.db.models.deletion.CASCADE, to='core.tipo', verbose_name='Tipo')),
            ],
        ),
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(blank=True, max_length=255, verbose_name='Comentario')),
                ('fecha_comentario', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contrasena', models.CharField(max_length=255)),
                ('rol', models.CharField(choices=[('Administrador', 'Administrador'), ('Ejecutivo', 'Ejecutivo'), ('Cliente', 'Cliente')], max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('group', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auth.group', verbose_name='Rol')),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_creados', to='core.usuario'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ejecutivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_asignados', to='core.usuario'),
        ),
    ]
