# Generated by Django 4.0 on 2021-12-20 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vkapi', '0002_category_rename_user_user_auth_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='info',
        ),
        migrations.RemoveField(
            model_name='groups',
            name='domain',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='catalog',
            new_name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Data',
        ),
        migrations.DeleteModel(
            name='Groups',
        ),
    ]
