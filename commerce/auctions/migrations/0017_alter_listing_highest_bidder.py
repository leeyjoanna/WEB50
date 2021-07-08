# Generated by Django 3.2.3 on 2021-06-29 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_alter_listing_highest_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='highest_bidder',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, related_name='highest_bidder', to=settings.AUTH_USER_MODEL),
        ),
    ]
