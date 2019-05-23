# Generated by Django 2.2 on 2019-05-23 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0004_plant_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField(default=1)),
                ('width', models.IntegerField(default=1)),
                ('image', models.ImageField(height_field='height', upload_to='images/plants/', width_field='width')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.Plant')),
            ],
        ),
    ]
