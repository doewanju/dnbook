# Generated by Django 2.2.5 on 2019-09-27 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('others', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='culture',
            name='finish_time',
            field=models.DateTimeField(verbose_name='data published'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='start_time',
            field=models.DateTimeField(verbose_name='data published'),
        ),
    ]
