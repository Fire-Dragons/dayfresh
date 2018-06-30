# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('uname', models.CharField(max_length=100, unique=True)),
                ('upasswd', models.CharField(max_length=100)),
                ('umail', models.CharField(max_length=100)),
                ('is_activity', models.BooleanField(default=0)),
            ],
        ),
    ]
