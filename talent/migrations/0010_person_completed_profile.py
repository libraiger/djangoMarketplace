# Generated by Django 4.2.2 on 2023-09-13 10:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("talent", "0009_bountyclaim_expected_finish_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="completed_profile",
            field=models.BooleanField(default=False),
        ),
    ]
