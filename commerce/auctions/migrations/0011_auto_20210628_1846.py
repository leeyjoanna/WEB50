# Generated by Django 3.2.3 on 2021-06-28 18:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_item_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='item_description',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='listing',
            name='item_name',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='listing',
            name='item_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='item_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000)),
                ('comment_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_item', to='auctions.listing')),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
