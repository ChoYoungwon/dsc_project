# Generated by Django 5.1.2 on 2024-11-16 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_remove_report_link_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='DATE'),
        ),
    ]
