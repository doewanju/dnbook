# Generated by Django 2.2.3 on 2019-10-31 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmap', '0018_auto_20191030_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookstore',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
