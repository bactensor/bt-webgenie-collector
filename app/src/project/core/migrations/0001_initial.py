# Generated by Django 4.2.18 on 2025-01-18 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Challenge",
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
                (
                    "external_id",
                    models.BigIntegerField(
                        help_text="ID as if in Validator's internals"
                    ),
                ),
                ("received_at", models.DateTimeField(auto_now_add=True)),
                ("ground_truth_html", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Competition",
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
                (
                    "external_id",
                    models.BigIntegerField(
                        help_text="ID as if in Validator's internals"
                    ),
                ),
                ("received_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EvaluationType",
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
                (
                    "external_id",
                    models.BigIntegerField(
                        help_text="ID as if in Validator's internals"
                    ),
                ),
                ("received_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Judgement",
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
                (
                    "external_id",
                    models.BigIntegerField(
                        help_text="ID as if in Validator's internals"
                    ),
                ),
                ("received_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="LeaderboardSession",
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
                (
                    "external_id",
                    models.BigIntegerField(
                        help_text="ID as if in Validator's internals"
                    ),
                ),
                ("received_at", models.DateTimeField(auto_now_add=True)),
                ("created_at", models.DateTimeField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Neuron",
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
                ("hotkey", models.CharField(max_length=48)),
                ("is_active_validator", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="TaskSolution",
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
                (
                    "external_id",
                    models.BigIntegerField(
                        help_text="ID as if in Validator's internals"
                    ),
                ),
                ("received_at", models.DateTimeField(auto_now_add=True)),
                ("created_at", models.DateTimeField()),
                ("miner_answer", models.JSONField()),
                (
                    "challenge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_solutions",
                        to="core.challenge",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_data",
                        to="core.neuron",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SolutionEvaluation",
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
                (
                    "external_id",
                    models.BigIntegerField(
                        help_text="ID as if in Validator's internals"
                    ),
                ),
                ("received_at", models.DateTimeField(auto_now_add=True)),
                ("value", models.FloatField()),
                (
                    "evaluation_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="solution_evaluations",
                        to="core.evaluationtype",
                    ),
                ),
                (
                    "judgement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="solution_evaluations",
                        to="core.judgement",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_data",
                        to="core.neuron",
                    ),
                ),
                (
                    "task_solution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="solution_evaluations",
                        to="core.tasksolution",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddConstraint(
            model_name="neuron",
            constraint=models.UniqueConstraint(
                fields=("hotkey",), name="unique_neuron_hotkey"
            ),
        ),
        migrations.AddField(
            model_name="leaderboardsession",
            name="competition",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="leaderboard_sessions",
                to="core.competition",
            ),
        ),
        migrations.AddField(
            model_name="leaderboardsession",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_data",
                to="core.neuron",
            ),
        ),
        migrations.AddField(
            model_name="judgement",
            name="miner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="miner_judgements",
                to="core.neuron",
            ),
        ),
        migrations.AddField(
            model_name="judgement",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_data",
                to="core.neuron",
            ),
        ),
        migrations.AddField(
            model_name="judgement",
            name="validator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="validator_judgements",
                to="core.neuron",
            ),
        ),
        migrations.AddField(
            model_name="evaluationtype",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_data",
                to="core.neuron",
            ),
        ),
        migrations.AddField(
            model_name="competition",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_data",
                to="core.neuron",
            ),
        ),
        migrations.AddField(
            model_name="challenge",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_data",
                to="core.neuron",
            ),
        ),
        migrations.AddField(
            model_name="challenge",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="challenges",
                to="core.leaderboardsession",
            ),
        ),
        migrations.AddConstraint(
            model_name="tasksolution",
            constraint=models.UniqueConstraint(
                fields=("sender", "external_id"),
                name="unique_tasksolution_validator_external_id",
            ),
        ),
        migrations.AddConstraint(
            model_name="solutionevaluation",
            constraint=models.UniqueConstraint(
                fields=("sender", "external_id"),
                name="unique_solutionevaluation_validator_external_id",
            ),
        ),
        migrations.AddConstraint(
            model_name="leaderboardsession",
            constraint=models.UniqueConstraint(
                fields=("sender", "external_id"),
                name="unique_leaderboardsession_validator_external_id",
            ),
        ),
        migrations.AddConstraint(
            model_name="judgement",
            constraint=models.UniqueConstraint(
                fields=("sender", "external_id"),
                name="unique_judgement_validator_external_id",
            ),
        ),
        migrations.AddConstraint(
            model_name="evaluationtype",
            constraint=models.UniqueConstraint(
                fields=("sender", "external_id"),
                name="unique_evaluationtype_validator_external_id",
            ),
        ),
        migrations.AddConstraint(
            model_name="competition",
            constraint=models.UniqueConstraint(
                fields=("sender", "external_id"),
                name="unique_competition_validator_external_id",
            ),
        ),
        migrations.AddConstraint(
            model_name="challenge",
            constraint=models.UniqueConstraint(
                fields=("sender", "external_id"),
                name="unique_challenge_validator_external_id",
            ),
        ),
    ]
