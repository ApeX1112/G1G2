# Generated by Django 4.2.16 on 2024-10-19 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirportData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.CharField(max_length=255)),
                ('temperature_en_chiffre', models.FloatField()),
                ('humidity_en_chiffre', models.IntegerField()),
                ('temperature_en_chiffre_2days_left', models.FloatField()),
                ('humidity_en_chiffre_2days_left', models.IntegerField()),
                ('faa_designator', models.CharField(blank=True, max_length=10, null=True)),
                ('length_ft', models.FloatField(blank=True, null=True)),
                ('tail_height_at_oew_ft', models.FloatField(blank=True, null=True)),
                ('wheelbase_ft', models.FloatField(blank=True, null=True)),
                ('date', models.DateField()),
                ('std', models.TimeField()),
                ('atd', models.TimeField(blank=True, null=True)),
                ('type', models.CharField(max_length=50)),
                ('fluid', models.IntegerField()),
                ('water', models.IntegerField()),
                ('meteo', models.CharField(blank=True, max_length=50, null=True)),
                ('oat', models.FloatField()),
                ('finish', models.CharField(max_length=255)),
                ('duration', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
