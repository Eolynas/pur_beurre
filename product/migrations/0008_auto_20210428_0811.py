# Generated by Django 3.1.6 on 2021-04-28 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0007_auto_20210428_0807"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(null=True, upload_to=""),
        ),
    ]
