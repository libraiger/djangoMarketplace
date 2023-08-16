# Generated by Django 4.2.2 on 2023-08-16 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("talent", "0003_person_github_link_person_website_link_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="person",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
