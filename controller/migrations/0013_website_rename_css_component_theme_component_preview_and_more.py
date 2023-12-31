# Generated by Django 4.2.5 on 2023-11-23 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0012_component_css'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameField(
            model_name='component',
            old_name='css',
            new_name='theme',
        ),
        migrations.AddField(
            model_name='component',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='static/component_previews/'),
        ),
        migrations.CreateModel(
            name='WebsiteComponentOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controller.component')),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controller.website')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='website',
            name='components',
            field=models.ManyToManyField(through='controller.WebsiteComponentOrder', to='controller.component'),
        ),
        migrations.AddField(
            model_name='website',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
