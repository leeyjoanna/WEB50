# Generated by Django 3.2.3 on 2021-06-25 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_item_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='item_owner',
        ),
    ]
