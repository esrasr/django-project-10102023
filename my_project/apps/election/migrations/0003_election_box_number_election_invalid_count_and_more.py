# Generated by Django 4.2.5 on 2023-10-07 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("election", "0002_add_city"),
    ]

    operations = [
        migrations.AddField(
            model_name="election",
            name="box_number",
            field=models.CharField(default="S-000000"),
        ),
        migrations.AddField(
            model_name="election",
            name="invalid_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="election",
            name="count",
            field=models.PositiveIntegerField(),
        ),
    ]
