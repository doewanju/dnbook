# Generated by Django 2.2.5 on 2019-10-01 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmap', '0005_auto_20190927_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookstore',
            name='id',
        ),
        migrations.AddField(
            model_name='bookstore',
            name='bookstore_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bookstore',
            name='name',
            field=models.CharField(default='storename', max_length=20),
        ),
    ]
