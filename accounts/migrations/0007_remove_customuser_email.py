# Generated by Django 4.2.4 on 2023-09-01 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_customuser_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='email',
        ),
    ]
