# Generated by Django 4.2.13 on 2024-06-07 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_result_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='filePath',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
