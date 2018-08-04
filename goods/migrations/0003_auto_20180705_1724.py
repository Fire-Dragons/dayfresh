# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20180705_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indextypegoodsbanner',
            name='index',
            field=models.SmallIntegerField(verbose_name='展示顺序', unique=True, default=0),
        ),
    ]
