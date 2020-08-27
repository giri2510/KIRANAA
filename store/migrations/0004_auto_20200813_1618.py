# Generated by Django 3.1 on 2020-08-13 10:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0003_auto_20200813_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalorder',
            name='cust',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateField(verbose_name=datetime.datetime(2020, 8, 13, 10, 48, 43, 852602, tzinfo=utc)),
        ),
    ]
