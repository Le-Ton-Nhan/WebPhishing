# Generated by Django 3.2.19 on 2023-05-29 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_final_result_img_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='final_result',
            name='connection_speed',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='final_result',
            name='host',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='final_result',
            name='host_country',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='final_result',
            name='num_open_ports',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='final_result',
            name='open_ports',
            field=models.TextField(blank=True),
        ),
    ]
