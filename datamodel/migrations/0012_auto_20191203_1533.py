# Generated by Django 2.1.7 on 2019-12-03 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0011_auto_20191126_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='date',
            field=models.DateField(default='2019-12-03'),
        ),
    ]
