# Generated by Django 2.1.2 on 2018-10-23 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=250)),
                ('file_name', models.CharField(max_length=250)),
                ('org_file', models.FileField(upload_to='')),
            ],
        ),
    ]
