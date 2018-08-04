# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20180705_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexgoodsbanner',
            name='index',
            field=models.SmallIntegerField(default=0, verbose_name='展示顺序'),
        ),
        migrations.AlterField(
            model_name='indexpromotionbanner',
            name='index',
            field=models.SmallIntegerField(default=0, verbose_name='展示顺序'),
        ),
        migrations.AlterField(
            model_name='indextypegoodsbanner',
            name='index',
            field=models.SmallIntegerField(default=0, verbose_name='展示顺序'),
        ),
    ]
