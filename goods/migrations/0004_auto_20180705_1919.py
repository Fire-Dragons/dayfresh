# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20180705_1724'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indexgoodsbanner',
            old_name='imaee',
            new_name='image',
        ),
        migrations.AlterField(
            model_name='indexgoodsbanner',
            name='index',
            field=models.SmallIntegerField(verbose_name='展示顺序', unique=True, default=0),
        ),
    ]
