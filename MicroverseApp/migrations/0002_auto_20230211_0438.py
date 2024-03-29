# Generated by Django 3.2 on 2023-02-11 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MicroverseApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='national_ID',
            field=models.CharField(blank=True, max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=16, unique=True),
        ),
    ]
