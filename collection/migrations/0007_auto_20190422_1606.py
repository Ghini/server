# Generated by Django 2.2 on 2019-04-22 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0007_auto_20190421_2118'),
        ('collection', '0006_auto_20190421_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accession',
            name='taxon',
        ),
        migrations.AddField(
            model_name='contact',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('0', 'The name of the record has not been checked by any authority.'), ('1', 'The name of the record determined by comparison with other named plants.'), ('2', 'The name of the record determined by a taxonomist or by other competent persons using herbarium and/or library and/or documented living material.'), ('3', 'The name of the plant determined by taxonomist engaged in systematic revision of the group.'), ('4', 'The record is part of type gathering or propagated from type material by asexual methods')], default='0', max_length=1)),
                ('date', models.DateField()),
                ('accession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verifications', to='collection.Accession')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='verifications', to='collection.Contact')),
                ('taxon', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='verifications', to='taxonomy.Taxon')),
            ],
        ),
        migrations.AddField(
            model_name='accession',
            name='taxa',
            field=models.ManyToManyField(related_name='accessions', through='collection.Verification', to='taxonomy.Taxon'),
        ),
    ]
