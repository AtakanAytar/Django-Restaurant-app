# Generated by Django 3.2.8 on 2021-10-23 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0007_auto_20211023_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qr_link_resolve',
            name='qr_code_id',
            field=models.CharField(max_length=50),
        ),
    ]
