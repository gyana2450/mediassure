# Generated by Django 3.2.6 on 2021-08-20 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210820_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_superuser',
        ),
        migrations.AddField(
            model_name='account',
            name='is_superadmin',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_admin',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
