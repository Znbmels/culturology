# Generated by Django 5.0.2 on 2025-04-26 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tribes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="people",
            name="history",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="people",
            name="audio",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="people",
            name="language",
            field=models.CharField(max_length=50),
        ),
    ]
