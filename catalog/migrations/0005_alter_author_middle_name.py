# Generated by Django 3.2.7 on 2021-09-07 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_author_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='middle_name',
            field=models.CharField(max_length=100),
        ),
    ]
