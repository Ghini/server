# Generated by Django 2.2 on 2019-04-21 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0006_auto_20190421_2103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rank',
            old_name='shows_as',
            new_name='show_as',
        ),
    ]
