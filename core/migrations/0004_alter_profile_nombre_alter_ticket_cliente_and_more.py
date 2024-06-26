# Generated by Django 5.0.4 on 2024-06-27 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_profile_bio_remove_profile_birth_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nombre',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_creados', to='core.profile'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ejecutivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_asignados', to='core.profile'),
        ),
    ]
