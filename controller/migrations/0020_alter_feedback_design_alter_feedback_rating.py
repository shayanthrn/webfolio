# Generated by Django 4.2.5 on 2023-11-30 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0019_alter_websitecomponentorder_theme_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='design',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]
