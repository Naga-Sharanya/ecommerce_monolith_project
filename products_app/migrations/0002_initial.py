# Generated by Django 5.1.4 on 2025-02-14 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products_app', '0001_initial'),
        ('usermanagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanagement.user'),
        ),
    ]
