# Generated by Django 2.2 on 2019-04-22 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0007_auto_20190422_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accession',
            name='qualifier',
        ),
        migrations.AddField(
            model_name='verification',
            name='qualifier',
            field=models.CharField(blank=True, choices=[('aff.', 'aff.'), ('cf.', 'cf.'), ('forsan', 'forsan'), ('near', 'near'), ('?', '?'), (None, '')], max_length=8, null=True),
        ),
    ]
