# Generated by Django 3.2.19 on 2023-06-05 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20230605_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='final_result',
            name='nameServerwhois',
            field=models.TextField(blank=True),
        ),
    ]
