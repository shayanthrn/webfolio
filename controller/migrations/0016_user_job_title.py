# Generated by Django 4.2.5 on 2023-11-29 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0015_websitecomponentorder_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='job_title',
            field=models.CharField(default='Software Developer', max_length=255),
            preserve_default=False,
        ),
    ]
