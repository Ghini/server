# Generated by Django 2.2 on 2019-04-21 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0004_auto_20190421_1240'),
        ('garden', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='code',
            field=models.CharField(default='1', max_length=8),
        ),
        migrations.AlterField(
            model_name='location',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='locationplanner',
            name='date_done',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='locationplanner',
            name='plant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='garden.Plant'),
        ),
        migrations.AlterUniqueTogether(
            name='plant',
            unique_together={('accession', 'code')},
        ),
    ]
