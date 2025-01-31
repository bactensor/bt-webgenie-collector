# Generated by Django 4.2.18 on 2025-01-30 14:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="leaderboardsession",
            name="unique_leaderboardsession_validator_external_id",
        ),
        migrations.AddIndex(
            model_name="leaderboardsession",
            index=models.Index(fields=["-created_at"], name="core_leader_created_752fdb_idx"),
        ),
    ]
