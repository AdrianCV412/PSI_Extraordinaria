# Generated by Django 2.2.7 on 2020-05-30 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0017_auto_20191212_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='move',
            name='date',
            field=models.DateField(default='2020-05-30'),
        ),
    ]
