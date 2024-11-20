# Generated by Django 5.1.2 on 2024-11-20 23:13

import report.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', report.fields.ThumbnailImageField(blank=True, null=True, upload_to='report/%Y/%m')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='LATITUDE')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='LONGITUDE')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='DATE')),
            ],
            options={
                'ordering': ('date',),
            },
        ),
    ]
