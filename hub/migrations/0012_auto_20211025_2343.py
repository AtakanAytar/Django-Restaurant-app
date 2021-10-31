# Generated by Django 3.2.8 on 2021-10-25 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0011_alter_qr_link_resolve_qr_code_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='session_id',
            field=models.CharField(default='none', max_length=50),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='session_id',
            field=models.CharField(default='none', max_length=50),
        ),
        migrations.AlterField(
            model_name='qr_link_resolve',
            name='qr_code_id',
            field=models.CharField(max_length=50),
        ),
    ]
