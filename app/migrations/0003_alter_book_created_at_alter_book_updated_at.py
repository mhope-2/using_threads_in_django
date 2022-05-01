# Generated by Django 4.0.4 on 2022-04-27 19:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_book_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="book",
            name="updated_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]