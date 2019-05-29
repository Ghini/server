# Generated by Django 2.2 on 2019-05-29 19:31

import computed_property.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0012_auto_20190523_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxon',
            name='phonetic',
            field=computed_property.fields.ComputedCharField(compute_from='compute_phonetic_epithet', default='', editable=False, max_length=40),
        ),
    ]
