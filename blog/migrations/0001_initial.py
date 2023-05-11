# Generated by Django 4.1.7 on 2023-05-10 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentService',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=500)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
