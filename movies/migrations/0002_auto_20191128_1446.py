# Generated by Django 2.2.7 on 2019-11-28 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='comment',
            field=models.CharField(max_length=150),
        ),
    ]