# Generated by Django 3.0.4 on 2020-03-15 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20200314_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='io',
            name='pin',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
