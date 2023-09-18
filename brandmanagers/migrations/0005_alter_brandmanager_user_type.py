# Generated by Django 4.2.4 on 2023-09-15 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brandmanagers', '0004_brandmanager_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandmanager',
            name='user_type',
            field=models.CharField(choices=[('brand_manager', 'Brand Manager'), ('client', 'Client'), ('influencer', 'Influencer')], default='brand_manager', max_length=15),
        ),
    ]