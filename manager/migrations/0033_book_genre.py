# Generated by Django 3.1.3 on 2020-12-28 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0032_auto_20201228_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(null=True, related_name='genre_of_book', to='manager.Genre'),
        ),
    ]