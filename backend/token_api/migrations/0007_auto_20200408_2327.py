# Generated by Django 3.0.5 on 2020-04-08 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('token_api', '0006_auto_20200408_2245'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='actionpolicy',
            unique_together={('policy_name',)},
        ),
        migrations.AlterUniqueTogether(
            name='token',
            unique_together={('token_id',)},
        ),
    ]
