# Generated by Django 4.1.4 on 2022-12-11 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CardStorage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='number',
            field=models.CharField(max_length=20, verbose_name='Номер'),
        ),
    ]