# Generated by Django 2.1.1 on 2018-09-28 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20180706_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.CharField(choices=[('INCOMPLETE', 'Incomplete'), ('COMPLETE', 'Complete')], default='Incomplete', max_length=16),
        ),
    ]
