# Generated by Django 3.2.8 on 2021-10-28 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0014_branch_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch_info',
            name='latitude',
            field=models.FloatField(max_length=100),
        ),
        migrations.AlterField(
            model_name='branch_info',
            name='longtitute',
            field=models.FloatField(max_length=100),
        ),
    ]
