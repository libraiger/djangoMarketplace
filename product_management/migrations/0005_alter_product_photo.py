# Generated by Django 4.2.2 on 2023-10-30 05:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product_management", "0004_alter_product_capability_start"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
    ]
