# Generated by Django 2.2.3 on 2019-10-30 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_normalprofile_profileimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='bossprofile',
            name='profileimg',
            field=models.ImageField(blank=True, null=True, upload_to='profileimg/'),
        ),
    ]
