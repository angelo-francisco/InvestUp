# Generated by Django 5.1 on 2024-08-10 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0016_alter_notifications_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='date',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
