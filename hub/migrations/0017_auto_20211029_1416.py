# Generated by Django 3.2.8 on 2021-10-29 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0016_orderitem_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='paid',
        ),
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]