# Generated by Django 4.2 on 2023-04-11 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0003_alter_params_type_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Uploadings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.FilePathField()),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='query.query')),
            ],
        ),
        migrations.CreateModel(
            name='ParamsValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=250)),
                ('param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='query.params')),
                ('uploading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='query.uploadings')),
            ],
        ),
    ]