# Generated by Django 4.2 on 2023-05-29 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0012_augmentations_uploadingfields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadingfields',
            old_name='query',
            new_name='augmentation',
        ),
        migrations.AlterField(
            model_name='augmentations',
            name='uploaded_file',
            field=models.CharField(default=''),
        ),
    ]
