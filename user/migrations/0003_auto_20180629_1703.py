# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_is_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uname',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
