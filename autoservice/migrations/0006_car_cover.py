# Generated by Django 5.1.3 on 2024-12-03 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0005_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='cover',
            field=models.ImageField(null=True, upload_to='covers', verbose_name='Cover'),
        ),
    ]