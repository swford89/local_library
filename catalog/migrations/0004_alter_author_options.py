# Generated by Django 3.2.7 on 2021-09-05 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210905_1611'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'middle_name', 'first_name']},
        ),
    ]
