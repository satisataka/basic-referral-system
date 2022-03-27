# Generated by Django 3.2.12 on 2022-03-26 01:32

import datetime
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20220324_2045'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phonetoken',
            options={'verbose_name': 'Code', 'verbose_name_plural': 'Codes'},
        ),
        migrations.AddField(
            model_name='phonetoken',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 26, 4, 32, 25, 819281), editable=False),
        ),
        migrations.AlterField(
            model_name='phonetoken',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(editable=False, max_length=128, region=None, unique=True),
        ),
    ]