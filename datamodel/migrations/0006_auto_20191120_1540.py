# Generated by Django 2.1.5 on 2019-11-20 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0005_auto_20191119_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='date',
            field=models.DateField(default='2019-11-20'),
        ),
    ]