# Generated by Django 5.0.7 on 2024-08-09 21:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("investors", "0002_investmentproposal_slug"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="investmentproposal",
            name="slug",
        ),
    ]
