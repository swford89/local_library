# Generated by Django 3.2.7 on 2021-09-05 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20210904_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
    ]
