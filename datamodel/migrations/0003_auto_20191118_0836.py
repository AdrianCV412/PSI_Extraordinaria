# Generated by Django 2.1.7 on 2019-11-18 08:36

import datamodel.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0002_counter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='cat1',
            field=models.IntegerField(default=0, validators=[datamodel.models.validate_in_board]),
        ),
        migrations.AlterField(
            model_name='game',
            name='cat2',
            field=models.IntegerField(default=2, validators=[datamodel.models.validate_in_board]),
        ),
        migrations.AlterField(
            model_name='game',
            name='cat3',
            field=models.IntegerField(default=4, validators=[datamodel.models.validate_in_board]),
        ),
        migrations.AlterField(
            model_name='game',
            name='cat4',
            field=models.IntegerField(default=6, validators=[datamodel.models.validate_in_board]),
        ),
        migrations.AlterField(
            model_name='game',
            name='cat_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_as_cat', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='mouse',
            field=models.IntegerField(default=59, validators=[datamodel.models.validate_in_board]),
        ),
        migrations.AlterField(
            model_name='game',
            name='mouse_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_as_mouse', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='move',
            name='date',
            field=models.DateField(default='2019-11-18'),
        ),
        migrations.AlterField(
            model_name='move',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moves', to='datamodel.Game'),
        ),
    ]
