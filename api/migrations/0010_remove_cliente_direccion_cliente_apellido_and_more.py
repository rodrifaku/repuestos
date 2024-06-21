# Generated by Django 5.0.6 on 2024-06-21 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_detalleventa_estado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='direccion',
        ),
        migrations.AddField(
            model_name='cliente',
            name='apellido',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='rut',
            field=models.CharField(default=1, max_length=12, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(max_length=15),
        ),
    ]