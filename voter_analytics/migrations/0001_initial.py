# Generated by Django 4.2.16 on 2024-11-12 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Voter",
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
                ("voter_id", models.CharField(max_length=20)),
                ("last_name", models.TextField()),
                ("first_name", models.TextField()),
                ("street_number", models.IntegerField()),
                ("street_name", models.TextField()),
                ("apt_number", models.TextField()),
                ("zip_code", models.IntegerField()),
                ("date_of_birth", models.DateField()),
                ("day_of_reg", models.DateField()),
                ("party_affiliation", models.CharField(max_length=1)),
                ("precinct_number", models.CharField(max_length=1)),
                ("v20_state", models.BooleanField()),
                ("v21_town", models.BooleanField()),
                ("v21_primary", models.BooleanField()),
                ("v22_general", models.BooleanField()),
                ("v23_town", models.BooleanField()),
                ("voter_score", models.IntegerField()),
            ],
        ),
    ]
