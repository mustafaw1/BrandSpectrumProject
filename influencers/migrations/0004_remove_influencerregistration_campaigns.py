# Generated by Django 4.2.4 on 2023-09-06 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('influencers', '0003_influencerregistration_campaigns'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='influencerregistration',
            name='campaigns',
        ),
    ]