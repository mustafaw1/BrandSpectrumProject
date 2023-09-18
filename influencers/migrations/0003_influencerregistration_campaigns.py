# Generated by Django 4.2.4 on 2023-09-05 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
        ('influencers', '0002_remove_influencerregistration_campaigns'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencerregistration',
            name='campaigns',
            field=models.ManyToManyField(blank=True, related_name='influencers', to='campaigns.campaign'),
        ),
    ]
