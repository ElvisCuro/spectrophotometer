# Generated by Django 5.1.2 on 2024-10-30 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eva1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordata',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
