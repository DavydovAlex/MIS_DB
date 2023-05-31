# Generated by Django 4.2 on 2023-05-29 03:48

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0011_query_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Augmentations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(default='')),
                ('status', models.IntegerField(choices=[(0, 'Waiting'), (1, 'Loaded'), (2, 'In Process')], default=0)),
                ('create_date', models.DateTimeField(default=datetime.datetime(1900, 1, 1, 0, 0))),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('uploaded_file', models.FileField(upload_to='')),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='query.query')),
            ],
        ),
        migrations.CreateModel(
            name='UploadingFields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='query.fields')),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='query.augmentations')),
            ],
        ),
    ]