# Generated by Django 5.1.2 on 2024-11-20 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priority',
            name='severity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]