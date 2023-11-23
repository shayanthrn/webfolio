# Generated by Django 4.2.5 on 2023-11-23 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0009_work_portfolio_education'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('intro', 'Introduction'), ('education', 'Education'), ('work', 'Work Experience'), ('portfolio', 'Portfolio'), ('skills', 'Skills')], max_length=10)),
                ('html', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='static/portfolio_thumbnails/'),
        ),
    ]