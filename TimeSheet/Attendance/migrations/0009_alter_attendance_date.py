# Generated by Django 4.1.4 on 2023-01-13 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0008_alter_attendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
