# Generated by Django 4.2.20 on 2025-03-20 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud_escolar_api', '0003_usuario_delete_administradores'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
