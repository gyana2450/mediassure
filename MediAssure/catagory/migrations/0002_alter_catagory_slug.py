# Generated by Django 3.2.6 on 2021-08-16 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catagory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catagory',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
