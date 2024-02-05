# Generated by Django 4.2.5 on 2024-01-22 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stars', models.IntegerField()),
                ('title', models.CharField(max_length=1000)),
                ('content', models.CharField(max_length=10000)),
                ('category1', models.CharField(max_length=100)),
                ('category2', models.CharField(max_length=100)),
            ],
        ),
    ]
