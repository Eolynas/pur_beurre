# Generated by Django 3.1.6 on 2021-04-28 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0010_auto_20210428_0949"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(null=True, upload_to=""),
        ),
    ]
