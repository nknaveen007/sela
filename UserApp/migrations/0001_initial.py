# Generated by Django 3.2.7 on 2021-09-15 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('UserId', models.AutoField(primary_key=True, serialize=False)),
                ('UserStatus', models.IntegerField(default=1)),
                ('PhoneNumber', models.CharField(default='', max_length=12)),
                ('Name', models.CharField(default='', max_length=100)),
                ('SelaId', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
