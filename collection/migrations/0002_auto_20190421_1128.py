# Generated by Django 2.2 on 2019-04-21 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collection', '0001_initial'),
        ('garden', '0001_initial'),
        ('taxonomy', '0005_auto_20190421_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='accession',
            name='intended_locations',
            field=models.ManyToManyField(related_name='planned_accessions', through='garden.LocationPlanner', to='garden.Location'),
        ),
        migrations.AddField(
            model_name='accession',
            name='taxon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='accessions', to='taxonomy.Taxon'),
        ),
    ]
