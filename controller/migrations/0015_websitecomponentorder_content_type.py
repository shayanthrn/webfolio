# Generated by Django 4.2.5 on 2023-11-29 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0014_alter_websitecomponentorder_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='websitecomponentorder',
            name='content_type',
            field=models.CharField(default='intro_component', max_length=20),
            preserve_default=False,
        ),
    ]