# Generated by Django 3.2.8 on 2021-10-29 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0015_auto_20211028_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
