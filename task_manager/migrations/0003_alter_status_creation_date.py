# Generated by Django 3.2.4 on 2021-09-05 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0002_rename_status_name_status_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
