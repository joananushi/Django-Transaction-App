# Generated by Django 4.2.5 on 2023-10-03 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=225, null=True)),
                ('last_name', models.CharField(max_length=225, null=True)),
                ('email', models.CharField(max_length=225, null=True)),
                ('password', models.CharField(max_length=225, null=True)),
                ('admin', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
