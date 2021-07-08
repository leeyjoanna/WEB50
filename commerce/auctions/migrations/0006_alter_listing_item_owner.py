# Generated by Django 3.2.3 on 2021-06-25 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_item_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='item_owner',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='item_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
