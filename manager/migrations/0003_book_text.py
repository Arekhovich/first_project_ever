# Generated by Django 3.1.3 on 2020-12-02 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_book_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='text',
            field=models.TextField(max_length=200, null=True),
        ),
    ]