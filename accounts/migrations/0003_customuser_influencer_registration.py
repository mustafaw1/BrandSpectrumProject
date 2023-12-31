# Generated by Django 4.2.4 on 2023-09-01 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_customuser_is_brand_manager_customuser_is_influencer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='influencer_registration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
