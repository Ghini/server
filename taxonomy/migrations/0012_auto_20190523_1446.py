# Generated by Django 2.2 on 2019-05-23 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0011_auto_20190516_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rank',
            name='short',
            field=models.CharField(blank=True, max_length=8),
        ),
    ]