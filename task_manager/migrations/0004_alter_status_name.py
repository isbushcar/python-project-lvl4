# Generated by Django 3.2.4 on 2021-09-05 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0003_alter_status_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
