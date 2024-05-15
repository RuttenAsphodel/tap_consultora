# Generated by Django 5.0.4 on 2024-05-14 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_usuario_rol'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]