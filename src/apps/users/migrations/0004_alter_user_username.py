# Generated by Django 5.0 on 2023-12-31 12:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=30, unique=True, verbose_name="username"),
        ),
    ]
