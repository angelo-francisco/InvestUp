# Generated by Django 5.0.7 on 2024-08-07 23:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0011_metrics"),
    ]

    operations = [
        migrations.AlterField(
            model_name="metrics",
            name="value",
            field=models.FloatField(),
        ),
    ]
