# Generated by Django 5.0.7 on 2024-08-07 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0008_alter_company_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="logo",
            field=models.FileField(upload_to="logos"),
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("document", models.FileField(upload_to="documents")),
                ("slug", models.SlugField(blank=True, max_length=100, unique=True)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="companies.company",
                    ),
                ),
            ],
        ),
    ]
