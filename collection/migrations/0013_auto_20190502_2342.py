# Generated by Django 2.2 on 2019-05-02 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0012_auto_20190424_1525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verification',
            old_name='code',
            new_name='seq',
        ),
        migrations.AlterUniqueTogether(
            name='verification',
            unique_together={('accession', 'seq')},
        ),
    ]