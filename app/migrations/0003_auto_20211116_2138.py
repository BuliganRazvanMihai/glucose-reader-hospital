# Generated by Django 3.2 on 2021-11-16 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_device_glucosevalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='patientId',
            field=models.IntegerField(),
        ),
    ]
