# Generated by Django 2.2.7 on 2019-12-07 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0012_auto_20191203_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='date',
            field=models.DateField(default='2019-12-07'),
        ),
    ]